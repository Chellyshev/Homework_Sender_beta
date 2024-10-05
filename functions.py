from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Functions:
    @staticmethod
    async def show_students(USER_DICT: dict ,callback_text: str, message_text: str, callback: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        for user_id in USER_DICT.keys():
            builder.add(types.InlineKeyboardButton(text=f'{USER_DICT[user_id]['name']}',
                                                   callback_data=f'{callback_text}{user_id}'))
        kb = builder.adjust(3).as_markup(resize_keyboard=True)
        await callback.message.answer(f"{message_text}", reply_markup=kb)

    @staticmethod
    def translate_num_to_rus(number: int):
        if 5 <= number % 100 <= 20:
            return 'баллов'
        elif number % 10 == 1:
            return 'балл'
        elif number % 10 in [2, 3, 4]:
            return 'балла'
        else:
            return 'баллов'