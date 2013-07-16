# MODULES
from django.views.decorators.csrf import csrf_exempt
from .models import Process, RunningProcess
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from pyhive.extra.django import DjangoModelSerializer
from pyhive.serializers import ListSerializer, GenericObjectSerializer
import datetime
import djcelery


# Modifier for serialization
def mod(obj, current, *args, **kwargs):
    for i in current:
        del i['date'], i['inputs'], i['outputs']
    return current


# Return a JSON with all the processes
def process_list(request):
    serializer = ListSerializer(item_serializer=DjangoModelSerializer())
    data = serializer.serialize(Process.objects.all(), modifiers=[mod])
    j = json.dumps(data)
    return HttpResponse(j, content_type="application/json")


def run_process_test(request, n1, n2):
    # Load correct task from celery tasks
    from tasks import add

    # Add task to broker code
    task = add.delay(n1, n2)

    # Save running process to db
    process_fk = Process.objects.get(process_code="process_test")
    p = RunningProcess()
    p.process_type = process_fk  # (3d, hadoop, R/PLR, ...)
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
        "polling_url": "/process/status/" + str(p.pk)
    }
    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


def run_process_get(request):

    n1 = request.GET["n1"]
    n2 = request.GET["n2"]

    # Load correct task from celery tasks
    from tasks import multiply

    # Add task to broker code
    task = multiply.delay(n1,n2)

    # Save running process to db

    process_fk = Process.objects.get(process_code="process_get")
    p = RunningProcess()
    p.process_type =  process_fk  # (3d, hadoop, R/PLR, ...)
    p.task_id = task.id
    p.started = datetime.datetime.now()
    p.inputs = {
        "n1": n1,
        "n2": n2
    }

    p.save() # Save the running process to the DB

    # Return response to the client. TODO: Create correct getstatus url!
    response = {
        "success": True,
        "polling_url": "/status"
    }
    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


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


def status(request, pk):
    pr = RunningProcess.objects.get(id=pk)

    response = { "finished": pr.finished, "status": pr.status }

    if pr.finished:
        response["result"] = pr.result
        response["finished_time"] = pr.finished_time

    # Timestamp for finished process

    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


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

