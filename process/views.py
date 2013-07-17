# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.
# MODULES
from django.views.decorators.csrf import csrf_exempt
from .models import Process, RunningProcess
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
import djcelery
from pyhive.extra.django import DjangoModelSerializer
from pyhive.serializers import ListSerializer, GenericObjectSerializer
from ajaxutils.decorators import ajax
from django.contrib.auth.decorators import login_required

from .models import Process, RunningProcess
from .formbuilder import FormFactory
from nanothings.utils import create_dir_name
from nanothings.settings import DEFAULT_OUTPUT_PATH


# Modifier for serialization
def mod(obj, current, *args, **kwargs):
    for i in current:
        del i['date'], i['inputs'], i['outputs']
    return current


# Return a JSON with all the processes
@ajax()
def process_list(request):
    serializer = ListSerializer(item_serializer=DjangoModelSerializer())
    data = serializer.serialize(Process.objects.all(), modifiers=[mod])
    return data

@ajax(require_POST=True)
@csrf_exempt
def run_process_3d(request, p_id):
    try:
        proc = Process.objects.get(pk=p_id)
    except Process.DoesNotExist:
        return {'success': False,
                'message': 'process with id {0} does not exists'.format(p_id)}, 400

    if proc.type != '3d':
        return {'success': False,
                'message': 'process with id {0} is not a 3d analisys'.format(p_id)}, 400


    # If the parameters are correct:
    ProcessForm = FormFactory(proc).build_form()
    form = ProcessForm(request.POST)
    if form.is_valid():
        parameters = form.save()
        from .tasks import run_3d_analisys

        # Add task to broker code
        try:
            outdir = create_dir_name(DEFAULT_OUTPUT_PATH)
            task = run_3d_analisys.delay(parameters["nucleus1"], parameters["nucleus2"], parameters["litaf1"], parameters["litaf2"], outdir)
        except Exception as e:
            return {
                'success': False,
                'message': 'Internal server error ' + e.message
            }, 500
        else:

            # Save running process to db
            process_fk = Process.objects.get(code="3dprova")
            p = RunningProcess()
            p.process_type = process_fk  # (3d, hadoop, R/PLR, ...)
            p.task_id = task.id
            p.started = datetime.datetime.now()
            p.inputs = json.dumps(parameters)
            p.save() # Save the running process to the DB

            # Return response to the client.
            return {
                'success': True,
                'polling_url': '/process/status/' + str(p.pk)
            }

    else:
        return {
            'success': False,
            'message': 'input parameters were invalid'
        }, 400

@ajax(require_POST=True)
@csrf_exempt
def run_test_int(request, p_id):
    try:
        proc = Process.objects.get(pk=p_id)
    except Process.DoesNotExist:
        return {'success': False,
                'message': 'process with id {0} does not exists'.format(p_id)}, 400

    if proc.type != '3d':
        return {'success': False,
                'message': 'process with id {0} is not a 3d analisys'.format(p_id)}, 400


    # If the parameters are correct:
    ProcessForm = FormFactory(proc).build_form()
    form = ProcessForm(request.POST)
    if form.is_valid():
        parameters = form.save()
        from .tasks import process_int

        # Add task to broker code
        try:
            task = process_int.delay(parameters["input1"], parameters["input2"], parameters["input3"])
        except Exception as e:
            return {
                       'success': False,
                       'message': 'Internal server error ' + e.message
                   }, 500
        else:

            # Save running process to db
            p = RunningProcess()
            p.process_type = proc  # (3d, hadoop, R/PLR, ...)
            p.task_id = task.id
            p.started = datetime.datetime.now()
            p.inputs = json.dumps(parameters)
            p.save() # Save the running process to the DB

            # Return response to the client.
            return {
                'success': True,
                'polling_url': '/process/status/' + str(p.pk)
            }

    else:
        return {
                   'success': False,
                   'message': 'input parameters were invalid'
               }, 400



@ajax()
def status(request, pk):
    pr = RunningProcess.objects.get(id=pk)

    response = {
        'finished': pr.finished,
        'status': pr.status
    }

    if pr.finished:
        if pr.status != 'FAILURE':
            response["result"] = pr.result
        # response["finished_time"] = pr.finished_time

    return response


# Abort a task given his UUID
@login_required
def abort(request, task_id):
    try:
        pr = RunningProcess.objects.get(id=task_id)
    except RunningProcess.DoesNotExist:
        response = {
            "success": False,
            "message": "the requested process does not exist"
        }
    else:
        wk = djcelery.celery.Worker  # Celery Worker
        wk.app.control.revoke(pr.task_id, terminate=True)  # Revoke task
        pr.delete()  # Delete from the DB

        response = {
            "success": True
        }

    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


# Returns a JSON with the properties of the given id of the task
@login_required
def detail(request, pk):
    pr = Process.objects.get(id=pk)

    serializer = DjangoModelSerializer()
    data = serializer.serialize(pr)
    j = json.dumps(data)

    return HttpResponse(j, content_type="application/json")

