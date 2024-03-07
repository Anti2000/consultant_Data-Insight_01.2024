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
    await update.message.reply_text('Выберите направление работы: ', reply_markup=inline_keyboard)


# функция-обработчик нажатий на кнопки
async def button(update: Update, context):

#type hint?????

    # получаем callback query из update
    query = update.callback_query

    language = query.data
    context.chat_data['language']=language 

    
    if language == "Библия":
        # await query.answer('It"s a pop-up notification!')
        await query.edit_message_text(text=f"Вы выбрали: {query.data}\nМожете задать вопрос помощнику!")


   
    elif language == "История христианства":
        # await query.answer('Это всплывающее уведомление!')
        await query.edit_message_text(text=f"Вы выбрали: {query.data}\nМожете задать вопрос помощнику!")

    



# функция-обработчик текстовых сообщений
async def text(update: Update, context):

    # y = await update.message.text()
    question = update.message.text

    language = context.chat_data
    language = language['language']
    id = update.message.from_user.id
    
    
    if language == "Библия":
        await update.message.reply_text("Ваш запрос обрабатывается, пожалуйста подождите...\nЗаймет несколько минут")
        system = "Ты эксперт в области электронной коммерции, аналитик, \
            прекрасно разбираешься в технологиях, маркетинге, создании и \
            развитии интернет- магазинов, вопросах лояльности и других, связанных с e-commerce"
        content = "Ответь на вопрос клиента"
        b_path = "DBs"
        index_name = "db_2024_02"
        score_threshold = 0.8
        k = 4
        response = chatgpt_f.answer_index(question, system, content, b_path, index_name, score_threshold , k)

        id = update.message.from_user.id

        ans = response["message"]
        

   
    elif language == "История христианства":
        await update.message.reply_text("Ваш запрос обрабатывается, пожалуйста подождите...\nЗаймет несколько минут")
        system = "Ты-консультант по Истории Христианства, ответь на вопрос клиента с информацией. Не придумывай ничего от себя. Упоминай источник с точным местом и информацией для ответа клиенту"
        content = "Ответь на вопрос клиента."
        b_path = "DBs"
        index_name = "panfil_history"
        score_threshold = 0.5
        k = 6
        response = chatgpt_f.answer_index(question, system, content, b_path, index_name, score_threshold , k)

       

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

    # добавляем CallbackQueryHandler (только для inline кнопок)
    application.add_handler(CallbackQueryHandler(button))

    #обработчик текстовых сообщений.
    application.add_handler(MessageHandler(filters.TEXT, text))
    
    


    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()