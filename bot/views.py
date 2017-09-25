'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''

from django.contrib.auth.models import User as AuthUser
from django.http import HttpResponse
from django.template import loader
from persistence import preferenceHandler
from .models import Cronology, Preference
from .models import User


# Create your views here.
def index(request, chat_id):
    template = loader.get_template('bot/index.html')
    User.objects.update(auth_user_id=request.user.id)
    context = {
        'request': request,
    }
    return HttpResponse(template.render(context, request))

def detail(request, chat_id):
    user = User.objects.get(chat_id=chat_id)
    template = loader.get_template('bot/user.html')
    context = {
        'user': user,
        'request' : request,
    }
    return HttpResponse(template.render(context, request))

def userLogin(request):    
    authUser = AuthUser.objects.get(id=request.user.id)
    chatId = str(request.COOKIES['chatId'])
    user = User.objects.filter(chat_id=chatId)
    user.update(auth_user_id=authUser.id)
    allCronology = Cronology.objects.filter(bot_user=chatId)
    cronology = []
    if len(allCronology) < 20:
        for i in range(0 , len(allCronology)):
            cronology.append(allCronology[i])
    else:
        for i in range(len(allCronology) - 20, len(allCronology)):
            cronology.append(allCronology[i])
    preferences = Preference.objects.filter(bot_user=chatId)
    template = loader.get_template('bot/userLogin.html')
    if request.method == 'POST':
        preferenceHandler.deletePreference(chatId, str(request.POST.get("label", "")))
    context = {
        'botuser': user,
        'user': authUser,
        'request' : request,
        'cronology': cronology,
        'preferences': preferences,
    }
    return HttpResponse(template.render(context, request))
