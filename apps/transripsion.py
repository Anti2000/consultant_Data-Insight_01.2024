from IPython.display import Audio
from pydub import AudioSegment
import requests
import time
#import getpass
from getpass4 import getpass
import json
from tinkoff_voicekit_client import ClientSTT
from pprint import pprint
import youtube_dl
from tinytag import TinyTag
from moviepy.editor import *
import openai
import getpass
import os
from openai import OpenAI



start_time = time.time()



# передаем API_KEY
API_KEY = 'cFFZOuddS30uDk7hMawEx5WS97cYDSPYFZ94jG4fBMg='
# передаем SECRET_KEY
SECRET_KEY = 'SbXgTD4E+a++7nfnlyBU69mih73wnNM6mmYLysQ9zps='


def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

VIDEO_FILE_PATH = "E_commerce_2023_2024_obsugdaem_s_Fedorom_Virinum.mp4.mp4"
AUDIO_FILE_PATH = "dfsf.mp3"

# MP4ToMP3(VIDEO_FILE_PATH, AUDIO_FILE_PATH)


def youtube_downloud_mp3(youtube_url):
    video_url = youtube_url
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


# url = 'https://drive.google.com/file/d/1jWatVeG3OL2BL8qmI_GvucHklk9LIcHw/view?usp=sharing'



def tinfoff_geting(files_path):

  # создаем клиент, передаем ключи
  client = ClientSTT(API_KEY, SECRET_KEY)

  # указываем параметры аудио
  audio_config = {
      "encoding": "MPEG_AUDIO",
      "sample_rate_hertz": 44100,
      "num_channels": 2,
      "enable_automatic_punctuation": True
      }

  # вызываем метод recognize
  response = client.recognize(files_path,
                              audio_config)
  
  return response
  # print(response)




def taking_info(filename):
  try:
    audio = AudioSegment.from_file(filename, "mp3")
    music = audio
  except:
      print("bingo")
      audio = AudioSegment.from_file(filename, format="mp4")
    # чтение из файла любого формата
  # music = AudioSegment.from_file(file=files_url,
  #                             format='mp4')
  print(f'Продолжительность(в секундах): {music.duration_seconds}\n ,Частота дискретизаци: {music.frame_rate}\n Количество каналов: {music.channels}')





def listen_audio(edit_files_url):
  # Проверка аудио на качество и наличие путем прослушивания
  Audio(edit_files_url)



def dounlowd_file(url, files_name):
  response = requests.get(url)
  if response.status_code == 200:
    with open(files_name, 'wb') as f:
      f.write(response.content)
      print(f"Downloaded and saved as {files_name}")
  else:
    print(f"Failed to download. HTTP Status Code: {response.status_code}")

# for url, pdf_name in zip(urls, pdf_names):
#     print(url, pdf_name)
#     response = requests.get(url)
#     if response.status_code == 200:
#       with open(pdf_name, 'wb') as f:
#         f.write(response.content)
#         print(f"PDF downloaded and saved as {pdf_name}")
#     else:
#         print(f"Failed to download PDF. HTTP Status Code: {response.status_code}")




def json_format():
  with open('1.json') as user_file:
    s = user_file.read()
    s = s.replace("\'", "\"")
    data = json.loads(s)
    s = data["results"]
    text = ""
    
    for i in s:
      s = i["alternatives"]
      i = str(s)
      text = text + i
    # text = s
        
    # for i in s:
    #   if i["channel"] == 1:
    #     s = i["alternatives"][0]["transcript"]
    #     print("Клиент: ", s)
    #     text = text + s
    #   elif i["channel"] == 0:
    #     s = i["alternatives"][0]["transcript"]
    #     print("Менеджер: ", s)
    #     text = text + s
  return text

    

def safing_json(data, name_json):
  with open(name_json, 'w', encoding='utf-8') as fp:
    json.dump(data, fp, ensure_ascii=False)



def w_file(content, path="bingo_x.txt"):
  with open(path , "w", encoding="utf-8") as f:
   f.write(content)



def cut_size(files_url, edit_files_url):
  # чтение из файла любого формата
  debaty = AudioSegment.from_file(file=files_url,
                               format='mp3')
  # # выведем параметры
  print(debaty.duration_seconds)
  print(debaty.frame_rate)
  print(debaty.channels)

  
  #   ОТРЕЗОК ПОСЕРЕДИНЕ
  b_hack = 1000 * 1200 # представление 40 секунд в миллисекундах
  e_hack = 1000 * 2400
  # сохраним фрагмент в файл
  debaty[b_hack:e_hack].export(edit_files_url, format='mp3')

  # # КОНЕЦ АУ_ФАЙЛА
  # e_hack = 1000 * 2400
  # # сохраним фрагмент в файл
  # debaty[e_hack:].export(edit_files_url, format='mp3')

  # hack = 1000 * 1200


  # сохраним фрагмент в файл
  # debaty[:hack].export(edit_files_url, format='mp3')

# транскрибация
def transciption_ai(audio_file):
  openai_key = getpass.getpass("OpenAI API Key:")
  os.environ["OPENAI_API_KEY"] = openai_key
  openai.api_key = openai_key

  # создаем экземпляр класса OpenAI
  client = OpenAI()
  # import whisper

  audio_file= open(audio_file, "rb")

  # выполняем транскрибацию
  transcript = client.audio.transcriptions.create(model="whisper-1",
                                                  file=audio_file)

  return transcript.text


def main():
  youtube_url = "https://www.youtube.com/watch?v=EjUtLF9fC00&t=8s"
  mp3_file = "1_3.mp3"
  or_mp3_path = "or.mp3"
  s_mp3_path = "1_2.mp3"
  files_path = "context_2.txt"
  name_json = "1_1.json"


  # youtube_downloud_mp3(youtube_url)
  # dounlowd_file(url, files_url)
  # listen_audio(files_url)
  # taking_info(files_path)
  cut_size(or_mp3_path, s_mp3_path)
  # result = tinfoff_geting(files_path1)
  # print(result)
  # safing_json(result, name_json)
  # content = str(json_format())
  # print(content)
  content = transciption_ai(s_mp3_path)
  w_file(content, files_path)
  


if __name__ == "__main__":
    main()

print('finish_time:', time.time() - start_time)



  


    

