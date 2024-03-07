import sqlite3
import time
import sqlite3
import traceback
import sys
import time
from datetime import datetime
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



now = time.strftime("%Y-%m-%d %H:%M")

def record_deal(question = "bingo", answer="bingo", system="bingo", content = "bingo", id = "empty", comment="bingo"):
    print("bingo")
    
    # time= time.strftime("%Y-%m-%d %H:%M")
    time = now
    try:
        with sqlite3.connect("DBs/sqliteDbGpt.db") as con:
            cursor = con.cursor()
            sqlite_insert_query = """INSERT INTO DB(id, question, answer, system, content, time, comment)  VALUES  (?, ?, ?, ?, ?, ?, ?)"""
            count = cursor.execute(sqlite_insert_query, (id, question, answer, system, content, time, comment))
            
            con.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (cursor):
            cursor.close()
            print("Соединение с SQLite закрыто")
			
# def ids():
# 	with sqlite3.connect("DBs/sqliteDbGpt.db") as con:
# 		cursor = con.cursor()
#               result = """SELECT* from ids"""
# 	





def data_to_email():
        
		try:
			mail_content = '''chatgpt''' + now
			sender_address = "anatole.yakovlev@gmail.com"
			sender_pass = "tbunoakrikzyszdv"
			receiver_address = "antiohy@mail.ru"
			message = MIMEMultipart()
			message['From'] = sender_address
			message['To'] = receiver_address
			message['Subject'] = 'A backup mail sent by cars apl. It has an attachment. ' + now
			message.attach(MIMEText(mail_content, 'plain'))
			attach_file_name = "DBs/sqliteDbGpt.db"
			attach_file = open(attach_file_name, 'rb')
			payload = MIMEBase('application', 'octate-stream')
			payload.set_payload((attach_file).read())
			encoders.encode_base64(payload)
			payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
			message.attach(payload)
			session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
			session.starttls() #enable security
			session.login(sender_address, sender_pass) #login with mail_id and password
			text = message.as_string()
			session.sendmail(sender_address, receiver_address, text)
			session.quit()
		except:
			print(f"{'check internet connection'}")
                  
def add_id(id):
    print("add_id in table")
    try:
        with sqlite3.connect("sqliteDbGpt.db") as con:
            cursor = con.cursor()
            sqlite_insert_query = """INSERT INTO ids(id) VALUES (?)"""
            count = cursor.execute(sqlite_insert_query, int(id))
            
            con.commit()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (cursor):
            cursor.close()
            print("Соединение с SQLite закрыто")

def ids():

	with sqlite3.connect("DBs/sqliteDbGpt.db") as con:
		
		cursor = con.cursor()
		# datax = cursor.execute("SELECT* from ids")
		sqlite_insert_query = """SELECT * from ids"""
		data = cursor.execute(sqlite_insert_query)
		ids = []
		for i in data:
			ids.append(i)

	if (cursor):
		cursor.close()
		print("Соединение с SQLite закрыто")
            
	return ids

# record_deal()
