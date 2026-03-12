from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8619546454:AAGyzYhlaHk KPTZbxeXCt_lovSpT8FHe1 3s"

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("📥 Downloading...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            await update.message.reply_video(video=video)

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text("❌ Download failed")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot running...")

app.run_polling()
