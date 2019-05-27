import telebot
import os
import MySQLdb

bot = telebot.TeleBot("805627194:AAG3Eptl1E48WijSQ3tejTqi8J6lY48sxRU")
db = MySQLdb.connect(host="aa6bkyeme6tejq.c1amhyf5jdyt.us-east-2.rds.amazonaws.com",    # localhost
                user="userDB",         #  username
                 passwd="020896lumen",  #  password
                 db="TelegramBot")        # name of the data base
cur = db.cursor()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Отправьте мне аудиосообщение, и я сохраню его в бд. Для получения информации используйте /help")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Для сохранения аудиосообщения создайте или перешлите его боту. Для просмотра количества сохраненных сообщений отправьте /myvoices")


@bot.message_handler(commands=['myvoices'])
def count_voices(message):
    cur.execute('SELECT voice_name FROM voices where user_create_id = %s', (str(message.from_user.id), ))
    data = cur.fetchall()
    db.commit()
    print(data)
    voice_names='['
    for item in data:
        if item != data[-1]:
            voice_names = voice_names + item[0] + ', '
        else:
            voice_names = voice_names + item[0] + ']'
    answer=str(message.from_user.id)+ ' --> ' + voice_names
    bot.reply_to(message,answer ) 


@bot.message_handler(content_types=['voice'])
def handler(message):
    file_info = bot.get_file(message.voice.file_id)
    file_name = file_info.file_path.replace('voice/', '')
    downloaded_file = bot.download_file(file_info.file_path)
    try:
        sql_insert_blob_query ="""INSERT INTO voices (user_create_id,voice_name, voice) VALUES(%s,%s, %s)"""
        cur.execute(sql_insert_blob_query, (message.from_user.id, file_name, downloaded_file ))
        db.commit()
        bot.reply_to(message,"Аудио добавлено") 
    except Exception as e:
        bot.reply_to(message,e )
        

bot.polling(none_stop=True)
