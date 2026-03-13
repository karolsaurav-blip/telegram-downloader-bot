from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp
import os

TOKEN = "8257319838:AAG0sKBwydHAhUK_74H-9lU3R4iQ191WWNg"

# Start menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
✨ *Welcome to Media Downloader Bot*

📥 Send any video link to download

Bot Creator : @Caethor_bot
"""
    keyboard = [
        [InlineKeyboardButton("📥 Download Guide", callback_data="download")],
        [InlineKeyboardButton("🤖 Create Your Bot", callback_data="createbot")],
        [InlineKeyboardButton("👑 Owner", url="https://t.me/Caethor")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# Button actions
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download":
        await query.edit_message_text(
            "📥 *Send any video link*\n\n"
            "Supported:\n"
            "• YouTube\n"
            "• Instagram\n"
            "• TikTok\n"
            "• Facebook",
            parse_mode="Markdown"
        )

    elif query.data == "createbot":
        await query.edit_message_text(
            "🤖 *Create Your Own Downloader Bot*\n\n"
            "1️⃣ Open @BotFather\n"
            "2️⃣ Use /newbot\n"
            "3️⃣ Copy your bot token\n"
            "4️⃣ Deploy this code on Railway or VPS\n\n"
            "📦 Template repo:\n"
            "https://github.com/",
            parse_mode="Markdown"
        )


# Downloader
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ Downloading...")

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


# App
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot running...")

app.run_polling()
