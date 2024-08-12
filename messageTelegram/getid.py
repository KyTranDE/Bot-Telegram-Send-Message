from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Mật khẩu đúng cần nhập
PASSWORD = "my_secure_password"

# Hàm lưu trạng thái của người dùng
user_state = {}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Lưu trạng thái rằng người dùng cần nhập mật khẩu
    user_state[update.effective_user.id] = "awaiting_password"
    await update.message.reply_text("Vui lòng nhập mật khẩu:")

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kiểm tra xem bot có đang chờ mật khẩu của người dùng không
    if user_state.get(update.effective_user.id) == "awaiting_password":
        if update.message.text == PASSWORD:
            await update.message.reply_text(f"Mật khẩu chính xác! Group ID là: {update.message.chat_id}")
            # Xóa trạng thái sau khi nhập mật khẩu đúng
            del user_state[update.effective_user.id]
        else:
            await update.message.reply_text("Mật khẩu sai. Vui lòng thử lại.")
    else:
        await update.message.reply_text("Vui lòng sử dụng lệnh /start trước.")




app = ApplicationBuilder().token(
    "7305659457:AAH7iMjozC4D5msQJGKLq3N9FU-Fc8njvds").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_password))

app.run_polling()
