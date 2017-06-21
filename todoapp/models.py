# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todolist(models.Model):
    name = models.CharField(max_length=128)
    creation_date = models.DateField()
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)

    def __unicode__(self):
        return ",".join([str(self.name),str(self.creation_date)])

class Todoitem(models.Model):
    description = models.CharField(max_length=128)
    completed = models.BooleanField()
    due_by = models.DateField()

    todolist = models.ForeignKey(Todolist,related_name='items',on_delete=models.CASCADE)
    def __unicode__(self):
        return ",".join([str(self.id),str(self.description), str(self.completed),str(self.due_by)])