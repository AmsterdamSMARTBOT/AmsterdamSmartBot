![AmsterdamSMARTBOT: Machine learning in Python](https://i.imgur.com/KjrawLzb.png)

# Smart BOT

This chatbot has been developed to be used in Amsterdam smart city environment.
It is based on an interactive conversation with the user.
The specialization is for searching parking and electric charge points in AMSTERDAM.

[![Package Version](https://i.imgur.com/7jjFZ3zb.png)](https://www.python.org/downloads/release/python-352/)

[![Package Version](https://res.cloudinary.com/siftery/image/upload/v1444323049/v1/p/products/django.png)](https://www.djangoproject.com/start/overview/)

[![Package Version](https://i.imgur.com/h8OS44o.jpg)](https://core.telegram.org/)


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


## Installation

work in progress

# Training data

The training data used by the engine is contained in "standard" folder.

At the moment, English training data is in this module. 

# [Home Page](http://amsterdamsmartbot.herokuapp.com/)

View the [documentation](http://chatterbot.readthedocs.io/)
for ChatterBot on Read the Docs.

To build the documentation yourself using [Sphinx](http://www.sphinx-doc.org/), run:

```
sphinx-build -b html docs/ build/
```

# Examples

For examples, see the [examples](https://github.com/gunthercox/ChatterBot/tree/master/examples)
directory in this project's git repository.

There is also an example [Django project using ChatterBot](https://github.com/gunthercox/ChatterBot/tree/master/examples), as well as an example [Flask project using ChatterBot](https://github.com/chamkank/flask-chatterbot).

# History

See release notes for changes https://github.com/gunthercox/ChatterBot/releases

# Development pattern for contributors

1. [Create a fork](https://help.github.com/articles/fork-a-repo/) of
   the [main ChatterBot repository](https://github.com/gunthercox/ChatterBot) on GitHub.
2. Make your changes in a branch named something different from `master`, e.g. create
   a new branch `my-pull-request`.
3. [Create a pull request](https://help.github.com/articles/creating-a-pull-request/).
4. Please follow the [Python style guide for PEP-8](https://www.python.org/dev/peps/pep-0008/).
5. Use the projects [built-in automated testing](http://chatterbot.readthedocs.io/en/latest/testing.html)
   to help make sure that your contribution is free from errors.

# License

ChatterBot is licensed under the [BSD 3-clause license](https://opensource.org/licenses/BSD-3-Clause).