from telegram.ext import Updater, MessageHandler, Filters
from wit import Wit
import ffmpeg
import os

CLIENT = Wit('CN76OWR2WNWJPNRKRRPUOTDZIHHCQ6L3')

def echo(update, context):
    """Echo the user message."""
    print(update)
    audio_oga = context.bot.get_file(update.message.voice).download()
    stream = ffmpeg.input(audio_oga)
    stream = ffmpeg.output(stream, 'audio.wav')
    ffmpeg.run(stream)
    if os.path.exists(audio_oga):
        os.remove(audio_oga)
    audio = open('audio.wav', 'rb')
    text = CLIENT.post_speech(audio)
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
    final_text_json = text['_text']
    update.message.reply_text(final_text_json, reply_to_message_id = update.message.message_id)

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
