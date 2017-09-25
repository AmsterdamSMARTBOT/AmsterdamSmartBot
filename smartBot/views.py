'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User as AuthUser
from bot.models import User
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.context import RequestContext

#View Home
def home(request):
    template = loader.get_template('login.html')
    chatId = request.GET.get('chatId', '')
    settings.USER = chatId
    request.session['chatId'] = chatId
    context = {
        'request': request,
    }
    return HttpResponse(template.render(context, request))

#View accountLogin
def accountLogin(request):
    template = loader.get_template('login.html')
    chatId = request.GET.get('chatId', '')
    context = {
        'request': request,
    }
    response = HttpResponse(template.render(context, request))
    response.set_cookie('chatId', chatId)
    return response

#View accountLogout
def accountLogout(request):
    template = loader.get_template('login.html')
    chatId = settings.USER 
    context = {
        'request': request,
    }
    return HttpResponse(template.render(context, request))