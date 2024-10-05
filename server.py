import asyncio
import os
from datetime import date
import json
from aiogram.enums.parse_mode import ParseMode

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputFile, FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from functions import Functions
from MediaGroupHandler import AlbumMiddleware
from functions import Functions

# Объект бота
bot = Bot(token="BOT_API_TOKEN")
# Диспетчер
dp = Dispatcher()
ANSWER = 0
ADMIN_ID = 355721034
username = ""
FILE_NAME = ''
USER_ID_DOWNLOAD = 0
USER_ID_POINTS = 0
MEDIA_GROUP = []
dp.message.middleware(AlbumMiddleware())
PATH = ''
MSG = None
USER_ID = 0
SIZES = ()
DATA = ''
class States(StatesGroup):
    STATE_register = State()
    STATE_file = State()
    STATE_points = State()
    STATE_homework = State()
    STATE_get_media_group = State()
    STATE_send_exam = State()
    STATE_add_date = State()
    STATE_edit_date = State()

if os.path.exists('data/user_data.json'):
    with open('data/user_data.json') as f:
        USER_DICT = json.load(f)
    print(USER_DICT)
else:
    USER_DICT = {}
WAYS = ['ЕГЭ - Информатика', 'ОГЭ - Информатика', 'ОГЭ - Математика', 'Информатика', 'Математика']
def save_to_file():
    js = json.dumps(USER_DICT)
    with open('data/user_data.json', 'w') as f:
        f.write(js)
    print(USER_DICT)
@dp.message(F.text == "Регистрация")
async def cmd_register(message: types.Message, state: FSMContext):
    await message.answer(f"Введи своё имя")
    await state.set_state(States.STATE_register)


@dp.message(States.STATE_register)
async def get_data(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    if user_id not in USER_DICT:
        USER_DICT[user_id] = {}

    if "name" not in USER_DICT[user_id]:
        USER_DICT[user_id]["name"] = message.text
        await message.answer(f'Привет, {message.text}. Как твоя фамилия?')
    elif "last_name" not in USER_DICT[user_id]:
        USER_DICT[user_id]["last_name"] = message.text
        b1 = types.KeyboardButton(text='ЕГЭ - Информатика')
        b2 = types.KeyboardButton(text='ОГЭ - Информатика')
        b3 = types.KeyboardButton(text='ОГЭ - Математика')
        b4 = types.KeyboardButton(text='Информатика')
        b5 = types.KeyboardButton(text='Математика')
        kb = types.ReplyKeyboardMarkup(keyboard=[[b1], [b2], [b3], [b4, b5]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(f"Направление подготовки?", reply_markup=kb)
    elif 'way' not in USER_DICT[user_id]:
        if message.text not in WAYS:
            b1 = types.KeyboardButton(text='ЕГЭ - Информатика')
            b2 = types.KeyboardButton(text='ОГЭ - Информатика')
            b3 = types.KeyboardButton(text='ОГЭ - Математика')
            b4 = types.KeyboardButton(text='Информатика')
            b5 = types.KeyboardButton(text='Математика')
            kb = types.ReplyKeyboardMarkup(keyboard=[[b1], [b2], [b3], [b4, b5]], resize_keyboard=True,
                                           one_time_keyboard=True)
            await message.answer(f"Направление подготовки?", reply_markup=kb)
        else:
            USER_DICT[user_id]['way'] = message.text
            path = ''
            if message.text == 'ЕГЭ - Информатика':
               path = f'Homework/Ege-IT/{USER_DICT[user_id]['name']}-{USER_DICT[user_id]['last_name']}'
            elif message.text == 'ОГЭ - Информатика':
                path = f'Homework/Oge-IT/{USER_DICT[user_id]['name']}-{USER_DICT[user_id]['last_name']}'
            elif message.text == 'ОГЭ - Математика':
                path = f'Homework/Oge-Math/{USER_DICT[user_id]['name']}-{USER_DICT[user_id]['last_name']}'
            elif message.text == 'Информатика':
                path = f'Homework/IT/{USER_DICT[user_id]['name']}-{USER_DICT[user_id]['last_name']}'
            elif message.text == 'Математика':
                path = f'Homework/Math/{USER_DICT[user_id]['name']}-{USER_DICT[user_id]['last_name']}'
            if not os.path.exists(path):
                os.mkdir(path)
            save_to_file()
            await message.answer(f"Спасибо за регистрацию!")
            await state.clear()
            await cmd_menu(message)


def return_folder_name(way: str):
    if way == 'ЕГЭ - Информатика':
        return 'Ege-IT'
    elif way == 'ОГЭ - Информатика':
        return 'Oge-IT'
    elif way == 'ОГЭ - Математика':
        return 'Oge-Math'
    elif way == 'Информатика':
        return 'IT'
    elif way == 'Математика':
        return 'Math'
# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}")
    await cmd_menu(message)


@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        b1 = types.InlineKeyboardButton(text="Отправить домашнее задание", callback_data='send-homework')
        b2 = types.InlineKeyboardButton(text="Добавить задание на ОГЭ / ЕГЭ", callback_data='add-exam')
        b3 = types.InlineKeyboardButton(text='Показать статистику', callback_data='send-statistic')
        b4 = types.InlineKeyboardButton(text='Добавить баллы', callback_data='add_points')
        b5 = types.InlineKeyboardButton(text='Поставить расписание', callback_data='add_dates')
        b6 = types.InlineKeyboardButton(text='Изменить расписание', callback_data='change_dates')
        kb = types.InlineKeyboardMarkup(inline_keyboard=[[b1], [b2], [b3, b4], [b5, b6]])
        await message.answer(f"Что делаем?", reply_markup=kb)
    elif str(message.from_user.id) not in USER_DICT.keys():
        b1 = types.KeyboardButton(text="Регистрация")
        kb = types.ReplyKeyboardMarkup(keyboard=[[b1]], resize_keyboard=True, one_time_keyboard=True)
        await message.answer(f"Пожалуйста, зарегистрируйся.", reply_markup=kb)
    else:
        b1 = types.KeyboardButton(text="Домашнее задание")
        b2 = types.KeyboardButton(text="Баллы за выполнение домашнего задания")
        b3 = types.KeyboardButton(text='Статистика')
        b4 = types.KeyboardButton(text='Сдать домашнее задание')
        b5 = types.KeyboardButton(text='Моё расписание')
        if USER_DICT[str(message.from_user.id)]['way'] in ['ЕГЭ - Информатика', 'ОГЭ - Информатика', 'ОГЭ - Математика']:
            b6 = types.KeyboardButton(text='Решать экзаменационные задачи')
            kb = types.ReplyKeyboardMarkup(keyboard=[[b1, b3],[b2], [b4, b5], [b6]], resize_keyboard=True, one_time_keyboard=True)
        else:
            kb = types.ReplyKeyboardMarkup(keyboard=[[b1, b3], [b2], [b4, b5]], resize_keyboard=True,
                                           one_time_keyboard=True)
        await message.answer(f"Чем бы ты хотел заняться?", reply_markup=kb)

@dp.message(F.text == "Моё расписание")
async def return_schedule(message: types.Message):
    if 'dates' in USER_DICT[str(message.from_user.id)].keys():
        answer = (f'<b>{USER_DICT[str(message.from_user.id)]['name']} {USER_DICT[str(message.from_user.id)]['last_name']}</b>\n'
                  f'Твоё расписание (время указано по Москве):\n\n')
        for data in USER_DICT[str(message.from_user.id)]['dates']:
            answer += f'{data}\n'
    else:
        answer = 'Тебе пока не поставили расписание'
    await message.answer(answer, parse_mode=ParseMode.HTML)

@dp.callback_query(F.data == "send-homework")
async def send_homework(callback: types.CallbackQuery):
    await Functions.show_students(USER_DICT, 'student_homework_', 'Выбери студента', callback)
    await callback.answer()

@dp.callback_query(F.data == "add_points")
async def add_points(callback: types.CallbackQuery):
    await Functions.show_students(USER_DICT, 'student_points_', 'Выбери студента', callback)

@dp.callback_query(F.data.startswith('student_points_'))
async def cmd_selected_student_points(call: CallbackQuery, state: FSMContext):
    global USER_ID_POINTS
    USER_ID_POINTS = str(call.data).replace('student_points_', '')
    await call.message.edit_text(f'Сколько баллов добавить? Если нужно убавить, отправьте знак "-" перед числом')
    await state.set_state(States.STATE_points)
    await call.answer()

@dp.callback_query(F.data.startswith('student_homework_'))
async def cmd_selected_student_homework(call: CallbackQuery, state: FSMContext):
    global USER_ID_DOWNLOAD
    USER_ID_DOWNLOAD = str(call.data).replace('student_homework_', '')
    await call.message.edit_text(f'Отправьте файл домашнего задания')
    await state.set_state(States.STATE_file)
    await call.answer()

@dp.message(States.STATE_points)
async def set_points(message: types.Message, state: FSMContext):
    if 'points' not in USER_DICT[USER_ID_POINTS].keys():
        USER_DICT[USER_ID_POINTS]['points'] = 0
    try:
        USER_DICT[USER_ID_POINTS]['points'] += int(message.text)
        await message.answer(f'Студенту {USER_DICT[USER_ID_POINTS]['name']} {USER_DICT[USER_ID_POINTS]['last_name']} добавлено {message.text} баллов.\n'
                            f'Количество баллов: {USER_DICT[USER_ID_POINTS]['points']}')
        if int(message.text) > 0:
            await bot.send_message(int(USER_ID_POINTS), f'Тебе добавили {message.text} {Functions.translate_num_to_rus(abs(int(message.text)))}\n'
                                                        f'Твой баланс: {USER_DICT[USER_ID_POINTS]['points']}')
        else:
            await bot.send_message(int(USER_ID_POINTS), f'У тебя забрали {abs(int(message.text))} {Functions.translate_num_to_rus(abs(int(message.text)))}\n'
                                                        f'Твой баланс: {USER_DICT[USER_ID_POINTS]['points']}')
        save_to_file()
        await state.clear()
    except:
        await message.answer(text='Вы ввели некорректное число. Попробуйте ещё раз')


@dp.message(States.STATE_file)
async def get_file(message: types.Message, state: FSMContext):
    if 'count_homeworks' not in USER_DICT[USER_ID_DOWNLOAD].keys():
        USER_DICT[USER_ID_DOWNLOAD]['count_homeworks'] = 1
    else:
        USER_DICT[USER_ID_DOWNLOAD]['count_homeworks'] += 1

    if 'total_homeworks' not in USER_DICT[USER_ID_DOWNLOAD].keys():
        USER_DICT[USER_ID_DOWNLOAD]['total_homeworks'] = 0

    path = f'Homework/{return_folder_name(USER_DICT[USER_ID_DOWNLOAD]['way'])}/{USER_DICT[USER_ID_DOWNLOAD]['name']}-{USER_DICT[USER_ID_DOWNLOAD]['last_name']}/{date.today()}_{USER_DICT[USER_ID_DOWNLOAD]['count_homeworks']}.pdf'
    await message.bot.download(file=message.document.file_id, destination=path)
    await message.answer(text=f'Домашнее задание отправленно!')
    file = FSInputFile(path=path)
    await bot.send_document(int(USER_ID_DOWNLOAD), file, caption='Тебе пришло новое домашнее задание!')
    save_to_file()
    await state.clear()

@dp.callback_query(F.data == "start")
async def cb_menu(callback: types.CallbackQuery):
    await cmd_menu(callback.message)
    await callback.answer()

@dp.message(F.text == "Домашнее задание")
async def send_homework_for_user(message: types.Message):
    path = f'Homework/{return_folder_name(USER_DICT[str(message.from_user.id)]['way'])}/{USER_DICT[str(message.from_user.id)]['name']}-{USER_DICT[str(message.from_user.id)]['last_name']}'
    files = os.listdir(path)
    if len(files) == 0:
        await message.answer('У тебя нет домашнего задания')
    else:
        for file in files:
            file_to_send = FSInputFile(path=path + '/' + file)
            await bot.send_document(int(str(message.from_user.id)), file_to_send)

@dp.message(F.text == "Сдать домашнее задание")
async def send_homework_for_user(message: types.Message):
    path = f'Homework/{return_folder_name(USER_DICT[str(message.from_user.id)]['way'])}/{USER_DICT[str(message.from_user.id)]['name']}-{USER_DICT[str(message.from_user.id)]['last_name']}'
    files = os.listdir(path)
    if len(files) == 0:
        await message.answer('У тебя нет домашнего задания')
    else:
        builder = InlineKeyboardBuilder()
        for file in files:
            builder.add(types.InlineKeyboardButton(text=f'{file}',
                                                   callback_data=f'send_to_admin_{file}'))
        kb = builder.adjust(1).as_markup(resize_keyboard=True)
        await message.answer('Выбери домашнее задание, которое хочешь сдать:', reply_markup=kb)

@dp.callback_query(F.data.startswith('send_to_admin_'))
async def cmd_selected_student_points(call: CallbackQuery, state: FSMContext):
    global FILE_NAME
    FILE_NAME = str(call.data).replace('send_to_admin_', '')
    await call.message.edit_text(f'Отправь, пожалуйста, домашнее задание в виде фотографий')
    await state.set_state(States.STATE_get_media_group)
    await call.answer()

@dp.message(States.STATE_get_media_group)
async def get_media(message: types.Message, state: FSMContext, album: list = None):
    global ADMIN_ID, FILE_NAME
    counter = 0
    caption = (
        f'Студент {USER_DICT[str(message.from_user.id)]['name']} {USER_DICT[str(message.from_user.id)]['last_name']} прислал тебе решение домашнего задания\n'
        f'{FILE_NAME}')
    if album is not None:
        for photo in album:
            await photo.bot.download(file=photo.photo[-1].file_id, destination=f'Answer/p{counter}.jpg')
            counter += 1
        images = []
        images_names = os.listdir('Answer')
        i = 0
        for photo in images_names:
            if i == 0:
                images.append(InputMediaPhoto(type='photo', media=FSInputFile(path=f'Answer/{photo}'), caption=caption))
            else:
                images.append(InputMediaPhoto(type='photo', media=FSInputFile(path=f'Answer/{photo}')))
            i += 1
        await bot.send_media_group(ADMIN_ID, media=images)
        for photo in images_names:
            if os.path.exists(f'Answer/{photo}'):
                os.remove(f'Answer/{photo}')
    else:
        await message.bot.download(file=message.photo[-1].file_id, destination=f'Answer/p1.jpg')
        await bot.send_photo(chat_id=ADMIN_ID, photo=FSInputFile(f'Answer/p{1}.jpg', 'hw'), caption=caption)
        if os.path.exists(f'Answer/p1.jpg'):
            os.remove(f'Answer/p1.jpg')

    await message.answer('Домашнее задание отправлено!')
    path = f'Homework/{return_folder_name(USER_DICT[str(message.from_user.id)]['way'])}/{USER_DICT[str(message.from_user.id)]['name']}-{USER_DICT[str(message.from_user.id)]['last_name']}/{FILE_NAME}'
    if os.path.exists(path):
        os.remove(path)
    USER_DICT[str(message.from_user.id)]['count_homeworks'] -= 1
    USER_DICT[str(message.from_user.id)]['total_homeworks'] += 1
    await state.clear()

@dp.message(F.text == "Баллы за выполнение домашнего задания")
async def send_points(message: types.Message):
    if 'points' not in USER_DICT[str(message.from_user.id)].keys():
        USER_DICT[str(message.from_user.id)]['points'] = 0
    await message.answer(f'Твои баллы: {USER_DICT[str(message.from_user.id)]['points']}')
    save_to_file()

@dp.message(F.text == "Статистика")
async def statics(message: types.Message):
    if 'points' not in USER_DICT[str(message.from_user.id)].keys():
        USER_DICT[str(message.from_user.id)]['points'] = 0

    if 'count_homeworks' not in USER_DICT[str(message.from_user.id)].keys():
        USER_DICT[str(message.from_user.id)]['count_homeworks'] = 0

    if 'total_homeworks' not in USER_DICT[str(message.from_user.id)].keys():
        USER_DICT[str(message.from_user.id)]['total_homeworks'] = 0
    data = USER_DICT[str(message.from_user.id)]
    answer = (f'<b>{data['name']} {data['last_name']}</b>\n'
              f'Твой баланс: <b>{data['points']}</b>\n'
              f'Количество нерешенных домашних заданий: <b>{data['count_homeworks']}</b>\n'
              f'Количество решенных домашних заданий за всё время: <b>{data['total_homeworks']}</b>')
    await message.answer(answer, parse_mode=ParseMode.HTML)
    save_to_file()

@dp.message(F.text == "Решать экзаменационные задачи")
async def exams(message: types.Message):
    global PATH, USER_ID, SIZES
    USER_ID = message.from_user.id
    builder = InlineKeyboardBuilder()
    user = USER_DICT[str(message.from_user.id)]
    if 'picked_tasks' not in USER_DICT[str(message.from_user.id)].keys():
        USER_DICT[str(message.from_user.id)]['picked_tasks'] = []

    if user['way'] == 'ЕГЭ - Информатика':
        rng = range(1, 24)
        PATH = 'exams/EGE'
        SIZES = (5, 5, 5, 5, 3, 1, 1)
    else:
        rng = range(1, 14)
        PATH = 'exams/OGE'
        SIZES = (5, 5, 3, 1, 1)
    for task in rng:
        builder.add(types.InlineKeyboardButton(text=f'{str(task)}',
                                               callback_data=f'task_{str(task)}'))

    builder.button(text=f'Начать решать',callback_data=f'continue')
    builder.button(text=f'Закончить', callback_data=f'end')
    kb = builder.adjust(*SIZES).as_markup(resize_keyboard=True)
    await message.answer(f"Твой профиль: {user['way']}.\nВыбери задания для решения", reply_markup=kb)

@dp.callback_query(F.data.startswith('task_'))
async def multichoice(call: CallbackQuery):
    global USER_ID, SIZES
    pick = str(call.data).replace('task_', '')
    if int(pick) in USER_DICT[str(USER_ID)]['picked_tasks']:
        USER_DICT[str(USER_ID)]['picked_tasks'].remove(int(pick))
    else:
        USER_DICT[str(USER_ID)]['picked_tasks'].append(int(pick))
    user = USER_DICT[str(USER_ID)]
    if user['way'] == 'ЕГЭ - Информатика':
        rng = range(1, 24)
    else:
        rng = range(1, 14)
    builder = InlineKeyboardBuilder()
    for task in rng:
        if task in user['picked_tasks']:
            builder.add(types.InlineKeyboardButton(text=f'{str(task)} ✅',
                                                callback_data=f'task_{str(task)}'))
        else:
            builder.add(types.InlineKeyboardButton(text=f'{str(task)}',
                                                   callback_data=f'task_{str(task)}'))
    builder.add(types.InlineKeyboardButton(text=f'Начать решать',
                                           callback_data=f'continue'))
    builder.button(text=f'Закончить', callback_data=f'end')
    kb = builder.adjust(*SIZES).as_markup(resize_keyboard=True)
    await call.message.edit_text(f"Твой профиль: {user['way']}.\nВыбери задания для решения", reply_markup=kb)
    await call.answer()

@dp.callback_query(F.data.startswith('continue'))
async def tasks(call: CallbackQuery, state: FSMContext):
    global USER_ID, PATH, USER_DICT, ANSWER, MSG
    rnd_num_task = random.choice(USER_DICT[str(USER_ID)]['picked_tasks'])
    rnd_task = random.choice(os.listdir(f'{PATH}/{rnd_num_task}'))
    print(rnd_task)
    with open(f'exams/answers.json') as f:
        print(PATH.split('/')[1], str(rnd_num_task).split('.')[0], int(str(rnd_task).split('.')[0]) - 1)
        ANSWER = json.load(f)[PATH.split('/')[1]][str(rnd_num_task).split('.')[0]][int(str(rnd_task).split('.')[0]) - 1]
    b1 = InlineKeyboardButton(text='Продолжить', callback_data='continue')
    b2 = InlineKeyboardButton(text='Закончить', callback_data='end')
    kb = InlineKeyboardMarkup(inline_keyboard=[[b1, b2]])
    await call.message.delete()
    MSG = await call.message.answer_photo(photo=FSInputFile(f'{PATH}/{rnd_num_task}/{rnd_task}', filename='task'), caption='Попробуй решить и присылай решение', reply_markup=kb)
    await state.set_state(States.STATE_send_exam)
    await call.answer()

@dp.message(States.STATE_send_exam)
async def get_answer(message: types.Message, state: FSMContext):
    global USER_ID, PATH, USER_DICT, ANSWER
    b1 = InlineKeyboardButton(text='Продолжить', callback_data='continue')
    b2 = InlineKeyboardButton(text='Закончить', callback_data='end')
    kb = InlineKeyboardMarkup(inline_keyboard=[[b1, b2]])
    if message.text == str(ANSWER):
        USER_DICT[str(USER_ID)]['points'] += 1
        await MSG.delete()
        await message.answer(f'Ты правильно решил задачу!\nТвой баланс: {USER_DICT[str(USER_ID)]['points']}', reply_markup=kb)
        save_to_file()
    else:
        await MSG.delete()
        await message.answer(f'Ты неправильно решил задачу!', reply_markup=kb)
    await state.clear()

@dp.callback_query(F.data.startswith('end'))
async def tasks(call: CallbackQuery):
    global USER_ID, PATH, USER_DICT
    if str(USER_ID) in USER_DICT.keys():
        USER_DICT[str(USER_ID)]['picked_tasks'] = []
    USER_ID = 0
    PATH = ''
    await call.message.delete()
    save_to_file()
    await call.answer()

@dp.callback_query(F.data == "add_dates")
async def dates(callback: types.CallbackQuery):
    await Functions.show_students(USER_DICT, 'dates_', 'Выбери студента', callback)
    await callback.answer()

@dp.callback_query(F.data.startswith('dates_'))
async def dates_send(call: CallbackQuery, state: FSMContext):
    global USER_ID
    USER_ID = str(call.data).replace('dates_', '')
    USER_DICT[USER_ID]['dates'] = []
    await call.message.answer(f"Введите расписание в формате <День недели>:<Ч:М (мск)>\n"
                              f"Каждую дату вводите с новой строки")
    await state.set_state(States.STATE_add_date)
    await call.answer()

@dp.message(States.STATE_add_date)
async def get_dates(message: types.Message, state: FSMContext):
    schedule = str(message.text).split('\n')
    for data in schedule:
        USER_DICT[USER_ID]['dates'].append(data)
    await message.answer(f"Расписание добавлено!")
    await state.clear()
    save_to_file()


@dp.callback_query(F.data == "change_dates")
async def change_dates(callback: types.CallbackQuery):
    await Functions.show_students(USER_DICT, 'student_change_', 'Выбери студента', callback)
    await callback.answer()

@dp.callback_query(F.data.startswith('student_change_'))
async def change_dates_select_date(call: CallbackQuery):
    global USER_ID
    USER_ID = str(call.data).replace('student_change_', '')
    builder = InlineKeyboardBuilder()
    for date_to_change in USER_DICT[USER_ID]['dates']:
        builder.add(types.InlineKeyboardButton(text=f'{date_to_change}', callback_data=f'change_dates_{date_to_change}'))
    kb = builder.adjust(3).as_markup(resize_keyboard=True)
    await call.message.answer(f"Выбери дату", reply_markup=kb)
    await call.answer()

@dp.callback_query(F.data.startswith('change_dates_'))
async def change_dates_in_dict(call: CallbackQuery, state: FSMContext):
    global USER_ID, DATA
    DATA = str(call.data).replace('change_dates_', '')
    await call.message.answer(f"Введите новую дату и время в формате: <День недели>:<Ч:М (мск)>")
    await state.set_state(States.STATE_edit_date)
    await call.answer()

@dp.message(States.STATE_edit_date)
async def final_edit_dates(message: types.Message, state: FSMContext):
    schedule = str(message.text)
    ind = USER_DICT[USER_ID]['dates'].index(DATA)
    USER_DICT[USER_ID]['dates'][ind] = schedule
    await message.answer(f"Расписание изменено!")
    await state.clear()
    await bot.send_message(chat_id=USER_ID, text=f'Ваше расписание изменено!\n'
                                                 f'{DATA} --> {schedule}')
    save_to_file()

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
