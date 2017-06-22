from rest_framework import serializers
from .models import *


class TodoitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todoitem
        fields = ('id','description','completed','due_by','todolist')

class TodolistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    items = TodoitemSerializer(many=True)
    # items = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model = Todolist
        fields = ('id','user','name','creation_date','items')



class PrettyListSerializer(serializers.ModelSerializer):
    #items = serializers.StringRelatedField(many=True)
    items = TodoitemSerializer(many=True)

    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Todolist
        fields = ('id','user','name','creation_date','items')

