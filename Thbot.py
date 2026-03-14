from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8176980034:AAEhKtBYXsmkMelx9V_5DzWS-egUWROyOuI"

# welcome message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👋 Welcome to Media Downloader Bot

📥 Send any video link to download

🎬 Supported:
YouTube
Instagram
TikTok
Facebook

Creator: @Caethor
"""
    await update.message.reply_text(text)

# downloader
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    await update.message.reply_text("📥 Downloading... Please wait")

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

    except:
        await update.message.reply_text("❌ Download failed")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot running...")

app.run_polling()
