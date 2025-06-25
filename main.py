import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import os

# Token and API key from Render Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
PIXELDRAIN_API_KEY = os.getenv("PIXELDRAIN_API_KEY")

logging.basicConfig(level=logging.INFO)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a file and I’ll upload it to PixelDrain.")

# Handle file uploads
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_file = update.message.document or update.message.video or update.message.audio
    if not tg_file:
        await update.message.reply_text("❗ Please send a supported file.")
        return

    file = await tg_file.get_file()
    byte_data = await file.download_as_bytearray()

    # Upload to Pixeldrain
    response = requests.post(
        "https://pixeldrain.com/api/file",
        headers={"Authorization": f"Bearer {PIXELDRAIN_API_KEY}"},
        files={"file": (tg_file.file_name or "file", byte_data)}
    )

    if response.ok:
        file_id = response.json().get("id")
        link = f"https://pixeldrain.com/u/{file_id}"
        await update.message.reply_text(f"✅ Uploaded!\n🔗 {link}")
    else:
        await update.message.reply_text("❌ Upload failed.")

# Bot startup
if __name__ == '__main__':
    print("🚀 Bot starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL, handle_file))
    print("✅ Bot running...")
    app.run_polling()
