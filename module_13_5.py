from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from api_bot import API
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton



api = API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button_cal = KeyboardButton(text= 'Рассчитать')
button_info = KeyboardButton(text= 'Информация')
kb.add(button_cal,button_info)
kb.resize_keyboard=True
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()




@dp.message_handler(commands=['start'])
async def start_messanges(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)



@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


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
    norma = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age'])+5
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()







@dp.message_handler()
async def all_messanges(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')








if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
