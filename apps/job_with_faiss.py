from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
import time
import re
import requests
import openai
import tiktoken
from dotenv import load_dotenv
from loguru import logger
# import matplotlib.pyplot as plt
from langchain.docstore.document import Document# Получение ключа API от пользователя и установка его как переменной окружения

start_time = time.time()

# получим переменные окружения из .env
load_dotenv()
# API-key
openai.api_key = os.environ.get("OPENAI_API_KEY")


# функция для загрузки документа по ссылке из гугл драйв
def load_document_text(url: str) -> str:
    # Extract the document ID from the URL
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    # doc_id = match_.group(1)
    doc_id = "1-0HEvLDRUA-gm40xVSRjce6_Js3gF0zX"

    # Download the document as plain text
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    text = response.text

    return text


def duplicate_headers_without_hashes(text):
    """
    Дублирует заголовки в тексте, убирая из дубликатов хэши.

    Например:
    '# Заголовок' превращается в:
    '# Заголовок
    Заголовок'
    """

    # Вспомогательная функция, которая будет вызываться для каждого найденного совпадения в тексте
    def replacer(match):
        # match.group() вернет найденный заголовок с хэшами.
        # затем мы добавляем к нему перенос строки и ту же строку, но без хэшей
        return match.group() + "\n" + match.group().replace("#", "").strip()

    # re.sub ищет в тексте все заголовки, начинающиеся с 1 до 3 хэшей, и заменяет их
    # с помощью функции replacer
    result = re.sub(r'#{1,3} .+', replacer, text)

    return result


def open_files(files_name):
    with open(files_name, 'r', encoding='utf-8') as f:
        print(f'{"-reading files-"}')
        # lines = len(f.readlines())
        # return f.readlines()
        return f.read()



def write_files(data, files_name:str='PreachersHelperBot/fastapi/bible.txt') -> None:
    with open(files_name, 'w', encoding='utf-8') as f:
        f.write(data)



def split_text(text):
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    fragments = markdown_splitter.split_text(text)


    return fragments

def make_chunks(doc, sep:str=" ", ch_size:int=1024):
    
    print(f'{"-making chunks-"}')

    # создаем список чанков
    source_chunks = []
    splitter = CharacterTextSplitter(separator=sep, chunk_size=ch_size)
    for chunk in splitter.split_text(doc):
        source_chunks.append(Document(page_content=chunk, metadata={}))
        
    return source_chunks


def making_em_db(source_chunks):
    embeddings = OpenAIEmbeddings()
    print(f'{"-point-"}')

    # Создадим индексную базу из разделенных фрагментов текста
    db = FAISS.from_documents(source_chunks, embeddings)
    print(f'{"-making faiss db-"}')
    return db


def add_text_em_db(db, text):
#     documents = [Document(page_content=text, metadata={})]
#     added_ids = db.add_documents(documents)

    # ids = db.add_texts(["Пример текста 1", "Пример текста 2"], metadatas=[{"author": "user1"}, {"author": "user2"}])
    # # text = str(text)
    # print(type(text))
    added_ids = db.add_documents(text)
    print(added_ids)
    # input("stopping")

    # ids = db.add_texts([text])

    # db.add_texts(text)
    return db



def saving_em_db(db, folder_path="DBs", b_name="db_"):
      
    # Теперь вы можете сохранить файл напрямую в Google Drive
    # folder_path  = "DBs"
    print(f'{"-point-"}')


    # Задаем имя, чтобы идентифицировать сохраненные файлы
    index_name = b_name

    # сохраняем db_from_texts на ваш гугл драйв
    db.save_local(folder_path=folder_path, index_name=index_name)
    print(f'{"-saving db-"}')



def open_em_db(index_name, folder_path):
    
    # Путь к папке, где сохранены файлы индекса и хранилища документов
    # folder_path = "DBs"  
    # b_gpt/DBs/db_from_texts_PP5.pkl

    # Инициализирум модель эмбеддингов
    embeddings = OpenAIEmbeddings()

    # Имя, используемое при сохранении файлов
    # index_name = "db_from_texts_PP4"

    # Загрузка данных и создание нового экземпляра FAISS
    faiss_instance = FAISS.load_local(
        folder_path=folder_path,
        embeddings=embeddings,
        index_name=index_name
    )

    return faiss_instance



def insert_newlines(text: str, max_len: int = 170) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_len:
            lines.append(current_line)
            current_line = ""
        current_line += " " + word
    lines.append(current_line)
    return " ".join(lines)



def answer_index(db, topic, system, content, verbose=1, score_threshold = 0.6, k=4):

    # try:
            # docs = seach_relavent_text(search_index, topic)

    # docs = db.similarity_search(topic, k=4)
    docs = db.similarity_search_with_relevance_scores(topic, k, score_threshold=score_threshold)
    message_content = ""

    for doc, similarity_score in docs:
        print(f"Document: {doc.page_content}, Similarity Score: {similarity_score}")
        message_content = message_content + doc.page_content
        print("-----------")

#      UserWarning: No relevant docs were retrieved using the relevance score threshold 0.75
#   warnings.warn(
    
    # # if verbose: print('\n ===========================================: ')
    # message_content = re.sub(r'\n{2}', ' ', '\n '.join([f'\n\n=====================' + doc.page_content + '\n' for i, doc in enumerate(docs)]))
    # if verbose: print('message_content :\n ======================================== \n', message_content)
 

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"{content} информация для ответа клиенту: {message_content}\n\nВопрос клиента: \n{topic}"}
    ]

    if verbose: print('\n ===========================================: ')

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4-turbo-preview",
        # model="gpt-4-0125-preview",
        messages=messages,
        temperature=0
    )
    # answer = insert_newlines(completion.choices[0].message.content)
    answer = completion.choices[0].message.content
    print(answer)
# except:
    # answer = "Перефразируйте пожалуйста вопрос."
    # print("Something else went wrong")
    # logger.info(answer)
    return {"message": answer, "system": system, "content": content}  # возвращает ответ



def seach_relavent_text(db, query):
    # query = input("введите вопрос: ")

    k = 4  # мы хотим получить до 5 результатов
    score_threshold = 0.75  # мы хотим видеть только документы, релевантность которых не менее 0.75

    # Применяем метод поиска
    results = db.similarity_search_with_relevance_scores(query, k, score_threshold=score_threshold)
    # docs = db.similarity_search(query, k=4) 
 
    # Выведем результаты
    for doc, similarity_score in results:
        print(f"Document: {doc.page_content}, Similarity Score: {similarity_score}")
        print("-----------")
    


def summarize_questions(dialog):
    """
    Функция возвращает саммаризированный текст диалога.
    """
    messages = [
        {"role": "system", "content": "Ты - нейро-саммаризатор. Твоя задача - саммаризировать диалог, который тебе пришел. Если пользователь назвал свое имя, обязательно отрази его в саммаризированном диалоге"},
        {"role": "user", "content": "Саммаризируй следующий диалог консультанта и пользователя: " + " ".join(dialog)}
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-4-0613",     # используем gpt4 для более точной саммаризации
        messages=messages,
        temperature=0,          # Используем более низкую температуру для более определенной суммаризации
    )

    return completion.choices[0].message.content


def answer_user_question_dialog(system, db, user_question, question_history):
    """
    Функция возвращает ответ на вопрос пользователя.
    """
    summarized_history = ""
    # Если в истории более одного вопроса, применяем суммаризацию
    if len(question_history) > 0:
        summarized_history = "Вот краткий обзор предыдущего диалога: " + summarize_questions([q + ' ' + (a if a else '') for q, a in question_history])

    # Добавляем явное разделение между историей диалога и текущим вопросом
    input_text = summarized_history + "\n\nТекущий вопрос: " + user_question

    # Извлекаем наиболее похожие отрезки текста из базы знаний и получение ответа модели
    answer_text = answer_index(system, input_text, db)

    # Добавляем вопрос пользователя и ответ системы в историю
    question_history.append((user_question, answer_text if answer_text else ''))

    # Выводим саммаризированный текст, который видит модель
    if summarized_history:
        print('****************************')
        print(insert_newlines(summarized_history))
        print('****************************')

    return insert_newlines(answer_text)


def run_dialog(system_doc_url, knowledge_base_url):
    """
    Функция запускает диалог между пользователем и нейро-консультантом.
    """
    #список кортежей, где каждый кортеж содержит пару вопрос-ответ, для отслеживания истории вопросов и ответов во время сессии диалога.
    question_history = []
    while True:
        user_question = input('Пользователь: ')
        if user_question.lower() == 'stop':
            break
        answer = answer_user_question_dialog(system_doc_url, knowledge_base_url, user_question, question_history)
        print('Консультант:', answer)

    return

        
def main():
    # db_path = "DBs/db_2024_02.txt"
    db_path = "db_2024_02"
    folder = "DBs"
    system = "Ты эксперт в области электронной коммерции, аналитик, \
        прекрасно разбираешься в технологиях, маркетинге, создании и \
        развитии интернет- магазинов, вопросах лояльности и других, связанных с e-commerce"
    content = "Ответь на вопрос клиента"
    # folder_path="DBs"
    # b_name="db_2024_02"

    # text = open_files("consult_data_insight_db.txt")
    # chunks = make_chunks(text)
    # db = making_em_db(chunks)

    db = open_em_db(db_path, folder)
    # db = add_text_em_db(db, chunks)
    # saving_em_db(db, folder_path, b_name)

    # result = db.similarity_search(topic, k=4)

    # load_document_text("https://drive.google.com/file/d/1-2u4leel-dttGWOy7b01pu0AGs-m9plD/view?usp=drive_link")
    # text=duplicate_headers_without_hashes(text)

    # text = split_text(text)
     # text = open_files("PreachersHelperBot/Pamfil_Evsevij_Cerkovnaya_istoriya.txt")
    question = input("inter question: ")

    answer = answer_index(db, question, system, content)
    print(answer)




    
    # topic = input("Entet your question? ")
    # system = "Ты-консультант по библии, ответь на вопрос клиента на основе библии с информацией. Не придумывай ничего от себя, отвечай только по библии. Упоминай библию с точной информацией откуда для ответа клиенту"

    # # seach_relavent_text(db, topic)
    
    # ans = answer_index(system, topic, db)
    # print(ans)


    # answer_index(system, topic, search_index, verbose=1)

    # similar_documents = faiss_instance.search("какие есть подписки", "similarity")


if __name__ == "__main__":
    main()

print('finish_time:', time.time() - start_time)




