from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import datetime
import time

# ==== Налаштування ====
TOKEN = "7620319962:AAFNFAo2T-C1XXam9YFKPDV1QMRUYlB8StI"
CHANNEL_USERNAME = "@CryptoTravelsWithDmytro"
SECRET_LINK = "https://github.com/DemianUA/pharos-scripts"

# ==== Перевірка часу ====
def is_allowed_time():
    now = datetime.datetime.now()
    return now.hour >= 8 or now.hour < 2  # з 08:00 до 02:00

# ==== /start ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_time():
        await safe_reply(update, "🕒 Бот працює з 08:00 до 02:00. Повертайся пізніше.")
        return

    keyboard = [[InlineKeyboardButton("Отримати посилання", callback_data="getlink")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await safe_reply(update, "🔐 Натисни кнопку нижче, щоб отримати доступ:", reply_markup)

# ==== Обробка кнопки ====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_allowed_time():
        await query.edit_message_text("🕒 Бот працює з 08:00 до 02:00. Повертайся пізніше.")
        return

    user_id = query.from_user.id
    username = query.from_user.username or "NoUsername"

    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)

    if member.status in ["member", "administrator", "creator"]:
        await query.edit_message_text(f"✅ Ось твоє посилання: {SECRET_LINK}")
        print(f"[✅] {user_id} @{username} отримав доступ")
    else:
        await query.edit_message_text(f"🚫 Спочатку підпишись на канал: {CHANNEL_USERNAME}")

# ==== Обробка всього іншого ====
async def fallback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed_time():
        await safe_reply(update, "🕒 Бот працює з 08:00 до 02:00. Повертайся пізніше.")
    else:
        await safe_reply(update, "Напиши /start, щоб отримати доступ 🙂")

# ==== Безпечна відповідь ====
async def safe_reply(update: Update, text: str, reply_markup=None):
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text)

# ==== Запуск ====
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_handler))

print("⏳ Перевірка часу запуску...")

while True:
    if is_allowed_time():
        print("✅ Час дозволений, запускаємо бота...")
        print("🤖 Bot is polling...")
        app.run_polling()
        break
    else:
        print("🕒 Зараз бот спить (08:00–02:00). Перевірка знову через 5 хв...")
        time.sleep(300)
