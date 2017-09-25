'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

from django.conf.urls import url
from . import views

#URLs used for the web app
urlpatterns = [
    # /bot/
    url(r'^(?P<chat_id>[0-9]+)/$', views.index, name='index'),
    url(r'^$', views.userLogin, name='userLogin')
]