'''
Created on 24 mar 2017

@author: Gerardo - Rocco
'''

import atexit
import json
import logging
import os
import sys
import urllib
import django
import telegram
import googlemaps
import requests
import aimlHandler
from builtins import str
from threading import Timer
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.keyboardbutton import KeyboardButton

TOKEN = "326681466:AAF-FhP762y8CwaxIKsGrB7MIQUXRZZoZKo"
gmaps = googlemaps.Client(key='AIzaSyCHw4CGzrZOpOleKM3KCPPMI7jJV_MDkDI')
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
WEBAPP = "145.94.191.66:8000/accounts/login"
TUTORIAL = "145.94.191.66:8000"
choosenPosition = ''
lastUpdate = ""

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
kernel = aimlHandler.initializeBot()

#the method sets the timer to ping the HEROKU server to keep it up 
class Repeat(object):
    count = 0
    @staticmethod
    def repeat(rep, delay, func):
        "repeat func rep times with a delay given in seconds"

        if Repeat.count < rep:
            # call func, you might want to add args here
            func()
            Repeat.count += 1
            # setup a timer which calls repeat recursively
            # again, if you need args for func, you have to add them here
            timer = Timer(delay, Repeat.repeat, (rep, delay, func))
            # register timer.cancel to stop the timer when you exit the interpreter
            atexit.register(timer.cancel)
            timer.start()

#the method ping the HEROKU server
def pingHeroku():
    urllib.request.urlopen("https://amsterdamsmartbot.herokuapp.com/").read()

#the method manages the telegram's command /start
def start(bot, update, args, chat_data):
    name = update.message.from_user["first_name"]
    surname = update.message.from_user["last_name"]
    utente = User()
    utente.name = name
    utente.surname = surname
    utente.lastCommand = "start"
    utente.chat_id = update.message.chat_id
    utente.save()
    settings.USER = utente.chat_id
    cronologyHandler.createCronology(bot, update, utente)
    parking_keyboard = KeyboardButton(text="Can you find me a parking?")
    chargePoint_keyboard = KeyboardButton(text="Can you find me a electric charge point?")
    custom_keyboard = [[ parking_keyboard],[chargePoint_keyboard]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    global lastUpdate 
    lastUpdate= str(update.update_id)
    update.message.reply_text('Hi ' + name + ' ' + surname + ', I\'m Smartbot!')
    bot.sendMessage(chat_id = update.message.chat_id, text="How can i help you?", reply_markup=reply_markup)
    geometryHandler.loadJSON()

#the method manages specific keywords for AIML 
def talk(bot, update):
    global kernel
    botActived = userHandler.getUserBotActived(update.message.chat_id)
    if botActived:
        bot.sendMessage(chat_id=update.message.chat_id, text = kernel.respond(update.message.text))
        if 'Yes i was created to search parkings in Amsterdam' in kernel.respond(update.message.text): 
            userHandler.setUserBotActived(update.message.chat_id, False)
            parkingHandler.parking(bot, update)
        elif 'Yes i was created to search electric charge points in Amsterdam' in kernel.respond(update.message.text): 
            userHandler.setUserBotActived(update.message.chat_id, False)
            electricChargePointHandler.chargePoint(bot, update)
        elif 'Use the following link to access your profile' in kernel.respond(update.message.text): 
            userHandler.setUserBotActived(update.message.chat_id, False)
            profile(bot, update) 
        elif 'Use the following link to open the home page' in kernel.respond(update.message.text): 
            userHandler.setUserBotActived(update.message.chat_id, False)
            homePage(bot, update)
        elif 'Use the following link to open tutorial page' in kernel.respond(update.message.text): 
            userHandler.setUserBotActived(update.message.chat_id, False)
            print("WE ARE IN TUTORIAL AIML")
            tutorial(bot, update)
    else:
        analyzeText(bot, update)

#the method manages the telegram's command /profile
def profile(bot, update):
    user = userHandler.getUser(update.message.chat_id)
    userHandler.setUserLastCommand(update.message.chat_id, "webappUser")
    cronologyHandler.createCronology(bot, update, user)
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<a href="' + WEBAPP + '?chatId=' + str(update.message.chat_id) + '">User Cronology</a>', 
                    parse_mode=telegram.ParseMode.HTML)
    userHandler.setUserBotActived(update.message.chat_id, True)
    
def homePage(bot, update):
    user = userHandler.getUser(update.message.chat_id)
    userHandler.setUserLastCommand(update.message.chat_id, "Home Page")
    cronologyHandler.createCronology(bot, update, user)
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<a href="' + TUTORIAL +  '">Open Home Page</a>', 
                    parse_mode=telegram.ParseMode.HTML)
    userHandler.setUserBotActived(update.message.chat_id, True)

#the method manages the telegram's command /tutorial   
def tutorial(bot, update):
    user = userHandler.getUser(update.message.chat_id)
    userHandler.setUserLastCommand(update.message.chat_id, "Tutorial")
    cronologyHandler.createCronology(bot, update, user)
    bot.sendMessage(chat_id=update.message.chat_id, 
                    text='<a href="' + TUTORIAL +  '">Open Tutorial</a>', 
                    parse_mode=telegram.ParseMode.HTML)
    userHandler.setUserBotActived(update.message.chat_id, True)
      
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

#the method gets user's GPS location
def getLocation(bot, update):
    latid = update.message.location["latitude"]
    long = update.message.location["longitude"]
    userHandler.setUserLatLong(update.message.chat_id, latid, long)
    reverse_geocode_result = gmaps.reverse_geocode((latid, long))
    name = update.message.from_user["first_name"]
    message = name + " you are located in: " + reverse_geocode_result[0]['formatted_address']
    bot.sendMessage(chat_id=update.message.chat_id, 
                        text = message)
    utente = userHandler.getUser(update.message.chat_id)
    if utente.lastCommand == "parking":
        showKeyboardTypeOfParking(bot, update)
    elif utente.lastCommand == "chargePoint":
        electricChargePointHandler.location(bot, update)
  
  
def showKeyboardTypeOfParking(bot,update):
    user = userHandler.getUser(update.message.chat_id)
    buttonPrivateParking = KeyboardButton(text="Private Parking")
    buttonStreetParking = KeyboardButton(text="Street Parking")
    custom_keyboard = [[buttonStreetParking],[buttonPrivateParking]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard , resize_keyboard=True,one_time_keyboard=True) 
    bot.sendMessage(chat_id=update.message.chat_id , text="Can you choose the parking's type ?" , reply_markup = reply_markup)
    userHandler.setUserLastCommand(update.message.chat_id, "parking.type")
    
#the method manages specific texts received from the user 
def analyzeText(bot, update):
    utente = userHandler.getUser(update.message.chat_id)
    address = ''
    if utente.lastCommand == 'start':
        textToAnalyze = update.message.text
        if textToAnalyze=='Find me the closest Parking':
            parkingHandler.parking(bot, update)
    elif utente.lastCommand == "parking":
        textToAnalyze = update.message.text
        if preferenceHandler.checkPreferences(utente, textToAnalyze, bot, update):
            preference = preferenceHandler.getSinglePreference(utente, textToAnalyze)
            userHandler.setUserLatLong(update.message.chat_id, preference.lat, preference.lon)
            showKeyboardTypeOfParking(bot,update)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text = "Please insert the location you want to start")
            choosenPosition = update.message.text
            newCommand = utente.lastCommand + ".preference"
            userHandler.setUserLastCommand(update.message.chat_id, newCommand)
    elif utente.lastCommand == "parking.type":
        textToAnalyze = update.message.text
        if textToAnalyze == "Private Parking":
            parkingHandler.location(bot, update)
        elif textToAnalyze == "Street Parking":
            parkingStreetHandler.location(bot, update)
    elif utente.lastCommand == "chargePoint":
        textToAnalyze = update.message.text
        if preferenceHandler.checkPreferences(utente, textToAnalyze, bot, update):
            preference = preferenceHandler.getSinglePreference(utente, textToAnalyze)
            userHandler.setUserLatLong(update.message.chat_id, preference.lat, preference.lon)
            electricChargePointHandler.location(bot, update)
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text = "Please insert the location you want to start")
            choosenPosition = update.message.text
            newCommand = utente.lastCommand + ".preference"
            userHandler.setUserLastCommand(update.message.chat_id, newCommand)
    elif utente.lastCommand == "parking.preference":
            textToAnalyze = update.message.text
            geocode_result = gmaps.geocode(textToAnalyze)
            if geocode_result:
                userHandler.setUserPositionName(update.message.chat_id, textToAnalyze)
                preferenceHandler.savePreferences(bot, update)
            else:
                message = "I couldn't find this location. \nType again"
                bot.sendMessage(chat_id=update.message.chat_id, text = message )
    elif utente.lastCommand == "chargePoint.preference":
            textToAnalyze = update.message.text
            geocode_result = gmaps.geocode(textToAnalyze)
            if geocode_result:
                userHandler.setUserPositionName(update.message.chat_id, textToAnalyze)
                preferenceHandler.savePreferences(bot, update)
            else:
                message = "I couldn't find this location. \nType again"
                bot.sendMessage(chat_id=update.message.chat_id, text = message )
    elif utente.lastCommand == "parking.result":
        print("sono nel parking.result")
        user = userHandler.getUser(update.message.chat_id)
        parkingHandler.parkingResult(bot, update)
    elif utente.lastCommand == "chargePoint.result":
        user = userHandler.getUser(update.message.chat_id)
        electricChargePointHandler.chargePointResult(bot, update)
    elif (utente.lastCommand == "parking.preference.choose") or (utente.lastCommand == "chargePoint.preference.choose"):
        textToAnalyze = update.message.text
        user = userHandler.getUser(update.message.chat_id)        
        geocode_result = gmaps.geocode(user.positionName)
        if geocode_result:
            address = geocode_result[0]['formatted_address']
            message = "You inserted this location " + address
            latid = geocode_result[0]['geometry']['location']['lat']
            long = geocode_result[0]['geometry']['location']['lng']
            userHandler.setUserLatLong(update.message.chat_id, latid, long)
            if textToAnalyze == "YES":
                bot.sendMessage(chat_id=update.message.chat_id, text = "Choose the name you want to save this position: " )
                newCommand = utente.lastCommand + ".save"
                userHandler.setUserLastCommand(update.message.chat_id, newCommand)
            elif textToAnalyze == "NO":
                if "parking" in utente.lastCommand :
                    newCommand = "parking.type"
                    userHandler.setUserLastCommand(update.message.chat_id, newCommand)
                    user = userHandler.getUser(update.message.chat_id)
                    showKeyboardTypeOfParking(bot, update)
                elif "chargePoint" in utente.lastCommand :
                    newCommand = "chargePoint.result"
                    userHandler.setUserLastCommand(update.message.chat_id, newCommand)
                    user = userHandler.getUser(update.message.chat_id)
                    electricChargePointHandler.chargePointResult(bot, update)
                    
        else:
            message = "I couldn't find this location. \nType again"
            bot.sendMessage(chat_id=update.message.chat_id, text = message )
    elif (utente.lastCommand == "parking.preference.choose.save") or (utente.lastCommand == "chargePoint.preference.choose.save"):
        textToAnalyze = update.message.text
        bot.sendMessage(chat_id=update.message.chat_id, text = "The current position has been saved with the name: " + textToAnalyze)
        user = userHandler.getUser(update.message.chat_id)
        if "parking" in utente.lastCommand :
            newCommand = "parking.type"            
            userHandler.setUserLastCommand(update.message.chat_id, newCommand)
            preferenceHandler.createPreference(textToAnalyze, user, address)
            showKeyboardTypeOfParking(bot, update)
        elif "chargePoint" in utente.lastCommand :
            newCommand = "chargePoint.result"
            userHandler.setUserLastCommand(update.message.chat_id, newCommand)
            preferenceHandler.createPreference(textToAnalyze, user, address)
            electricChargePointHandler.chargePointResult(bot, update)        
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text = "I couldn't understand you" )
        
def check(bot, update):
    point = Point(4.904444, 52.348712)
    obj = multiPolygonHandler.getMultiPolygonByPoint(point)
    
#the method initializes the chatbot
def run():
    updater = Updater(TOKEN)
    Repeat.repeat(100000000000, 600, pingHeroku)
    choosenPosition = 'posizione'
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_args=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("parking", parkingHandler.parking))
    dp.add_handler(CommandHandler("chargepoint", electricChargePointHandler.chargePoint))
    dp.add_handler(CommandHandler("talk", talk))
    dp.add_handler(CommandHandler("profile", profile))
    dp.add_handler(CommandHandler("tutorial", tutorial))
    dp.add_handler(MessageHandler([Filters.location], getLocation))
    dp.add_handler(MessageHandler([Filters.text], talk))
    dp.add_handler(CallbackQueryHandler(get_inlineKeyboardButton, pass_chat_data=True))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()   
    
    
def get_inlineKeyboardButton(bot, update, chat_data):
    query = update.callback_query
    chat_id = update['callback_query']['message']['chat']['id']
    utente = userHandler.getUser(chat_id)
    if "parking" in utente.lastCommand:
        parkingHandler.sendMessageForSingleParking(bot, query, query.data)
    elif "chargePoint" in utente.lastCommand:
        electricChargePointHandler.sendMessageForSingleChargePoint(bot, query, query.data)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartBot.settings')
    django.setup() 
    from bot.models import User, Preference, Cronology
    from dataset import parkingHandler, electricChargePointHandler, geometryHandler ,parkingStreetHandler
    from persistence import cronologyHandler, preferenceHandler, userHandler, multiPolygonHandler
    run()