from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7620319962:AAFNFAo2T-C1XXam9YFKPDV1QMRUYlB8StI"
CHANNEL_USERNAME = "@CryptoTravelsWithDmytro"
SECRET_LINK = "https://github.com/DemianUA/pharos-scripts"

LOG_FILE = "log.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Отримати посилання", callback_data="getlink")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔐 Щоб отримати доступ — натисни кнопку нижче:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or "NoUsername"

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text(f"✅ Ось твоє посилання: {SECRET_LINK}")
        with open(LOG_FILE, "a") as log:
            log.write(f"{user_id} @{username}\n")
    else:
        await query.edit_message_text(f"🚫 Щоб отримати посилання, спочатку підпишись на канал: {CHANNEL_USERNAME}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("🤖 Bot is polling...")
app.run_polling()
