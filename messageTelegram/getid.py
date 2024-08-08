from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Group ID is: {update.message.chat_id}")

app = ApplicationBuilder().token(
    "7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))

app.run_polling()

# -4206369318
# 7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds

# improt
