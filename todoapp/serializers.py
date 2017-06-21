from rest_framework import serializers
from .models import *

class TodolistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Todolist
        fields = ('id','user','name','creation_date')


class TodoitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoitem
        fields = ('id','description','completed','due_by','todolist')

class PrettyListSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Todolist
        fields = ('id','user','name','creation_date','items')

