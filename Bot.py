from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8619546454:AAGyzYhIaHkKPTZbxeXCt_IovSpT8FHe13s"

WELCOME_TEXT = """
✨ *Welcome to Ultimate Media Downloader Bot* ✨

📥 *Send any video link and I will download it for you.*

🎬 *Supported Platforms*
• YouTube
• Instagram
• TikTok
• Facebook

🔗 *Drop a link below to start downloading!*

Bot Creator : @Caethor
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ *Downloading your media...*", parse_mode="Markdown")

    ydl_opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            await update.message.reply_video(video=video)

        os.remove(filename)

        await update.message.reply_text("✅ *Download Complete!*", parse_mode="Markdown")

    except:
        await update.message.reply_text("❌ *Download failed. Try another link.*", parse_mode="Markdown")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot running...")

app.run_polling()
