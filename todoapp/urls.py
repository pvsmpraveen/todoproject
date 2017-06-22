from django.conf.urls import url,include
from django.contrib import admin
from rest_framework_jwt.views import *

from views import *
from django.contrib.auth import views
from .forms import LoginForm

urlpatterns = [
    #rest calls
    url(r'^$', home, name='home'),

    url(r'^api/token-auth/',obtain_jwt_token),
    url(r'^api/token-refresh/', refresh_jwt_token),
    url(r'^api/token-verify/', verify_jwt_token),
    # url(r'^api/createuser/$', CollegeList.as_view()),

    url(r'^api/prettylists/$', prettylists.as_view()),


    url(r'^api/lists/$', todolists.as_view()),                           #GET_ALL,#CREATE
    url(r'^api/lists/(?P<listid>[0-9]+)/$', todolists_detail.as_view()),     #UPDATE,DELETE,PUT,GET_LIST

    url(r'^api/items/$', todoitems.as_view()),
    url(r'^api/items/(?P<itemid>[0-9]+)/$', todoitems_detail.as_view()),

    url(r'^api/lists/(?P<listid>[0-9]+)/items/$', items_todolist.as_view()),
    url(r'^api/lists/(?P<listid>[0-9]+)/items/(?P<itemid>[0-9]+)/$', items_todolist_detail.as_view()),

    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm,'redirect_authenticated_user':True},name="loginn"),
    url(r'^logout/$', views.logout, {'next_page': '/todoapp/login'},name="logoutt"),
    url(r'^register/$',register_user,name="registerr"),
]
