from .models import Process, RunningProcess
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json
from pyhive.extra.django import DjangoModelSerializer
from pyhive.serializers import ListSerializer, GenericObjectSerializer
import datetime


def process_list(request):
    serializer = ListSerializer(item_serializer=DjangoModelSerializer())
    data = serializer.serialize(Process.objects.all())
    j = json.dumps(data)
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

    p.save() # Save the running process to the DB

    # Return response to the client. TODO: Create correct getstatus url!
    response = {
        "success": True,
        "polling_url": "/status"
    }
    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")


def status(request, pk):
    st = Process.objects.get(id=pk).runningprocess_set.get().finished

    response = {
        "status": st
    }
    j = json.dumps(response)
    return HttpResponse(j, content_type="application/json")
