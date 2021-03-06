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
from django.db import models
import jsonfield
import djcelery


class Process(models.Model):

    TYPE_CHOICES = (
        ('plr', 'plr'),
        ('hadoop', 'hadoop'),
        ('3d', '3d')
    )

    # Fields
    code = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=40)
    date = models.DateTimeField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    inputs = jsonfield.JSONField()
    outputs = jsonfield.JSONField()

    def __unicode__(self):
        return u'%s' % (self.code)


class RunningProcess(models.Model):

    # Fields
    process_type = models.ForeignKey(Process)
    task_id = models.CharField(max_length=36)
    inputs = jsonfield.JSONField()
    started = models.DateTimeField()

    # From id returns task result
    @property
    def celery_task(self):
        return djcelery.celery.AsyncResult(self.task_id)

    # Check if the task has finished
    @property
    def finished(self):
        return self.celery_task.ready()

    # Return the current status of the task
    @property
    def status(self):
        return self.celery_task.status

    # Returns the result of the task
    @property
    def result(self):
        return self.celery_task.get()

    # Returns the time when the task has finished
    @property
    def finished_time(self):
        return 0  # tmp
