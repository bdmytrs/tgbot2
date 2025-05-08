
import os
import time
import threading
from flask import Flask
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROUP_CHAT_IDS = [
    -4773983672,
    -4628960734,
    # ... до 250
]

def start(update, context):
    update.message.reply_text("Бот работает и готов пересылать сообщения!")

def forward_all(update, context):
    message = update.message

    for group_id in GROUP_CHAT_IDS:
        try:
            if message.text:
                context.bot.send_message(chat_id=group_id, text=message.text)
            elif message.photo:
                context.bot.send_photo(chat_id=group_id, photo=message.photo[-1].file_id, caption=message.caption or '')
            elif message.document:
                context.bot.send_document(chat_id=group_id, document=message.document.file_id, caption=message.caption or '')
            elif message.video:
                context.bot.send_video(chat_id=group_id, video=message.video.file_id, caption=message.caption or '')
            elif message.audio:
                context.bot.send_audio(chat_id=group_id, audio=message.audio.file_id, caption=message.caption or '')
            elif message.voice:
                context.bot.send_voice(chat_id=group_id, voice=message.voice.file_id)
            elif message.sticker:
                context.bot.send_sticker(chat_id=group_id, sticker=message.sticker.file_id)

            time.sleep(0.25)

        except Exception as e:
            print(f"Ошибка при пересылке в {group_id}: {e}")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, forward_all))

    updater.start_polling()
    updater.idle()

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
