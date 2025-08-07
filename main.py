from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8062303656:AAHXVonWe9gbM5E8Fib5CV6eqtPkP0EKJTg"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.effective_chat.id] = {"step": "name"}
    await update.message.reply_text("Здравствуйте! Введите ваше имя:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if chat_id not in user_data:
        await update.message.reply_text("Пожалуйста, введите /start")
        return

    step = user_data[chat_id]["step"]

    if step == "name":
        user_data[chat_id]["name"] = text
        user_data[chat_id]["step"] = "phone"
        await update.message.reply_text("Введите ваш номер телефона:")
    elif step == "phone":
        user_data[chat_id]["phone"] = text
        user_data[chat_id]["step"] = "message"
        await update.message.reply_text("Теперь введите ваше сообщение:")
    elif step == "message":
        user_data[chat_id]["message"] = text
        summary = user_data[chat_id]
        await update.message.reply_text(
            f"Спасибо! Вот ваша заявка:\n\nИмя: {summary['name']}\nТелефон: {summary['phone']}\nСообщение: {summary['message']}"
        )
        del user_data[chat_id]

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()