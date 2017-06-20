from django.conf.urls import url,include
from django.contrib import admin
from rest_framework_jwt.views import *

from .views import *

urlpatterns = [
    #rest calls
    url(r'^api/token-auth/',obtain_jwt_token),
    url(r'^api/token-refresh/', refresh_jwt_token),
    url(r'^api/token-verify/', verify_jwt_token),
    # url(r'^api/createuser/$', CollegeList.as_view()),
    url(r'^api/lists/$', todolists.as_view()),                           #GET_ALL,#CREATE
    url(r'^api/lists/(?P<listid>[0-9]+)/$', todolists_detail.as_view()),     #UPDATE,DELETE,PUT,GET_LIST

    url(r'^api/items/$', todoitems.as_view()),
    url(r'^api/items/(?P<listid>[0-9]+)/$', todoitems_detail.as_view()),

    url(r'^api/lists/(?P<listid>[0-9]+)/items/$', items_todolist.as_view()),
    url(r'^api/lists/(?P<listid>[0-9]+)/items/(?P<itemid>[0-9]+)/$', items_todolist_detail.as_view()),
    # #
    # list/
    # list/id
    # items/
    # items/id
    # list/id/items/
    # list/id/items/id/
]
