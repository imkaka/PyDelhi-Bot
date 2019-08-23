# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
from datetime import datetime
from pytz import timezone
from time import sleep
import logging
import requests
import pytz
import re
import os
import json
import sys
import signal
import subprocess

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will save the process id of the program going in background in a file named 'pid'. Now, when you run you program again, the last one will be terminated with the help of pid. If in case the no process exist with given process id, simply the `pid` file will be deleted and a new one with current pid will be created.  # NOQA
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            logging.error("Terminating previous instance of " +
                          os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token/Key Management Starts---
This part will check for the config.json file which holds the Telegram and Meetup Token/Key and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.  # NOQA
"""
configError = "Please open config.json file located in the project directory and replace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather and similarly for Meetup-API-Key"   # NOQA
if 'config.json' not in os.listdir():
    with open('config.json', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Meetup-API-Key': 0}, f)
        logging.info(configError)
        sys.exit(0)
else:
    with open('config.json', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"] or config["Meetup-API-Key"]:
            logging.info("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
            MeetupAPIKey = config["Meetup-API-Key"]
        else:
            logging.error(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

updater = Updater(token=TelegramBotToken)
dispatcher = updater.dispatcher

utc = pytz.utc

logging.info("I'm On..!!")


def start(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Hi! My powers are solely for the service of PyDelhi Community
Use /help to get /help''')


def mailing_list(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-mailinglist')


def website(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='https://pydelhi.org/')


def irc(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-irc')


def twitter(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-twitter')


def meetup(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://wwww.meetup.com/pydelhi')


def nextmeetup(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    r = requests.get('http://api.meetup.com/pydelhi/events', params=MeetupAPIKey)

    if r.json():
        event_link = r.json()[0].get('link')
        date_time = r.json()[0].get('time', 0) // 1000
        utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
        indian_tz = timezone('Asia/Kolkata')
        date_time = utc_dt.astimezone(indian_tz)
        date_time = date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        venue = r.json()[0].get('venue', {}).get(
            'name', 'Either venue is not set or will be announced later')
        address = r.json()[0].get('venue', {}).get(
            'address_1', 'Either address is not set or will be announced later')
        # bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[0]['venue']['lat'], longitude=r.json()[0]['venue']['lon'])  # NOQA
        city = r.json()[0].get('venue', {}).get(
            'city', 'Either city is not set or will be announced later')
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Address : %s
City : %s
Event Page : %s
''' % (date_time, venue, address, city, event_link))
    else:
        bot.sendMessage(
            chat_id=update.message.chat_id, text="Next meetup hasn't been scheduled yet!")


def nextmeetups(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    r = requests.get('http://api.meetup.com/pydelhi/events', params=MeetupAPIKey)

    if r.json():
        bot.sendMessage(
            chat_id=update.message.chat_id,
            text='''
Next Meetup Schedule/Description
%s
Event Page: %s
''' % (re.sub(r'<[\w/=":.\- ]+>', ' ', r.json()[0].get('description')), r.json()[0].get('link')),
            parse_mode='HTML')

    else:
        bot.sendMessage(
            chat_id=update.message.chat_id, text="Next meetup hasn't been scheduled yet!")


def facebook(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://bit.ly/pydelhi-facebook')


def github(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='http://github.com/pydelhi')


def invitelink(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='''To prevent spamming we have removed invite link from the group,
please ping any one of the admin/moderators of PyDelhi to help you add your friend to the group.''')


def gethelp(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    sleep(0.2)
    bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/mailinglist - to get PyDelhi Mailing List link
/irc - to get a link to Pydelhi IRC channel
/twitter - to get Pydelhi Twitter link
/meetuppage - to get a link to PyDelhi Meetup page
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to PyDelhi Facebook page
/github - to get a link to PyDelhi Github page
/invitelink - to get an invite link for PyDelhi Telegram Group of Volunteers
/help - to see recursion in action

To contribute to|modify this bot : https://github.com/realslimshanky/PyDelhi-Bot
''')


dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('mailinglist', mailing_list))
dispatcher.add_handler(CommandHandler('website', website))
dispatcher.add_handler(CommandHandler('irc', irc))
dispatcher.add_handler(CommandHandler('twitter', twitter))
dispatcher.add_handler(CommandHandler('meetuppage', meetup))
dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextmeetups))
dispatcher.add_handler(CommandHandler('facebook', facebook))
dispatcher.add_handler(CommandHandler('github', github))
dispatcher.add_handler(CommandHandler('invitelink', invitelink))
dispatcher.add_handler(CommandHandler('help', gethelp))

updater.start_polling()
