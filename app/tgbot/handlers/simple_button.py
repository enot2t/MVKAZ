from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import requests


API_DOGS_URL = 'https://random.dog/woof.json'
ERROR_TEXT = 'Здесь должна была быть картинка с котиком :('
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'

cat_response: requests.Response
simple_router = Router()


@simple_router.message(F.text == 'Собаки')
async def button_1(message: Message):
    dog_response = requests.get(API_DOGS_URL)
    if dog_response.status_code == 200:
        dog_link = dog_response.json()['url']
        await message.answer_photo(dog_link)
    else:
        await message.answer(ERROR_TEXT)\

@simple_router.message(F.text == 'Кошки')
async def button_1(message: Message):
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()[0]['url']
        await message.answer_photo(cat_link)
    else:
        await message.answer(ERROR_TEXT)
