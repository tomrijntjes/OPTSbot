#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,RegexHandler,ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardHide


from sheet import GoogleSheet
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

s = GoogleSheet(os.environ["SHEET_URL"])

POSITION,TEAM_MATE,OPPONENT_ONE = range(3)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! This is the official Objective Partners table soccer league reporter bot. Write "/leaderboard" to get the latest ranking for the current season!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)

def ranking(bot,update):
    s.update()
    update.message.reply_text(s.get_ranking())
    
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def subscribe(bot,update):
    reply_keyboard = list(chunks(s.players,3))
    update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#conversation handler for registering a game
#position, team mate, opponent one, position, opponent two, color, score



def result(bot,update):
    reply_keyboard = [['Front','Back']]
    update.message.reply_text(
        "Let's register a game :)\n"
        "Send /cancel to stop talking to me.\n\n"
        "Which position did you play?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TEAM_MATE

def team_mate(bot, update):
    reply_keyboard = list(chunks(filter(s.players,lambda p: p!=user.first_name),3))
    user = update.message.from_user
    logger.info("%s played in the %s" % (user.first_name, update.message.text))
    update.message.reply_text('Okay! Who was on your team?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return OPPONENT_ONE

def opponent_one(bot,update):
    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardHide())

    return ConversationHandler.END



def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ["TOKEN"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("leaderboard", ranking))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('result', result)],

        states={
            POSITION: [MessageHandler(Filters.text, position)],

            TEAM_MATE: [MessageHandler(Filters.text, team_mate)],

            OPPONENT_ONE: [MessageHandler(Filters.text, oppont_one)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    
    #get data
    s.update()

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()