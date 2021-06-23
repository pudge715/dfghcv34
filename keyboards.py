from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

import db

main = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width=2)
acquaintances = types.KeyboardButton(text = '👥 Знакомства')
vacancy = types.KeyboardButton(text = '💻 Вакансии')
fjob = types.KeyboardButton(text = '🔎 Ищу работу')
main.add(acquaintances,vacancy,fjob)

findjob = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width = 2)
watch = types.KeyboardButton(text = 'Просмотр анкет')
zap = types.KeyboardButton(text = 'Заполнить анкету')
mn = types.KeyboardButton(text = 'Главное меню')
findjob.add(watch,zap,mn)

back = types.ReplyKeyboardMarkup(resize_keyboard = True)
otmena = types.KeyboardButton('Отмена')
back.add(otmena)

znak = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
watch = types.KeyboardButton(text = 'Анкеты')
zap = types.KeyboardButton(text = 'Подать анкету')
mn = types.KeyboardButton(text = 'Главное меню')
znak.add(watch,zap,mn)

adm = types.InlineKeyboardMarkup(resize_keyboard = True,row_width = 1)
stat = types.InlineKeyboardButton(text = 'Статистика',callback_data = 'stat')
ras = types.InlineKeyboardButton(text = 'Рассылка',callback_data = 'ras')
ban = types.InlineKeyboardButton(text = 'Забанить юзера',callback_data='ban')
rekl = types.InlineKeyboardButton(text = 'Добавить вакансию',callback_data = 'rekl')
adm.add(stat,ras,ban,rekl)

def Links(id, start, table):
    link = db.getCurrentLink(id, table)
    country = db.getAllLinks(table)
    Links = types.InlineKeyboardMarkup(row_width=1)
    if table == "find_job":
        Links.add(types.InlineKeyboardButton("Написать ✅", url=f"{link[10]}"))
    else:
        Links.add(types.InlineKeyboardButton("Написать ✅", url=f"{link[9]}"))
    if country[0][0] == id:
        if len(country) > 1:
            Links.add(types.InlineKeyboardButton("Далее", callback_data=f'next_{country[start + 1][0]}_{start + 1}'))
    elif country[-1][0] == id:
        Links.add(types.InlineKeyboardButton("Назад", callback_data=f'back_{country[start - 1][0]}_{start - 1}'))
    else:
        Links.add(types.InlineKeyboardButton("Далее", callback_data=f'next_{country[start + 1][0]}_{start + 1}'))
        Links.add(types.InlineKeyboardButton("Назад", callback_data=f'back_{country[start - 1][0]}_{start - 1}'))
    return Links