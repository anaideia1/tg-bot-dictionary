#
# def main():
#     # Initialize the Telegram bot
#     bot = telebot.TeleBot("6788502153:AAGI2mlWU6S1XK3AWZmUE3W5uGEga9clv9E")
#
#
#     @bot.message_handler(commands=['start', 'help'])
#     def send_welcome(message):
#         """
#         This function sends a welcome message to the user when they start the bot.
#         """
#         bot.reply_to(message, "Welcome to the Translation bot! Send me a "
#                               "message and I'll convert it to some language "
#                               "and generate example of pronunciation.")
#         languages_btn = [
#             [
#                 InlineKeyboardButton(lang[1],
#                                      callback_data=lang[0])
#                 for lang in LANGUAGES
#             ]
#         ]
#         languages_keyword = InlineKeyboardMarkup(languages_btn)
#         update.message.reply_text(
#             "Please pick a company", reply_markup=languages_keyword
#         )
#
#     @bot.message_handler(func=lambda message: True)
#     def text_to_speech(message):
#         """
#         This function converts the user's text message to speech and sends it back to the user.
#         """
#         try:
#             # Get the user's message
#             text = message.text
#
#             # Set the language to English by default
#             lang = 'en'
#
#             # Check if the user has specified a language
#             if len(text.split()) > 1 and text.split()[0].lower() == 'lang':
#                 lang = text.split()[1]
#                 text = ' '.join(text.split()[2:])
#
#             # Convert the text to speech
#             trans_client = GCPTranslation(creds=creds)
#             speech_client = GCPTextToSpeech(creds=creds)
#             trans_text, _, _ = trans_client.translate(text=text, target=lang)
#             speech = speech_client.text_to_speech(text=trans_text, lang=lang)
#             bot.send_audio(message.chat.id, speech)
#         except Exception as e:
#             # Log the error
#             print(f"Error: {e}")
#             bot.reply_to(message, "Sorry, I couldn't convert your text to speech. Please try again later.")
#
#     # Start the bot
#     bot.polling()

import os
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from auth import get_credentials_from_file
from translation import GCPTranslation
from text_to_speech import GCPTextToSpeech
from conversation_branches_data import (
    REASONS, LANGUAGES, LANGUAGE_CODES, NATION_DISHES, VOICES, REASONS_ANSWERS,
    VOICES_CODES
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

PURPOSE, TARGET_LANGUAGE, DISHES, LOCATION, BIO, VOICE_GENDER, TRANSLATION = range(7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their purpose."""
    reply_keyboard = [REASONS]

    await update.message.reply_text(
        "Hi! I'm translation bot, so I will hold a small conversation with you"
        " to better undertand your interests and then translate a few phrases "
        "for you. \nSend /cancel to stop talking to me.\n\n"
        "Why are you here?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="What is your purpose?"
        ),
    )

    return PURPOSE


async def purpose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected purpose and asks about target language."""
    user = update.message.from_user
    text = update.message.text
    logger.info("Purpose of %s: %s", user.first_name, update.message.text)

    reply_keyboard = [LANGUAGES]
    await update.message.reply_text(
        f"{REASONS_ANSWERS[text]}\n"
        "I see! What language do you want to translate into?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="What is your target language?"
        ),
    )

    return TARGET_LANGUAGE


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the chosen language and asks for a favorite dishes."""
    user = update.message.from_user
    text = update.message.text
    logger.info("Chosen language of %s: %s", user.first_name, text)
    context.user_data['language'] = text
    context.user_data['language_code'] = LANGUAGE_CODES[text]

    source_text = "It's so beautiful language. It will be pure pleasure to translate to you!"
    creds = get_credentials_from_file()
    trans_client = GCPTranslation(creds=creds)
    trans_text, _, _ = trans_client.translate(
        text=source_text, target=context.user_data['language_code']
    )

    reply_keyboard = [NATION_DISHES[text]]
    await update.message.reply_text(
        f"{trans_text}\n"
        "Gorgeous! Now we proceed to something more interesting "
        "(and also tasty). What's your liking in specified cuisine?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="What is tastiest?"
        ),
    )

    return DISHES


async def dishes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the dishes and ask about location."""
    user = update.message.from_user
    logger.info("Dish of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Nice shot. It's really tasty dish, if made by good chef."
        "So now, when we now each other better, maybe you can tell your "
        "location for us to meet? Or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and asks for a voice gender preferred."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)

    reply_keyboard = [VOICES]
    await update.message.reply_text(
        "OK. So our last question will be..."
        "Which voice would you prefer for speech generation?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="What do you want to hear?"
        ),
    )

    return VOICE_GENDER


async def voice_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    context.user_data['voice_gender'] = VOICES_CODES[update.message.text]
    logger.info("Bio of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text(
        "Thank you! Your telegram dictionary for your needs."
        "Type your phrases for translation.",
        reply_markup=ReplyKeyboardRemove(),

    )

    return TRANSLATION


async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Stores the info about the chosen voice and begin translation.
    This function converts the user's text message to speech and sends it back
    to the user.
    """
    creds = get_credentials_from_file()
    user = update.message.from_user
    text = update.message.text
    lang = context.user_data['language_code']
    voice = context.user_data['voice_gender']
    logger.info("Translation for %s of \'%s\' on %s", user.first_name, text, context.user_data['language'])
    try:
        # Convert the text to speech
        trans_client = GCPTranslation(creds=creds)
        speech_client = GCPTextToSpeech(creds=creds)
        trans_text, _, _ = trans_client.translate(text=text, target=lang)
        speech = speech_client.text_to_speech(text=trans_text, lang=lang, voice=voice)
        await update.message.reply_text(trans_text)
        await update.message.reply_audio(speech)
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        await update.message.reply_text(
            "Ooops... Something happened",
            reply_markup=ReplyKeyboardRemove()
        )

    return TRANSLATION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    application = Application.builder().token(BOT_TOKEN).build()

    # Add conversation handler with the different states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PURPOSE: [MessageHandler(filters.Regex(f"^({'|'.join(REASONS)})$"), purpose)],
            TARGET_LANGUAGE: [MessageHandler(filters.Regex(f"^({'|'.join(LANGUAGES)})$"), language)],
            DISHES: [MessageHandler(filters.TEXT & ~filters.COMMAND, dishes)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            VOICE_GENDER: [MessageHandler(filters.Regex(f"^({'|'.join(VOICES)})$"), voice_gender)],
            TRANSLATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
