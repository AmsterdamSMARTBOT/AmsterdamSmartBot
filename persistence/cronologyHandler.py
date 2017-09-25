'''
Created on 06 giu 2017

@author: ROCCO - GERARDO
'''
import datetime

from bot.models import User, Cronology, Preference

def createCronology(bot, update, user):
    cronology = Cronology()
    cronology.bot_user = user
    cronology.command = user.lastCommand
    cronology.date = datetime.datetime.now()
    cronology.save()