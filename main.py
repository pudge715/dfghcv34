import sqlite3
from sqlite3 import Error
import keyboards as kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from config import token,admins
import random
import time
import db

TOKEN = token
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot,storage = MemoryStorage())

class anketa(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()


class zanketa(StatesGroup):
    z1 = State()
    z2 = State()
    z3 = State()
    z4 = State()
    z5 = State()
    z6 = State()
    z7 = State()

class mailing(StatesGroup):
    text = State()

class banl(StatesGroup):
    nick = State()

class advent(StatesGroup):
    atext = State()

with sqlite3.connect("database.db") as conn:
  cursor = conn.cursor()
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS acquaintances
  (user_id INTEGER,user_name TEXT,user_number TEXT,age INTEGER,gender TEXT,activity TEXT,about TEXT,whom_is_he_looking)
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS find_job
  (user_id INTEGER,user_name TEXT,user_number TEXT,age TEXT,gender TEXT,activity TEXT,what_wants TEXT,devote_time TEXT,earn_money TEXT,telegram TEXT)
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS users
  (user_id INTEGER,user_name TEXT)
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS banlist
  (user_id INTEGER,user_name TEXT)
  """)
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS ad
  (id INTEGER,text TEXT)
  """)
  


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    cursor.execute("select * from users where user_id = ?",(message.from_user.id,))
    usr = cursor.fetchone()
    if not usr:
            cursor.execute("INSERT INTO users values (:user_id, :user_name);" ,
            {'user_id':message.from_user.id,
            'user_name':message.from_user.username})
            conn.commit()
    await bot.send_message(message.chat.id,text = f'👋 Добро пожаловать,{message.from_user.first_name}\nДля навигации по боту используй кнопки ниже.',reply_markup = kb.main)

@dp.message_handler(commands=['adm'])
async def send_welcome(message: types.Message):
    if message.from_user.id in admins:
        await bot.send_message(message.chat.id,text = 'success!',reply_markup=kb.adm)


@dp.message_handler(content_types = ['text'])
async def get_text(message: types.message,state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    if message.text == 'Главное меню':
        await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
    if message.text == '👥 Знакомства':
        await bot.send_message(message.chat.id,text = 'Для навигации по данному разделу используйте кнопки ниже',reply_markup = kb.znak)
    if message.text == 'Подать анкету':
        await bot.send_message(message.chat.id,text = 'Укажите Ваш возраст',reply_markup=kb.back)
        await zanketa.z1.set()
    if message.text == 'Анкеты':
        await state.update_data(table="acquaintances")
        acquaintances = db.getAllLinks("acquaintances")
        if acquaintances:
            await message.answer_photo(open(f"photo/{acquaintances[0][1]}.jpg", "rb"), f"""<b>
Возраст: <code>{acquaintances[0][4]}</code> 
Пол: <code>{acquaintances[0][5]}</code> 
Деятельность: <code>{acquaintances[0][6]}</code> 
Обо мне: <code>{acquaintances[0][7]}</code> 
Цель поиска: <code>{acquaintances[0][8]}</code> 
</b>""", reply_markup=kb.Links(acquaintances[0][0], 0, "acquaintances"))
        else:
            await message.answer(f"<b>В данный момент нет анкет</b>")
            return
    if message.text == '💻 Вакансии':
        ttt = cursor.execute(f"SELECT text FROM ad WHERE id = 1").fetchone()[0]
        await bot.send_message(message.chat.id,text = f'{ttt}')
    if message.text == '🔎 Ищу работу':
        await message.answer('Для навигации по данному разделу используйте кнопки ниже',reply_markup = kb.findjob)
    if message.text == 'Просмотр анкет':
        await state.update_data(table="find_job")
        jobs = db.getAllLinks("find_job")
        if jobs:
            await message.answer_photo(open(f"photo/{jobs[0][1]}.jpg", "rb"), f"""<b>
Возраст: <code>{jobs[0][5]}</code> 
Пол: <code>{jobs[0][4]}</code> 
Деятельность: <code>{jobs[0][6]}</code> 
Чем хочет заниматься: <code>{jobs[0][7]}</code> 
Готов уделять: <code>{jobs[0][8]}</code> 
Хочет заработать: <code>{jobs[0][9]}</code> 

</b>""", reply_markup=kb.Links(jobs[0][0], 0, "find_job"))
        else:
            await message.answer(f"<b>В данный момент нет анкет</b>")
            return
    if message.text == 'Заполнить анкету':
        await bot.send_message(message.chat.id,text = 'Укажите Ваш пол',reply_markup=kb.back)
        await anketa.q1.set()

@dp.callback_query_handler(lambda call: "next_" in call.data or "back_" in call.data, state="*")
async def callback_alent_n(call: types.callback_query, state: FSMContext):
    state_data = await state.get_data()
    data = call.data.split("_")
    link = db.getCurrentLink(data[1], state_data["table"])
    if state_data["table"] == "find_job":
        text = f"""<b>
Возраст: <code>{link[5]}</code> 
Пол: <code>{link[4]}</code> 
Деятельность: <code>{link[6]}</code> 
Чем хочет заниматься: <code>{link[7]}</code> 
Готов уделять: <code>{link[8]}</code> 
Хочет заработать: <code>{link[9]}</code> 
</b>"""
    elif state_data["table"] == "acquaintances":
        text = f"""<b>
Возраст: <code>{link[4]}</code> 
Пол: <code>{link[5]}</code> 
Деятельность: <code>{link[6]}</code> 
Обо мне: <code>{link[7]}</code> 
Цель анкеты: <code>{link[8]}</code> 
</b>"""
    await bot.edit_message_media(media=types.InputMediaPhoto(media=open(f"photo/{link[1]}.jpg", "rb"), caption=text), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=kb.Links(int(data[1]), int(data[2]), state_data["table"]))

@dp.message_handler(state=zanketa.z1)
async def z1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z1 = message.text
    await state.update_data(z1=z1)
    await bot.send_message(message.chat.id,text = 'Укажите Ваш пол',reply_markup=kb.back)
    await zanketa.z2.set()

@dp.message_handler(state=zanketa.z2)
async def z2(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z2 = message.text
    await state.update_data(z2=z2)
    await bot.send_message(message.chat.id,text = 'Ваша сфера деятельности?',reply_markup=kb.back)
    await zanketa.z3.set()

@dp.message_handler(state=zanketa.z3)
async def z3(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z3 = message.text
    await state.update_data(z3=z3)
    await bot.send_message(message.chat.id,text = 'Коротко о себе',reply_markup=kb.back)
    await zanketa.z4.set()

@dp.message_handler(state=zanketa.z4)
async def z4(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z4 = message.text
    await state.update_data(z4=z4)
    await bot.send_message(message.chat.id,text = 'Кого хотите найти и зачем?',reply_markup=kb.back)
    await zanketa.z5.set()

@dp.message_handler(state=zanketa.z5)
async def z5(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z5 = message.text
    await state.update_data(z5=z5)
    await bot.send_message(message.chat.id,text = 'Укажите ссылку на Ваш телеграм\n[t.me/name]',reply_markup=kb.back)
    await zanketa.z6.set()

@dp.message_handler(state=zanketa.z6)
async def z6(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    z6 = message.text
    await state.update_data(z6=z6)
    await bot.send_message(message.chat.id,text = 'Пришлите Ваше фото',reply_markup=kb.back)
    await zanketa.z7.set()


@dp.message_handler(state=zanketa.z7,content_types=['photo'])
async def z7(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    await message.photo[-1].download(f'photo/{message.from_user.id}.jpg')
    data = await state.get_data()
    age = data.get('z1')
    gender = data.get('z2')
    activity = data.get('z3')
    about = data.get('z4')
    whom_is_he_looking = data.get('z5')
    tg = data.get('z6')
    cursor.execute("INSERT INTO acquaintances ('user_id', 'user_name', 'user_number', 'age', 'gender', 'activity', 'about',  'whom_is_he_looking', 'telegram') values (:user_id, :user_name, :user_number, :age, :gender, :activity, :about, :whom_is_he_looking, :telegram);",
    {'user_id': message.from_user.id,
    'user_name': message.from_user.first_name,
    'user_number':'hidden',
    'age':age,
    'gender':gender,
    'activity':activity,
    'about':about,
    'whom_is_he_looking':whom_is_he_looking,
    'telegram':tg})
    conn.commit()
    await bot.send_message(message.chat.id,text = 'Ваша анкета была сохранена!',reply_markup=kb.main)
    await state.finish()


@dp.message_handler(state=anketa.q1)
async def q1(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q1 = message.text
    await state.update_data(q1=q1)
    await bot.send_message(message.chat.id,text = 'Укажите Ваш возраст',reply_markup=kb.back)
    await anketa.q2.set()


@dp.message_handler(state=anketa.q2)
async def q2(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q2 = message.text
    await state.update_data(q2=q2)
    await bot.send_message(message.chat.id,text = 'Что умеете делать?',reply_markup=kb.back)
    await anketa.q3.set()

@dp.message_handler(state=anketa.q3)
async def q3(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q3 = message.text
    await state.update_data(q3=q3)
    await bot.send_message(message.chat.id,text = 'Что хотите делать?',reply_markup=kb.back)
    await anketa.q4.set()

@dp.message_handler(state=anketa.q4)
async def q4(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q4 = message.text
    await state.update_data(q4=q4)
    await bot.send_message(message.chat.id,text = 'Cколько времени готовы уделять?',reply_markup=kb.back)
    await anketa.q5.set()

@dp.message_handler(state=anketa.q5)
async def q5(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q5 = message.text
    await state.update_data(q5=q5)
    await bot.send_message(message.chat.id,text = 'Сколько хотите заработать?',reply_markup=kb.back)
    await anketa.q6.set()

@dp.message_handler(state=anketa.q6)
async def q6(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q6 = message.text
    await state.update_data(q6=q6)
    await bot.send_message(message.chat.id,text = 'Ссылка на Ваш Telegram\n[t.me/name]',reply_markup=kb.back)
    await anketa.q7.set()

@dp.message_handler(state=anketa.q7)
async def q7(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    q7 = message.text
    await state.update_data(q7=q7)
    await bot.send_message(message.chat.id,text = 'Отправьте фотографию для анкеты',reply_markup=kb.back)
    data = await state.get_data()
    age = data.get('q1')
    gender = data.get('q2')
    activity = data.get('q3')
    what_wants = data.get('q4')
    devote_time = data.get('q5')
    earn_money = data.get('q6')
    cursor.execute("INSERT INTO find_job ('user_id', 'user_name', 'user_number', 'age', 'gender', 'activity', 'what_wants', 'devote_time', 'earn_money', 'telegram') values (:user_id, :user_name, :user_number, :age, :gender, :activity, :what_wants, :devote_time, :earn_money, :telegram);",
    {'user_id': message.from_user.id,
    'user_name': message.from_user.first_name,
    'user_number':'hidden',
    'age':age,
    'gender':gender,
    'activity':activity,
    'what_wants':what_wants,
    'devote_time':devote_time,
    'earn_money':earn_money,
    'telegram':message.text})
    conn.commit()
    await anketa.q8.set()

@dp.message_handler(state=anketa.q8,content_types=['photo'])
async def q8(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    await message.photo[-1].download(f'photo/{message.from_user.id}.jpg')
    await bot.send_message(message.chat.id,text = 'Ваша анкета была сохранена!',reply_markup=kb.main)
    await state.finish()


@dp.message_handler(state=banl.nick)
async def ban(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    nick = message.text
    cursor.execute("INSERT INTO users values (:user_id, :user_name);" ,
    {'user_id':'-',
    'user_name':nick})
    conn.commit()
    await state.update_data(nick=nick)
    await bot.send_message(message.chat.id,text = 'Пользователь заблокирован.',reply_markup=kb.main)
    await state.finish()


@dp.message_handler(state=advent.atext)
async def ad(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Вы были возвращены в главное меню',reply_markup=kb.main)
            await state.finish()
            return
    atext = message.text
    cursor.execute(f'UPDATE ad SET text = "{atext}" WHERE id = "1"')
    conn.commit()
    await state.update_data(atext=atext)
    await bot.send_message(message.chat.id,text = 'Вакансия добавлена',reply_markup=kb.main)
    await state.finish()

@dp.message_handler(state=mailing.text)
async def mtext(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
            await bot.send_message(message.chat.id,text = 'Отменено',reply_markup=kb.main)
            await state.finish()
            return
    text = message.text
    await state.update_data(text=text)
    users = cursor.execute("SELECT user_id FROM users")
    print(users)
    for user in users:
        try:
            await bot.send_message(chat_id=user[0],text = f"{text}")
            time.sleep(0.3)
        except:
            print('error')
    await bot.send_message(message.chat.id,text = "Рассылка завершена")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data)
async def ans(call: CallbackQuery,state: FSMContext):
    if call.data == 'stat':
        us = cursor.execute('SELECT Count(*) FROM users').fetchone()[0]
        z = cursor.execute('SELECT Count(*) FROM acquaintances').fetchone()[0]
        f = cursor.execute('SELECT Count(*) FROM find_job').fetchone()[0]
        await bot.send_message(call.message.chat.id,text = f'<b>Статистика</b>\n\n<b>Пользователей:</b> {us}\n<b>Анкет в знакомствах:</b> {z}\n<b>Анкет в работе:</b> {f}')
    if call.data == 'ras':
        await bot.send_message(call.message.chat.id,text = 'Введите текст рассылки',reply_markup=kb.back)
        await mailing.text.set()
    if call.data == 'ban':
        await bot.send_message(call.message.chat.id,text = 'Введи ник пользователя',reply_markup = kb.back)
        await banl.nick.set()
    if call.data == 'rekl':
        await bot.send_message(call.message.chat.id,text = 'Введите текст вакансии')
        await advent.atext.set()

executor.start_polling(dp)