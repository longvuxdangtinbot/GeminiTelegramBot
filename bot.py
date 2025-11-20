import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ================== KEY CỦA MÀY ==================
TELEGRAM_TOKEN = "7987292757:AAHvRB0FlfoGJwCJENf633z0nyjoOplU5gQ"
GEMINI_API_KEY = "AIzaSyCwHDxhI5kvLg69s6hiJ77SZQnPvOfrB1g"
# ================================================

genai.configure(api_key=GEMINI_API_KEY)

# Model miễn phí sống 100% tháng 11/2025 (nhanh + thông minh hơn Gemini cũ)
model = genai.GenerativeModel("gemini-2.5-flash")

user_chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Chào boss! 🤖 Gemini 2.5 Flash trợ lý cá nhân siêu nhanh siêu xịn đây!\n"
        "Hỏi gì tao cũng rep ngay lập tức, nhớ hết lịch sử chat luôn 🔥\n"
        "Thử hỏi tao xem sao!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])

    try:
        response = user_chats[user_id].send_message(text)
        reply = response.text

        if len(reply) <= 4096:
            await update.message.reply_text(reply)
        else:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i:i+4096])

    except Exception as e:
        await update.message.reply_text(f"Gemini lỗi tạm thời bro (thường do rate limit): {str(e)}\nThử lại sau 1 phút nha!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot đang chạy với Gemini 2.5 Flash - Sống 100% tháng 11/2025! 🚀")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()