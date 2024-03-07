from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from dotenv import load_dotenv
import openai
import os
import requests
import aiohttp
import json
import datetime
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import re
from apps import sqlight



def open_em_db(folder_path, index_name):
    
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


def answer_index(topic, system, content, b_path, index_name, verbose=1, score_threshold = 0.6, k=4):
    db = open_em_db(b_path, index_name)

    
    print(topic)
    docs = db.similarity_search_with_relevance_scores(topic, k, score_threshold=score_threshold)
    message_content = ""
    for doc, similarity_score in docs:
            print(f"Document: {doc.page_content}, Similarity Score: {similarity_score}")
            message_content = message_content + doc.page_content
            print("-----------")
   
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
    print("Something else went wrong")
    return {"message": answer, "system": system, "content": content}  # возвращает ответ







