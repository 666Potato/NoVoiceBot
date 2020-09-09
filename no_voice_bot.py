import os

import ffmpeg
from telegram.ext import Updater, MessageHandler, Filters
from wit import Wit


CLIENT = Wit('CN76OWR2WNWJPNRKRRPUOTDZIHHCQ6L3')


def echo(update, context):
    """Extract user voice message and convert it to wav for subsequent post request to wit.ai."""
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
    update.message.reply_text(voice_text, reply_to_message_id=update.message.message_id)

    # Delete temporary files
    if os.path.exists(audio_oga) and os.path.exists(filepath):
        os.remove(audio_oga)
        os.remove(filepath)


def main():
    """Start the bot."""
    updater = Updater("1260098169:AAFB855CpwQwcSn4c9fjTKjkNIcCtUX8IYk", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, echo))
    # Start the Bot
    updater.start_polling()
    # Wait for other requests
    updater.idle()


if __name__ == '__main__':
    main()
