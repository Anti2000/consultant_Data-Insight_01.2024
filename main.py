from datetime import datetime
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes,  CallbackQueryHandler
from telegram import InlineKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from dotenv import load_dotenv
import openai
import os
from langchain.vectorstores import FAISS

from apps import sqlight
from apps import chatgpt_f
from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation=" 10 MB", compression="zip")


# подгружаем переменные окружения
load_dotenv()

# токен бота
TOKEN = os.getenv('TG_TOKEN')

#TOKEN = os.environ.get("TG_TOKEN_Bible")
GPT_SECRET_KEY = os.environ.get("OPENAI_API_KEY")

# передаем секретный токен chatgpt
openai.api_key = GPT_SECRET_KEY


# функция-обработчик команды /start
async def start(update: Update, context):
    # прикрепляем inline клавиатуру к сообщению
    await update.message.reply_text("Задайте свой вопрос")




# функция-обработчик текстовых сообщений
async def text(update: Update, context):

    # y = await update.message.text()
    question = update.message.text

    id = update.message.from_user.id
    
    
    await update.message.reply_text("Ваш запрос обрабатывается, пожалуйста подождите...\nЗаймет несколько минут")
    system = "Ты эксперт в области электронной коммерции, аналитик, \
        прекрасно разбираешься в технологиях, маркетинге, создании и \
        развитии интернет- магазинов, вопросах лояльности и других, связанных с e-commerce. Не придумывай от себе ничего. Отвечай только по документу."
    content = "Ответь на вопрос клиента"
    b_path = "DBs"
    index_name = "e-commerce"
    # score_threshold = 0.8
    # k = 4
    response = chatgpt_f.answer_index(question, system, content, b_path, index_name)

    id = update.message.from_user.id

    ans = response["message"]
        

       

    ans = response["message"]
    await update.message.reply_text(ans)

    if ans:
        sqlight.record_deal(question, ans, system, content, id)

    
# функция-обработчик команды /data 
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("bingo_email")
    sqlight.data_to_email()


    
    # возвращаем текстовое сообщение пользователю
    await update.message.reply_text('Данные сгружены')


@logger.catch
def main() -> None:

    # создаем приложение и передаем в него токен
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен.')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("data", data, block=False))

     #обработчик текстовых сообщений.
    application.add_handler(MessageHandler(filters.TEXT, text))
    
    


    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()