# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import RedirectView, FormView

from .models import *
from todoapp.serializers import *


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .forms import MyRegistrationForm


@login_required(login_url="login/")
def home(request):
    request.COOKIES['username'] = request.user
    response = render(request, "home.html")
    response.set_cookie('username', request.user)
    return response

def register_user(request):
    args = {}
    if request.method == 'POST':
        # print request.POST
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/todoapp/login')
        else:
            # print form.error_messages
            # print form.non_field_errors
            args['errors'] =  form.errors
    else:
        form = MyRegistrationForm()
    args['form'] = form
    args.update(csrf(request))
    return render(request, 'register.html',args)

##################### REST API #######################################
class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(request, *args, **kwargs)

#################### TODOLIST #####################################
class todolists(CSRFExemptMixin,APIView):

    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    def get(self,request,format=None):
        snippets = Todolist.objects.filter(user=User.objects.get(username=request.user))
        serializer = TodolistSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SingleTodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(username=request.user))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class todolists_detail(CSRFExemptMixin,APIView):

    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    def get_object(self, listid,username):
        try:
            return Todolist.objects.filter(user__username=username).get(pk=listid)
        except Exception as ex:
            raise Http404

    def get(self, request, listid, format=None):
        snippet = self.get_object(listid,request.user)
        serializer = TodolistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, listid, format=None):
        snippet = self.get_object(listid,request.user)
        serializer = SingleTodoSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, listid, format=None):
        snippet = self.get_object(listid,request.user)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

########################### TODOITEM ############################

class todoitems(CSRFExemptMixin,APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    def get(self,request,format=None):
        snippets = Todoitem.objects.filter(todolist__user__username=request.user)
        serializer = TodoitemSerializer(snippets, many=True)
        return Response(serializer.data)

    #No POST, implement post from list/id/item/ post!

class todoitems_detail(CSRFExemptMixin,APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    def get_object(self, itemid,username):
        try:
            return Todoitem.objects.filter(todolist__user__username=username).get(pk=itemid)
        except Exception as ex:
            raise Http404

    def get(self, request, itemid, format=None):
        snippet = self.get_object(itemid,request.user)
        serializer = TodoitemSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, itemid, format=None):
        snippet = self.get_object(itemid,request.user)
        newdata = request.data.copy()
        newdata["todolist"] = snippet.todolist_id
        serializer = TodoitemSerializer(snippet,data=newdata)
        # print serializer
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, itemid, format=None):
        snippet = self.get_object(itemid,request.user)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



###########################################################!!!!!!!!!!!!!
#################### TODOLIST ITEMS #####################################
class items_todolist(CSRFExemptMixin,APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    #validate list to username validation here
    def validate(self,user,listid):
        try:
            Todolist.objects.get(user=User.objects.get(username=user),pk=listid)
        except Exception as ex:
            raise Http404

    def get(self,request,listid,format=None):
        self.validate(request.user,listid)

        snippets = Todoitem.objects.filter(todolist__user__username=request.user).filter(todolist=listid)
        serializer = TodoitemSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request,listid, format=None):
        self.validate(request.user,listid)
        newdata = request.data.copy()
        newdata["todolist"] = listid
        serializer = TodoitemSerializer(data=newdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class items_todolist_detail(CSRFExemptMixin, APIView):
    authentication_classes = [JSONWebTokenAuthentication,SessionAuthentication,BasicAuthentication]
    permission_classes =  [IsAuthenticated]

    #validate list to username validation here
    def validate(self,user,listid):
        try:
            Todolist.objects.get(user=User.objects.get(username=user),pk=listid)
        except Exception as ex:
            raise Http404

    def get_object(self, itemid,username):
        try:
            return Todoitem.objects.filter(todolist__user__username=username).get(pk=itemid)
        except Exception as ex:
            raise Http404

    def get(self, request,listid,itemid, format=None):
        self.validate(request.user, listid)

        snippet = self.get_object(itemid,request.user)
        serializer = TodoitemSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, listid,itemid, format=None):
        self.validate(request.user, listid)

        snippet = self.get_object(itemid,request.user)
        newdata = request.data.copy()
        newdata["todolist"] = listid
        serializer = TodoitemSerializer(snippet, data=newdata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,listid,itemid, format=None):
        self.validate(request.user, listid)

        snippet = self.get_object(itemid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



########################### PRETTY LIST SERIALIZER #######################3
class prettylists(CSRFExemptMixin,APIView):
    authentication_classes = []
    permission_classes =  []
    def get(self,request,format=None):
        snippets = Todolist.objects.all()
        serializer = PrettyListSerializer(snippets, many=True)
        return Response(serializer.data)
