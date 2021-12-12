import chatbot
import sentiment
import emotion

import logging

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
    ans_sentiment = sentiment.generate(model_sentiment, tokenizer_sentiment, update.message.text)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'{ans_chat}\nClass: {ans_sentiment}')

    logging.info(f'''\nMethod: reply
    Message: {update.message.text}
    Sentiment: {ans_sentiment}.''')


def classify(update: Update, context: CallbackContext):
    '''Bot classifies your message'''
    model_sentiment, tokenizer_sentiment = sentiment.load_model_tokenizer(
        'model_sentiment', 'tokenizer_sentiment')
    ans_sentiment = sentiment.generate(model_sentiment, tokenizer_sentiment, update.message.text)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=ans_sentiment)
