import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# Directly put your tokens here (Replace with your actual tokens)
BOT_TOKEN = "1696477109:AAGjp4CaM_9gmOkellZVADTFPqLKFw1P4Ko"
PIXELDRAIN_API_KEY = "2612bc59-1fa9-4f62-9c7d-db233805d4a7"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a file and I’ll upload it to PixelDrain.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_file = update.message.document or update.message.video or update.message.audio
    if not tg_file:
        await update.message.reply_text("❗ Please send a supported file.")
        return

    file = await tg_file.get_file()
    byte_data = await file.download_as_bytearray()

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

if __name__ == '__main__':
    print("🚀 Bot starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL, handle_file))
    print("✅ Bot running...")
    app.run_polling()
