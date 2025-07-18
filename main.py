from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import yt_dlp
import os

import logging
import asyncio
import sys

API_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID", "0"))  # ID المستخدم المصرح له

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(lambda message: "youtube.com/watch" in message.text or "youtu.be/" in message.text)
async def download_youtube_video(message: types.Message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        await message.reply("🚫 هذا البوت خاص.")
        return

    url = message.text.strip()

    await message.reply("⏳ جارٍ تحميل الفيديو، انتظر قليلاً...")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("video.mp4", 'rb') as f:
            await message.reply_video(f, caption="✅ تم تحميل الفيديو")

        os.remove("video.mp4")

    except Exception as e:
        await message.reply(f"❌ حدث خطأ أثناء التحميل:\n{str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp)
