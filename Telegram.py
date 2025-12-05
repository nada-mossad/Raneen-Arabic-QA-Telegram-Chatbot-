from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

FASTAPI_URL = "http://127.0.0.1:8000/ask"   

TELEGRAM_TOKEN = ""  

def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحباً! أنا مساعد التسوق الخاص بك. اسألني عن أي منتج")


def handle_message(update: Update, context: CallbackContext):
    question = update.message.text 
    response = get_answer_from_fastapi(question)
    update.message.reply_text(response)


def get_answer_from_fastapi(query: str) -> str:
    try:
        response = requests.post(FASTAPI_URL, json={"query": query})
        if response.status_code == 200:
            data = response.json()
            
            if "response" in data:
                return data["response"]
            elif "answer" in data:
                return f"Answer: {data['answer']}\nYou can find it at: {data['product_link']}"
            else:
                return "عذراً، لم أتمكن من فهم صيغة الرد"

        else:
            return "عذراً، لم أتمكن من معالجة طلبك في الوقت الحالي"

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
