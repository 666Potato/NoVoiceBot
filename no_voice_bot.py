import os
import logging

import ffmpeg
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters
from wit import Wit

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='logger.log')

load_dotenv()
CLIENT = Wit(os.getenv('WIT_AI_RUSSIAN'))


def echo(update, context):
    """Extract user voice message and convert it to wav for subsequent post request to wit.ai."""
    message = update.message.reply_text('Обработка аудио \U0001F914', reply_to_message_id=update.message.message_id)
    audio_oga = context.bot.get_file(update.message.voice).download()
    filepath = '{0}_{1}.wav'.format(update.message.from_user['first_name'],
                                    update.message.message_id)
    # Run ffmpeg
    (
     ffmpeg
     .input(audio_oga)
     .output('{0}'.format(filepath))
     .run()
    )

    with open(filepath, 'rb') as audio:
        text = CLIENT.post_speech(audio)

    voice_text = text['_text']
    try:
        if voice_text:
            message.edit_text(voice_text)
        else:
            message.reply_text('Пустое голосовое сообщение')
    except Exception:
        os.remove(audio_oga)
        os.remove(filepath)
        update.message.reply_text('Ошибка', reply_to_message_id=update.message.message_id)
        raise ValueError('did not work')

    # Delete temporary files
    if os.path.exists(audio_oga) and os.path.exists(filepath):
        os.remove(audio_oga)
        os.remove(filepath)


def main():
    """Start the bot."""
    updater = Updater(os.getenv('TELEGRAM_KEY'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, echo))
    # Start the Bot
    updater.start_polling()
    # Wait for other requests
    updater.idle()


if __name__ == '__main__':
    main()
