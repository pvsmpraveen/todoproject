from rest_framework import serializers
from .models import *

class TodolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ('id','name','creation_date','user')


class TodoitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoitem
        fields = ('id','description','completed','due_by')


