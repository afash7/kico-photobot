# -*- coding: utf-8 -*-

import os
import sys
import telebot
import sqlite3

TOKEN = "6841408162:AAFHdaBGKig_cYO6FKZRY5Nimbn4YP_ohug"

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect("database.db")

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS projects (user_id INTEGER, name TEXT, project TEXT, photo BLOB)")

steps = {}
names = {}
projects = {}

@bot.message_handler(content_types=["text"])

def handle_text(message):
    user_id = message.from_user.id
    if user_id not in steps:
        steps[user_id] = 0
    if steps[user_id] == 0:
        bot.send_message(user_id, "سلام. در اینجا میتوانید تصاویر پروژه یا بارگیری را ارسال کنید")
        bot.send_message(user_id, "لطفا نام کامل خود را به درستی وارد کنید:")
        steps[user_id] += 1
    elif steps[user_id] == 1:
        names[user_id] = message.text
        bot.send_message(user_id, f"خوش آمدید {names[user_id]}")
        bot.send_message(user_id, "لطفا نام پروژه را وارد کنید:")
        steps[user_id] += 1
    elif steps[user_id] == 2:
        projects[user_id] = message.text
        bot.send_message(user_id, f"پروژه {projects[user_id]} را انتخاب کردید.")
        bot.send_message(user_id, "لطفا عکس های پروژه را ارسال کنید:")
        steps[user_id] += 1
    else:
        bot.send_message(user_id, "در این مرحله فقط عکس قبول میشود. لطفا عکس های پروژه خود را ارسال کنید:")

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    user_id = message.from_user.id
    if user_id not in steps:
        steps[user_id] = 0
    if steps[user_id] < 3:
        bot.send_message(user_id, "در این مرحله فقط متن قبول میشود. لطفا نام خود و پروژه خود را وارد کنید:")
    else:
        file_id = message.photo[-1].file_id
        file = bot.get_file(file_id)
        photo = bot.download_file(file.file_path)
        cur.execute("INSERT INTO projects VALUES (?, ?, ?, ?)", (user_id, names[user_id], projects[user_id], photo))
        conn.commit()
        bot.send_message(user_id, "عکس شما با موفقیت ذخیره شد.")
        bot.send_message(user_id, "اگر عکس دیگری دارید، می توانید ارسال کنید. در غیر این صورت، می توانید ربات را ترک کنید.")
bot.polling()