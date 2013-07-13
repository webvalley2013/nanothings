from django.contrib import admin
from process.models import Process, RunningProcess

admin.site.register(Process)
admin.site.register(RunningProcess)
