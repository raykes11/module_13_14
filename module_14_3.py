from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from api_bot import API

api = API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()

button_cal = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')

kb.add(button_cal, button_info)
kb.add(button_buy)

kb.resize_keyboard = True

ikb = InlineKeyboardMarkup()

i_button_cal = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')

ikb.add(i_button_cal, i_button_formula)

buy_ikb = InlineKeyboardMarkup(inline_keyboard=[[product1, product2, product3, product4]])



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_messanges(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=ikb)


@dp.callback_query_handler(text='calories')
async def get_formulas(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def set_age(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        i += 1
        with open(f'{i}.png', 'rb') as img:
            await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
            await message.answer_photo(img)
            await asyncio.sleep(1)
    await message.answer('Выберите продукт для покупки:', reply_markup=buy_ikb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()


@dp.message_handler()
async def all_messanges(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
