'''
Made with love by Sigmoid.

@author - Păpăluță Vasile (papaluta.vasile@isa.utm.md)
'''
# Importing all needed libraries and modules.
import json
import requests
import random

# Predifined phrases.
greetings = ["Hi"]
farewells = ['Bye', 'Bye-Bye', 'Goodbye', 'Have a good day', 'Stop']
thank_you = ['Thanks', 'Thank you', 'Thanks a bunch', 'Thanks a lot.', 'Thank you very much', 'Thanks so much',
             'Thank you so much']
thank_response = ['You\'re welcome.', 'No problem.', 'No worries.', ' My pleasure.', 'It was the least I could do.',
                  'Glad to help.']

# The telegram bot class.
class telegram_bot:
    def __init__(self, pipeline : 'sklearn.pipeline.Pipeline', db : 'shelve.DbfilenameShelf') -> None:
        '''
            The constructor of the telegram bot.
        :param pipeline: 'sklearn.pipeline.Pipeline'
            The sklearn Pipeline implemented for classifying messages.
        :param db: 'shelve.DbfilenameShelf'
            The data storing object from shelve.
        '''
        # Setting up the token and the url for the bot.
        self.token = '1665743345:AAFYLquDUNvq9R5JMCeRoapqyxX-0ctkz1Y'
        self.url = f"https://api.telegram.org/bot{self.token}"

        # Setting up the pipeline and the pseudo data base.
        self.pipeline = pipeline
        self.db = db

    def choose_reply(self, user_msg : str, chat_id : int, user_id : int, name : str) -> None:
        '''
            This function chooses what function to send.
        :param user_msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        :param user_id: int
            The id of user.
        :param name: str
            The name of the user that send this message.
        '''
        # Checking if message is not a farewell.
        if user_msg not in farewells:

            # If message is a /start command we will sent greeting message.
            if user_msg == '/start':
                bot_resp = f"""Hi! {name}. I am proTexter. \nI'll keep the bad guys out. \nType Bye to Exit."""
                self.send_message(bot_resp, chat_id)
            # If message is a thank you form we wil send to the user a thank you response.
            elif user_msg in thank_you:
                bot_response = random.choice(thank_response)
                self.send_message(bot_response, chat_id)
            # If message is a greeting we will send the user a random greeting back.
            elif user_msg in greetings:
                bot_response = random.choice(greetings)
                self.send_message(bot_response, chat_id)
            # If the text message is nothing above we will verify if it isn't prostitute offer using the pipeline.
            else:
                # Verifying the message.
                (bot_response, state) = self.verify_msg(user_msg, chat_id, user_id, name)

                # Kicking the user is it exceted the number of chances.
                if state == -1:
                    self.kick_user(chat_id, user_id)
                # Sending the last message.
                self.send_message(bot_response, chat_id)
        else:
            # If message si a farewell then we will send bye to the user.
            bot_response = random.choice(farewells)
            self.send_message(bot_response, chat_id)

    def verify_msg(self, user_msg, chat_id, user_id, name):
        '''
            This function chooses finds out using the model.
        :param user_msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        :param user_id: int
            The id of user.
        :param name: str
            The name of the user that send this message.
        '''
        # Getting the prediction from the pipeline.
        prediction = self.pipeline.predict([user_msg])

        # If the text if a prostitute offer that the chatbot will take a point from the user.
        if prediction[0] == 1:
            if f'{chat_id}|{user_id}' in self.db:

                # If the user is present in the data base and has only one point it will be kicked from the chat.
                if self.db[f'{chat_id}|{user_id}'] == 1:
                    return f"dear {name} = you are banned", -1
                else:
                    # If the user has more thant one points the chatbot will take only on point
                    self.db[f'{chat_id}|{user_id}'] -= 1
                    return f"Dear {name} - if you will send {self.db[f'{chat_id}|{user_id}']} more messages like this you will be banned", 1
            else:
                # Adding the user to the data base it it doesnt exists.
                self.db[f'{chat_id}|{user_id}'] = 3
                return f"Dear {name} - you have 2 more chances", 1
        else:
            # If model deosn't detect any prostitute offer nothing happens.
            return "", 1

    def get_updates(self, offset : int =None) -> dict:
        '''
            THis function is getting the last messages in the chat
        :param offset: int
            The offset for requesting the data.
        :return: dict
            The last messages data.
        '''
        url = self.url + "/getUpdates?timeout=100"
        if offset:
            url = url + f"&offset={offset + 1}"
        url_info = requests.get(url)
        return json.loads(url_info.content)

    def send_message(self, msg : str, chat_id : int) -> None:
        '''
            This function allows the chatbot to send messages in the chat.
        :param msg: str
            The user message extracted from the request.
        :param chat_id: int
            The id of the chat.
        '''
        url = self.url + f'/sendMessage?chat_id={chat_id}&text={msg}'
        if msg is not None:
            requests.get(url)

    def kick_user(self, chat_id : int, user_id : int) -> None:
        '''
            This function allows the chatbot to kick a user.
        :param chat_id:
            The id of the chat.
        :param user_id:
            The id of user.
        '''
        url = self.url + f'/kickChatMember?chat_id={chat_id}&user_id={user_id}'
        requests.get(url)
