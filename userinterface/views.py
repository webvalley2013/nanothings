# This file is part of nanothings.
#
#     nanothings is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero GPL as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     nanothings is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero GPL for more details.
#
#     You should have received a copy of the GNU Affero GPL
#     along with nanothings.  If not, see <http://www.gnu.org/licenses/>.

# MODULES
from django.shortcuts import render, get_object_or_404
from process.models import RunningProcess, Process
from process.views import abort as api_abort
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


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


@login_required
def celery_error(request):
    return render(request, "celeryerr.html")


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


def hadoop(request):
    return render(request, "project/hadoop.html")


def api_doc(request):
    return render(request, "apidoc.html")


def license(request):
    return render(request, "license.html")


#
# LOGIN AND LOGOUT VIEWS
#
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return redirect("home")
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
    return redirect("home")