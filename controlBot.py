#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import logging
import subprocess, shlex
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

#Scripts
script1="ls -l"
nomscript1="Copia de MakerOnBoard"
descripcio_script1="S'inicia la copia de seguretat"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    keyboard = [[InlineKeyboardButton(nomscript1, callback_data='1')], [InlineKeyboardButton("Option 2", callback_data='2')],[InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Escull l'acció', reply_markup=reply_markup)

    logging.info("Seleccion %s" % (reply_markup))
    
def button(bot, update):
    query = update.callback_query
    
    if query.data == '1' :
        command_line = script1
        args = shlex.split(command_line)
        output=subprocess.check_output(args)  
          
    bot.editMessageText(text="%s" % descripcio_script1,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
    
    bot.sendMessage(chat_id=query.message.chat_id, text=output)
    
def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")

def script(bot, update):
    mensaje='Se incia la copia de seguridad...'
    command_line = 'ls -l'
    args = shlex.split(command_line)
    output=subprocess.check_output(args) 
    #finaltext=" ".join(output)
    #logging.info(output)
    update.message.reply_text(mensaje)
    update.message.reply_text("Listado:")
    update.message.reply_text(output)

def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
updater = Updater("323555779:AAFm6HxcpXupjW3twpGNVLv-9tjeT0nRmt8")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('script', script))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
