from django.shortcuts import render, get_object_or_404
from process.models import RunningProcess, Process
from process.views import abort as api_abort


# TODO: Check user auth
def list_of_processes(request):
    pList = RunningProcess.objects.all()
    context = {"pList": pList}
    return render(request, "process_list.html", context)


def detail(request, p_id):
    pr = get_object_or_404(RunningProcess, pk=p_id)
    return render(request, "detail.html", {"pr": pr})


def abort(request, p_id):
    return api_abort(request, p_id)


def home(request):
    return render(request, "index.html")