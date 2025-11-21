import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# ================== KEY CỦA MÀY ==================
TELEGRAM_TOKEN = "7987292757:AAHvRB0FlfoGJwCJENf633z0nyjoOplU5gQ"
GEMINI_API_KEY = "AIzaSyCwHDxhI5kvLg69s6hiJ77SZQnPvOfrB1g"
# ================================================

genai.configure(api_key=GEMINI_API_KEY)

# Model sống ngon nhất free tier hiện tại (11/2025)
model = genai.GenerativeModel("gemini-2.5-flash")

user_chats = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Chào boss! 🤖 Gemini 2.5 Flash trợ lý cá nhân siêu nhanh đây!\n"
        "Hỏi gì tao cũng rep ngay lập tức, nhớ hết lịch sử luôn 🔥\n"
        "Giờ tao chạy 24/7 thật rồi nha!"
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
        await update.message.reply_text(f"Gemini lag chút bro: {str(e)}\nThử lại 1-2 phút nha!")

# ================== THÊM ĐOẠN NÀY ĐỂ GIỮ WAKE RENDER FREE ==================
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Gemini Bot đang sống khỏe đây bro! 🤖", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Chạy Flask song song để Render không sleep
threading.Thread(target=run_flask, daemon=True).start()
# =========================================================================

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot đang chạy 24/7 với Gemini 2.5 Flash + không sleep nữa! 🚀")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()