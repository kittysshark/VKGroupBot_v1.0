import telebot
from telebot import types
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

token ='Your token'
id_channel = '@Your_chat_id'
URL = 'https://vk.com/your_vk_group'
bot = telebot.TeleBot(token)
post_number = 0
newpost = None
header = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept' : '*/*',
    'accept-encoding' : 'gzip, deflate, br',
    'accept-language' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer' : 'https://queuev4.vk.com/q_frame.php?7',
    'cashe-control' : 'no-store',
    'server' : 'kittenx',
    'sec-ch-ua' : '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-platform' : '"Windows"',
    'x-requested-with' : 'XMLHttpRequest'
    }
print("Bot Started!")

while True:
    page = requests.get(URL, headers = header)

    with open('index.html','w') as file:
        file.write(page.text)

    with open("index.html") as fp:
        soup = BeautifulSoup(fp, 'lxml')

    postInfo = soup.find_all('a', class_="author")
    LINK = URL + str(postInfo[post_number + 1].get('data-post-id'))

    if str(postInfo[post_number + 1].get('data-post-id')) == None:
        error = 'Error: postInfo = None'
        print(error)
        bot.send_message(id_channel, error)

    if LINK != newpost and str(postInfo[post_number + 1].get('data-post-id')) != None:
        date = datetime.now()
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Перейти к записи 🛫", url=LINK)
        markup.add(button1)
        bot.send_message(id_channel, f'Новый пост в нашем сообществе. Бегом смотреть!\n\n{LINK}',reply_markup=markup)
        print(f'{date} || {LINK}')
        print("-" * 90)
        newpost = LINK

    #print("-" * 60)
    time.sleep(14400)

bot.infinity_polling()

