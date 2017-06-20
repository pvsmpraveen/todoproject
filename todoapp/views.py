# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render

from .models import *
from todoapp.serializers import *


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(request, *args, **kwargs)

#################### TODOLIST #####################################

class todolists(CSRFExemptMixin,APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get(self,request,format=None):
        snippets = Todolist.objects.all()
        serializer = TodolistSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodolistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class todolists_detail(CSRFExemptMixin,APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get_object(self, listid):
        try:
            return Todolist.objects.get(pk=listid)
        except Todolist.DoesNotExist:
            raise Http404

    def get(self, request, listid, format=None):
        snippet = self.get_object(listid)
        serializer = TodolistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, listid, format=None):
        snippet = self.get_object(listid)
        # print snippet
        serializer = TodolistSerializer(snippet, data=request.data)
        # print serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, listid, format=None):
        snippet = self.get_object(listid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################### TODOITEM ############################

class todoitems(CSRFExemptMixin,APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get(self,request,format=None):
        snippets = Todoitem.objects.all()
        serializer = TodoitemSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoitemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class todoitems_detail(CSRFExemptMixin,APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get_object(self, listid):
        try:
            return Todoitem.objects.get(pk=listid)
        except Todoitem.DoesNotExist:
            raise Http404

    def get(self, request, listid, format=None):
        snippet = self.get_object(listid)
        serializer = TodoitemSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, listid, format=None):
        snippet = self.get_object(listid)
        # print snippet
        serializer = TodoitemSerializer(snippet, data=request.data)
        # print serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#################### TODOLIST ITEMS #####################################
class items_todolist(CSRFExemptMixin,APIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get(self,request,listid,format=None):
        snippets = Todoitem.objects.filter(todolist=listid)
        serializer = TodoitemSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request,listid, format=None):
        request.data["todolist"] = listid
        serializer = TodoitemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class items_todolist_detail(CSRFExemptMixin, APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    authentication_classes = ()
    permission_classes =  ()

    def get_object(self, itemid):
        try:
            return Todoitem.objects.get(pk=itemid)
        except Todoitem.DoesNotExist:
            raise Http404

    def get(self, request,listid,itemid, format=None):
        snippet = self.get_object(itemid)
        serializer = TodoitemSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, listid,itemid, format=None):
        snippet = self.get_object(itemid)
        request.data["todolist"] = listid
        serializer = TodoitemSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, studentid, format=None):
        snippet = self.get_object(studentid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)