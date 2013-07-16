# MODULES
from django.shortcuts import render, get_object_or_404
from process.models import RunningProcess, Process
from process.views import abort as api_abort
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


#
# ADMIN TOOLS (PROCESS MANAGEMENT) TODO: Check user auth
#
@login_required
def list_of_processes(request):
    pList = RunningProcess.objects.all()
    context = {"pList": pList}
    return render(request, "process_list.html", context)


@login_required
def detail(request, p_id):
    pr = get_object_or_404(RunningProcess, pk=p_id)
    return render(request, "detail.html", {"pr": pr})


@login_required
def abort(request, p_id):
    return api_abort(request, p_id)


#
# BASIC PAGES
#
def home(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def contacts(request):
    return render(request, "contacts.html")


def img_analysis(request):
    return render(request, "project/img_analysis.html")


def r_plr(request):
    return render(request, "project/r_plr.html")


def networks(request):
    return render(request, "project/networks.html")


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, "index.html")
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            return render(request, "loginerr.html", {
                "text": "Disabled account!"
            })
    else:
        # Return an 'invalid login' error message.
        return render(request, "loginerr.html", {
            "text": "Invalid login!"
        })


def logout_view(request):
    logout(request)
    return render(request, "index.html")