import logging
import chatbot
import bot_functions as bf

from telegram import Update
from telegram.ext import (
    Updater, CommandHandler,
    CallbackContext, MessageHandler,
    Filters
)


TOKEN = '2115383453:AAEIcUSa_R1VP_jomKSlb8bUxOrsYb1vID0'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', bf.start))

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), bf.reply))
    # dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), bf.classify))
    dispatcher.add_handler(MessageHandler(Filters.command, bf.unknown))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
