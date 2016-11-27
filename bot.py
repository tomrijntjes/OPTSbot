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

POSITION,TEAM_MATE,SCORE,SCORE_CHECK,DEFENDING_OPPONENT,LOSING_SCORE,OFFENDING_OPPONENT=range(7)


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

game = {"blue":{
            "back":"Tom",
            "front":"Ivo",
            "score":10
            },
        "red":{
            "back":"Xia",
            "front":"Matthijs",
            "score":7
        }
    }



def position(bot,update):
    reply_keyboard = [['Red Defense','Red Offense'],['Blue Defense','Blue Offense']]
    update.message.reply_text(
        "Let's register a game :)\n"
        "Send /cancel to stop talking to me.\n\n"
        "Which position did you play?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return TEAM_MATE

def team_mate(bot, update,user_data):
    user = update.message.from_user
    text = update.message.text
    if "blue" in text.lower():
        if "offense" in text.lower():
            user_data["blue"]={"front":user.first_name}
        elif "defense" in text.lower():
            user_data["blue"]={"back":user.first_name}
    elif "red" in text.lower():
        if "offense" in text.lower():
            user_data["red"]={"front":user.first_name}
        elif "defense" in text.lower():
            user_data["red"]={"back":user.first_name}
    else:
        update_message.reply_text('Sorry, that I did not understand. Give it another go!')
        return TEAM_MATE

    reply_keyboard = list(chunks([player for player in s.players if player!=user.first_name],3))
    update.message.reply_text('Okay! Who was on your team?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SCORE


def score(bot,update,user_data):
    text = update.message.text
    if "blue" in user_data:
        if "back" in user_data["blue"]:
            user_data["blue"]["front"]=text
        else:
            user_data["blue"]["back"]=text
    elif "red" in user_data:
        if "back" in user_data["red"]:
            user_data["red"]["front"]=text
        else:
            user_data["red"]["back"]=text
    update.message.reply_text('How many goals did your team score?')

    return SCORE_CHECK

def score_check(bot,update,user_data):
    text = update.message.text
    try:
        score = int(text)
    except ValueError:
        update.message.reply_text("Are you sure that was the score? Try Again please :)")
        return SCORE_CHECK
    if score < 0 or score > 10:
        update.message.reply_text("Are you sure that was the score? Try Again please :)")
        return SCORE_CHECK

    if "blue" in user_data:
        user_data["blue"]["score"]=score
        other_players = [user_data["blue"]["front"],user_data["blue"]["back"]]
    elif "red" in user_data:
        user_data["red"]["score"]=score
        other_players = [user_data["red"]["front"],user_data["red"]["back"]]
    reply_keyboard = list(chunks([player for player in s.players if player not in other_players],3))

    if score == 10:
        update.message.reply_text("Nice, congrats :D How often did the losing team break through?")
        return LOSING_SCORE
    else:
        if "blue" in user_data:
            user_data["red"]={"score":10}
        else:
            user_data["blue"]={"score":10}
        update.message.reply_text("Better luck next time. Who was the defending opponent?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DEFENDING_OPPONENT

def losing_score(bot,update,user_data):
    text = update.message.text
    try:
        score = int(text)
    except ValueError:
        update.message.reply_text("Are you sure that was the score? Try Again please :)")
        return LOSING_SCORE
    if score < 0 or score > 9:
        update.message.reply_text("Are you sure that was the score? Try Again please :)")
        return LOSING_SCORE
    if "blue" in user_data:
        user_data["red"]={"score":score}
        reply_keyboard = list(chunks([player for player in s.players if player!=user_data["blue"]["front"] or player!=user_data["blue"]["back"]],3))
    else:
        user_data["blue"]={"score":score}
        reply_keyboard = list(chunks([player for player in s.players if player!=user_data["red"]["front"] or player!=user_data["red"]["back"]],3))
    update.message.reply_text("That will teach them. Who was the defending player on the opposing team?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return DEFENDING_OPPONENT

def defending_opponent(bot,update,user_data):
    text = update.message.text
    if update.message.from_user.first_name in user_data["blue"]:
        user_data["red"]["back"]=text
        other_players = [text,user_data["blue"]["back"],user_data["blue"]["front"]]
    else:
        user_data["blue"]["back"]=text
        other_players = [text,user_data["red"]["back"],user_data["red"]["front"]]

    reply_keyboard = list(chunks([player for player in s.players if player not in other_players],3))
    update.message.reply_text("Who was the attacking player on the opposing team?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return OFFENDING_OPPONENT

def offending_opponent(bot,update,user_data):
    text = update.message.text
    if update.message.from_user.first_name in user_data["blue"]:
        user_data["red"]["front"]=text
    else:
        user_data["blue"]["front"]=text
    logging.info(user_data)
    if user_data["blue"]["score"]==10:
        winner,loser = "blue","red"  
    else:
        winner,loser = "red","blue"
    update.message.reply_text("{0} (o) and {1} (d) defeated {2} (o) and {3} with 10 to {4}.\n\nIs this information correct?".format(user_data[winner]["front"],user_data[winner]["back"],user_data[loser]["front"],user_data[loser]["back"],user_data[loser]["score"]))
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
        entry_points=[CommandHandler('game', position)],

        states={
            POSITION: [MessageHandler(Filters.text, position,pass_user_data=True)],

            TEAM_MATE: [MessageHandler(Filters.text, team_mate,pass_user_data=True)],

            SCORE: [MessageHandler(Filters.text, score,pass_user_data=True)],

            SCORE_CHECK: [MessageHandler(Filters.text, score_check,pass_user_data=True)],

            DEFENDING_OPPONENT: [MessageHandler(Filters.text, defending_opponent,pass_user_data=True)],

            LOSING_SCORE: [MessageHandler(Filters.text, losing_score,pass_user_data=True)],

            OFFENDING_OPPONENT: [MessageHandler(Filters.text, offending_opponent,pass_user_data=True)],

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