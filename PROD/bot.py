'''
Made with love by Sigmoid.

@author - Păpăluță Vasile (papaluta.vasile@isa.utm.md)
'''

# Importing all needed libraries.
import pickle
import shelve
from norm import TextNormalizer

# Importing NLP related libraries.
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Importing the scikit-learn pipeline attributes.
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MaxAbsScaler

# Importing the chat bot class.
from telebot import telegram_bot

# Defining the pseudo data base.
database = shelve.open('database')

# Loading the model, vectorizer and scaler.
norm = TextNormalizer(stopwords.words('english'),
                      PorterStemmer(),
                      word_tokenize)
svc = pickle.load(open('model.obj', 'rb'))
vectorizer = pickle.load(open('vectorizer.obj', 'rb'))

# Setting up the pipeline.
pipe = Pipeline([('text_normalizer', norm),
                 ('vectorizer', vectorizer),
                 ('svc', svc)])

# Creating the telegram bot.
tbot = telegram_bot(pipeline=pipe,
                    db=database)
update_id = None

# Generating the infinite loop.
while True:
    # Getting the last updates.
    updates = tbot.get_updates(offset=update_id)
    updates = updates['result']

    # If there are any updates then we are going to extract the data from them.
    if updates:
        for item in updates:
            # Getting the data from the last updates.
            update_id = item['update_id']
            try:
                # Trying to extract the text from the updates.
                message = item['message']['text']
            except:
                # If message doesn't have such an attribute, then we set it to None.
                message = None
            if message:
                # If the message has the text content we also extract the chat id, user id and user name.
                chat_id = item['message']['chat']['id']
                user_id = item['message']['from']['id']
                name = item['message']['from']['last_name'] if 'last_name' in item['message']['from'] else item['message']['from']['first_name']

                # Choosing a reply and sending it to the group channel.
                tbot.choose_reply(message, chat_id, user_id, name)
