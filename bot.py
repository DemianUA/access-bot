from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7356858534:AAGqrByIqcZw8Rw-2Qg-TDnVLF1i_RWtXZ4"
CHANNEL_USERNAME = "@qrwtehdnhvgfdd"  # Назва каналу

SECRET_LINK = "https://example.com"  # Твоє секретне посилання

async def getlink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status in ["member", "administrator", "creator"]:
        await update.message.reply_text(f"✅ Ось твоє посилання: {SECRET_LINK}")
    else:
        await update.message.reply_text(f"🚫 Щоб отримати посилання, спочатку підпишись на канал: {CHANNEL_USERNAME}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("getlink", getlink))

app.run_polling()
