from django.db import models
import jsonfield
import celery
from celery.result import BaseAsyncResult
import djcelery

class Process(models.Model):
    TYPE_CHOICES = (
        ('plr', 'plr'),
        ('hadoop', 'hadoop'),
        ('3d', '3d')
    )

    process_code = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=40)
    date = models.DateTimeField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    inputs = jsonfield.JSONField()
    outputs = jsonfield.JSONField()

    def __unicode__(self):
        return u'%s' % (self.process_code)


class RunningProcess(models.Model):
    process_type = models.ForeignKey(Process)
    task_id = models.CharField(max_length=36)
    inputs = jsonfield.JSONField()
    started = models.DateTimeField()

    # From id returns task result
    @property
    def celery_task(self):
        return djcelery.celery.AsyncResult(self.task_id)

    # Check the status of the task
    @property
    def finished(self):
        return self.celery_task.ready()