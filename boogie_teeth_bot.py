from io import open
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from telegram.utils.helpers import escape_markdown
from uuid import uuid4
import os
import logging
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

images = []

def teeth(update, context):
    """
    Callback for when the /teeth command is used
    Selects a random teeth image and replies
    """
    global images
    index = random.randint(0, len(images)-1)
    image = images[index]
    with open(image, 'rb') as img:
        update.message.reply_photo(photo=img)

def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Caps",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Bold",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Italic",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN))]

    update.inline_query.answer(results)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start_bot():
    TOKEN = os.environ["TELEGRAM_API_TOKEN"]
    PORT = os.environ.get('PORT')
    NAME = "boogie-teeth-bot"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("teeth", teeth))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    logger.info("Bot starting...")

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))

    logger.info("Bot started successfully")
    updater.idle()

def index_images():
    global images
    root = os.path.dirname(__file__)
    directory = os.path.join(root, "images")
    images = [os.path.join(directory, f) for f in os.listdir(directory)]
    logger.debug("Found {} image files".format(len(images)))

def main():
    index_images()
    start_bot()

if __name__ ==  "__main__":
    main()