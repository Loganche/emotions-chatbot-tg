import chatbot

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler,
    CallbackContext, MessageHandler,
    Filters
)


# bot answers "Hello $username"
def start(update: Update, context: CallbackContext):
    context.bot.send_message(f'Hello {update.effective_user.first_name}')


# called at unknown command asked
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


# bot answers with model outputs
def reply(update: Update, context: CallbackContext):
    model, tokenizer = chatbot.load_model_tokenizer('model_chat', 'tokenizer_chat')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=chatbot.generate(model, tokenizer, update.message.text))
