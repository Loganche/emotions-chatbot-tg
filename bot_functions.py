import chatbot
import sentiment
import emotion

import logging
import numpy as np

from uuid import uuid4
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler,
    CallbackContext, MessageHandler,
    Filters
)


def start(update: Update, context: CallbackContext):
    '''Bot answers "Hello $username"'''

    context.bot.send_message(f'Hello {update.effective_user.first_name}')

    logging.info(f'''\nMethod: start
    Username: {update.effective_user.first_name}''')


def unknown(update: Update, context: CallbackContext):
    '''Called at unknown command asked'''

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

    logging.info(f'''\nMethod: unknown
    Message: {update.message.text}''')


def reply(update: Update, context: CallbackContext):
    '''Bot answers with model outputs'''

    model_chat, tokenizer_chat = chatbot.load_model_tokenizer('model_chat', 'tokenizer_chat')
    ans_chat = chatbot.generate(model_chat, tokenizer_chat, update.message.text)
    ans_chat = ''.join(map(str, ans_chat))

    model_sentiment, tokenizer_sentiment = sentiment.load_model_tokenizer(
        'model_sentiment', 'tokenizer_sentiment')
    _, ans_result = sentiment.generate(
        model_sentiment, tokenizer_sentiment, update.message.text)

    # Generate ID and separate value from command
    key = str(uuid4())
    # Store value
    context.user_data[key] = ans_result

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'{ans_chat}')

    logging.info(f'\nMethod: reply\nMessage: {update.message.text}')


def result(update: Update, context: CallbackContext):
    '''Get results of emotional state'''
    # Берем среднее и округляем значения, а затем сравниваем с классами в отдельной функции
    results = show_res(round(np.mean(list(context.user_data.values()))))

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Your emotional state is {results}')
    # Очищаем БД сообщений, прежде, чем начать снова считать их
    context.user_data.clear()


def show_res(x):
    if x == 0:
        return 'NEGATIVE'
    elif x == 1:
        return 'NEUTRAL'
    else:
        return 'POSITIVE'
