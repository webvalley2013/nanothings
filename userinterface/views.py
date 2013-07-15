# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from process.models import RunningProcess, Process


# TODO: Check user auth
def list_of_processes(request):
    pList = RunningProcess.objects.all()
    context = {"pList": pList}
    return render(request, "userinterface/process_list.html", context)


def detail(request, p_id):
    pr = get_object_or_404(RunningProcess, pk=p_id)
    return render(request, "userinterface/detail.html", {"pr": pr})


def home(request):


    return render(request, "userinterface/index.html")