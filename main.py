import io
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pandas as pd

TOKEN = "5806318365:AAGBikHauXUqADld58lsJVNrFYsO--UuSmc"
bot = Bot(token=TOKEN)  #экземпляр класса Bot. В качестве аргумента передается токен
dp = Dispatcher(bot)  #эземпляр класса класса Dispatcher (dp), который в качестве аргумента получит bot, принимает все апдейты и обрабатывает их

classes = {'1A' : '1DIbZMRdqKYi_WalPl5T9kESXmP0Wh2ZpAnuHdBe35-Y', '1B' : '1aaAovvR--ZuCIbDJ_MSYvBxiJBbeujEhoEnVYmqLJCo',
           '1V' : '1Ppm660VIC9_Jy5U-33f90AUUxE0IJTtlBaCgiUc-naQ', '1D' : '1OrYnhtylV5HvE8fcpOUPciBnaQ3HrRLm76u0lUd5aro',
           '1E' : '1jEhtZkRLXqZ7JvPmpDUb_5WeA6IezblBfqfVqqS91P0'}

def work_with_file(cllas):
    SHEET_ID = classes[cllas]
    SHEET_NAME = '1'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    return url

def poisk_num_str(chel):
    num = table.index[table['Код'] == chel].tolist()
    return num

def into_dict(num, colums):
    dict = {}
    for item in colums:
        for info in table[item][num]:
            dict[item] = info
    return dict

@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    await message.answer('Приветствую!\nЭто чат-бот МБОУ СОШ №12.\nЗдесь вы можете посмотреть текущую успеваемость вашего ребёнка.')
    await message.answer('Введите класс ребёнка в формате:\n /class № класса')

@dp.message_handler(commands=['class'])
async def search_class(message: types.Message):
    cllas = message.get_args()
    url = work_with_file(cllas)
    global table
    table = pd.read_csv(url)
    await message.answer('Введите уникальный код в формате:\n/code код ребёнка')

@dp.message_handler(commands=['code'])
async def search_chel(message: types.Message):
    chel = message.get_args()
    num = poisk_num_str(chel)
    colum = table.columns
    dict = into_dict(num, colum)
    answer_message = ""
    for key in dict:
        answer_message += key + ': '+ dict[key] + '\n'
    await message.answer(answer_message)
    search = requests.get('https://source.unsplash.com/featured/?cat')
    photo = io.BytesIO(search.content)
    await bot.send_photo(message.chat.id, photo)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)  #метод start_polling опрашивает сервер, проверяя на нём обновления. Если они есть, то они приходят в Telegram
