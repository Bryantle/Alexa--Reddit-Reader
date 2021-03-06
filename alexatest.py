from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")

def get_headlines():
    user_pass_dict = {'user': "USERNAME",
                      'password': 'PASSWORD',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing the Alexa'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://www.reddit.com/r/worldnews.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i for i in titles])
    return titles

@app.route('/') #app cause we are referencing flask
def homepage():
    return ("hi there, how ya doin")

@ask.launch #ask cause now this is alexa
def start_skill():
    welcome_message = 'Hello there, would you like the news?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headline = get_headlines()
    headline_msg = 'The current world news headlines are {}.'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = "I am not sure why you would ask me then... bye."
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug = True)
