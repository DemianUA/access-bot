from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import datetime
import time

TOKEN = "7620319962:AAFNFAo2T-C1XXam9YFKPDV1QMRUYlB8StI"
CHANNEL_USERNAME = "@CryptoTravelsWithDmytro"
SECRET_LINK = "https://github.com/DemianUA/pharos-scripts"
LOG_FILE = "log.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_time():
        await update.message.reply_text("🕒 Бот спить і працює лише з 08:00 до 02:00. Повертайся пізніше.")
        return

    keyboard = [[InlineKeyboardButton("Отримати посилання", callback_data="getlink")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔐 Щоб отримати доступ — натисни кнопку нижче:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_allowed_time():
        await query.edit_message_text("🕒 Бот спить і працює лише з 08:00 до 02:00. Повертайся пізніше.")
        return

    user_id = query.from_user.id
    username = query.from_user.username or "NoUsername"

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text(f"✅ Ось твоє посилання: {SECRET_LINK}")
        with open(LOG_FILE, "a") as log:
            log.write(f"{user_id} @{username}\n")
    else:
        await query.edit_message_text(f"🚫 Щоб отримати посилання, спочатку підпишись на канал: {CHANNEL_USERNAME}")

async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_time():
        await update.message.reply_text("🕒 Бот спить і працює лише з 08:00 до 02:00. Повертайся пізніше.")
    else:
        await update.message.reply_text("Напиши /start, щоб отримати доступ 😊")

def is_allowed_time():
    now = datetime.datetime.now()
    return now.hour >= 8 or now.hour < 2

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_handler))

# 🔁 Очікування дозволеного часу (з 08:00 до 02:00)
print("⏳ Перевірка часу запуску...")

while True:
    if is_allowed_time():
        print("✅ Час дозволений, запускаємо бота...")
        print("🤖 Bot is polling...")
        app.run_polling()
        break
    else:
        print("🕒 Бот спить (дозволено з 08:00 до 02:00)")
        time.sleep(300)
