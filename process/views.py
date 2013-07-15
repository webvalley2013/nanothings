from django.views.decorators.csrf import csrf_exempt
from .models import Process, RunningProcess
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from pyhive.extra.django import DjangoModelSerializer
from pyhive.serializers import ListSerializer, GenericObjectSerializer
import datetime


def process_list(request):
    serializer = ListSerializer(item_serializer=DjangoModelSerializer())
    data = serializer.serialize(Process.objects.all())
    j = json.dumps(data)
    # "polls/index.html"
    return HttpResponse(j, content_type="application/json")


def run_process_test(request, n1, n2):
    # Load correct task from celery tasks
    from tasks import add

    # Add task to broker code
    task = add.delay(n1, n2)

    # Save running process to db
    task_id = task.id
    process_fk = Process.objects.get(process_code="process_test")
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
    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


'''
{
  "n1":"INT",
  "n2":"INT"
}
'''
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
    p.process_type =  process_fk# (3d, hadoop, R/PLR, ...)
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

    p.save() # Save the running process to the DB

    # Return response to the client. TODO: Create correct getstatus url!
    response = {
        "success": True,
        "polling_url": "/status"
    }


def status(request, pk):
    pr = RunningProcess.objects.get(id = pk)

    response = { "status": pr.finished }
    response["code"] = pr.status  # TMP

    if pr.finished:
        response["result"] = pr.result

    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")
