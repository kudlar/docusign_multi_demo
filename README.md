# Multiple Documents and AutoPlace Fields--Python recipe
This directory includes the source for the Python Multiple Documents and AutoPlace Field recipes and enables it to be run on a free Heroku server.

The /app directory holds the complete example

The top level files are used to manage and configure the example on [Heroku](https://www.heroku.com/).

## Run the recipe on Heroku
The recipe source, as is, works on the [Heroku](https://www.heroku.com/) using the free service level. No credit card needed!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Click the Deploy button, then enter your DocuSign Developer Sandbox credentials on the form in the Heroku dashboard. Then press the View button at the bottom of the dashboard screen when it is enabled by the dashboard.

## Run the recipe on your own server

### Get Ready
Your server needs Python 2.7 or later

You need an email address and password registered with the free DocuSign Developer Sandbox system. You also need a free Integration Key for your DocuSign developer account. See the [DocuSign Developer Center](https://www.docusign.com/developer-center) to sign up.

### How to do it
```sh
% pip install -r requirements.txt
% python run.py
```

