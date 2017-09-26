<p align="center">
  <img width="256" height="288" src="https://i.imgur.com/KjrawLz.png">
</p>

# Smart BOT


This chatbot has been developed to be used in Amsterdam smart city environment.
It is based on an interactive conversation with the user.
The specialization is for searching parking and electric charge points in AMSTERDAM.


An example of typical input would be something like this:

> **user:** Good morning! How are you doing?  

> **smartBOT:**  Hello and how are you this morning? I'm doing great, how about you?  

> **user:** I'm fine aswell

> **smartBOT:** Glad to hear it 

> **user:** Can you find me the closest parking in Amsterdam?

> **smartBOT:** Yes, I was created to search parkings in Amsterdam

> **smartBOT:** Would you mind shering your location to search the closest parking? ...  

## How it works

The iteration with the chatbot is possible thanks to AIML, Artificial Inteligence Markup Language, an XML dialect for creating natural language.
Through different keywords the service is able to understand and recommend the parking locations asked from the user. 


# Installation

Python version required: 3.5.2
Pypi is suggested to install libraries for the virtual environment
PostgreSQL version recommended: 9.5.6
Heroku version required: Cedar-14 (if you want to migrate in an heroku platform)



## Local Installation

First of all, initialize the local virtual environment:
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

Install all the required libraries through this command:
```
pip install -r requirements.txt
```

Database settings:

Execute these commands to create tables and relations into local database
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Run chatbot script:
```
python main.py
```

Run web application:
```
python manage.py runserver 0.0.0.0:8000
```


## Heroku Installation

```
heroku login
heroku create <nameAPP>
heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:set BUILD_WITH_GEO_LIBRARIES=1
git push heroku master
heroku config:set DISABLE_COLLECTSTATIC=0 
```

Downgrade from HEROKU-16 to CEDAR-14 (GDAL library not supported on Heroku-16):
```
heroku stack:set cedar-14 
git push heroku master
```

Database settings:

First of all, is needed to update database's informations from Heroku Dashboard into the settings.py file. In settings.py modify the dictionary DATABASES with the new informations (Engine, Host, User, Name, Password, Port)

Execute these commands to create tables and relations into heroku database:
```
heroku run python manage.py makemigrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## Training data

The training data used by the engine is contained in "standard" folder.
At the moment, English training data is in this module. 

## [Home Page](http://amsterdamsmartbot.herokuapp.com/)

This is the link to the web page where you can find an explanation about SmartBOT
http://amsterdamsmartbot.herokuapp.com/

# Examples

[![Package Version](https://i.imgur.com/U9kk0KLm.png)](https://i.imgur.com/U9kk0KLm.png)
[![Package Version](https://i.imgur.com/Zz8VxM2m.png)](https://i.imgur.com/Zz8VxM2m.png)
[![Package Version](https://i.imgur.com/keujiv1m.png)](https://i.imgur.com/keujiv1m.png)
[![Package Version](https://i.imgur.com/pvMRukvm.png)](https://i.imgur.com/pvMRukvm.png)

width="256" height="288"
width="100" height="100"

# Technologies

<p>
  


  <a href="http://postgis.net/"><img align="left"  src="https://www.iconattitude.com/icons/open_icon_library/apps/png/256/postgis.png"></a>
  <img align="center"  src="https://nedbatchelder.com/pix/django-icon-256.png" href="https://www.djangoproject.com/start/overview/">
  <img align="right"  src="https://cdn.iconscout.com/public/images/icon/free/png-256/heroku-company-brand-logo-3973db91061d38cd-256x256.png" href="https://www.heroku.com/">
</p>

<p>
  <img align="left"  src="https://mutaz.net/img/icons/android/256/30.png" href="https://core.telegram.org/">
  <img align="center"  src="http://austin.kidsoutandabout.com/sites/default/files/Python_0.png" href="https://www.python.org/downloads/release/python-352/">
  <img align="right"  src="http://www.webantena.net/wp-content/uploads/2016/06/googlemapsapi.png" href="https://enterprise.google.com/intl/en_uk/maps/?utm_source=cpc&utm_medium=google&utm_campaign=2016-geo-emea-endor-gmedia-search-gb-homepage&utm_content=gb%7Cen%7Chybr%7C1001878%7C%7Cbk%7Cbrand%7C%7Chomepage&ds_lpt_start=&ds_lpt_end=&gclid=EAIaIQobChMIhbTnv6_D1gIVQuEbCh1lCQzQEAAYASAAEgLZ6vD_BwE&dclid=CN3WmcGvw9YCFdiLUQodmxIDmQ">
</p>

