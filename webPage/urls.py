'''
Created on 28 giu 2017

@author: ROCCO
'''

from django.conf.urls import url
from . import views

#URLs
urlpatterns = [
    url(r'^$', views.home, name='home'),
]

