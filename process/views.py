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


@csrf_exempt
def run_process_post(request):
    n1 = request.POST["n1"]
    n2 = request.POST["n2"]

    # Load correct task from celery tasks
    from tasks import minus

    # Add task to broker code
    task = minus.delay(n1,n2)

    # Save running process to db

    process_fk = Process.objects.get(process_code="process_post")
    p = RunningProcess()
    p.process_type =  process_fk# (3d, hadoop, R/PLR, ...)
    p.task_id = task.id
    p.started = datetime.datetime.now()
    p.inputs = {
        "n1": n1,
        "n2": n2
    }

    p.save()  # Save the running process to the DB

    # Return response to the client. TODO: Create correct getstatus url!
    response = {
        "success": True,
        "polling_url": "/status"
    }

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
def detail(request, pk):
    pr = Process.objects.get(id=pk)

    serializer = DjangoModelSerializer()
    data = serializer.serialize(pr)
    j = json.dumps(data)

    return HttpResponse(j, content_type="application/json")

