from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from app.tgbot.keyboards.users_board import event_board
from app.tgbot.utils.file_management import get_pdf_path
from aiogram.types import (CallbackQuery, Message, FSInputFile)
from app.tgbot.keyboards.inline_board import select_mode_kb
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from app.infrastructure.database.database.db import DB
from app.models.basemodels import EventModel
import logging
from datetime import datetime
import pandas as pd
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


event_router = Router()

user_dict: dict[int, dict[str, str | int | bool]] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_start_dt = State()  # Дата начала события
    fill_end_dt = State()   # Дата окончания события
    fill_name = State()     # Название события
    fill_mode = State()     # Тип события
    fill_place = State()     # Место проведения события
    fill_description = State()  # Описание события (необязательно)

@event_router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего.\n\n'
             'Чтобы перейти к заполнению анкеты.'
    )

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@event_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Все не сохраненные данные были удалены',
        reply_markup=event_board()
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()

# Этот хэндлер будет срабатывать на команду /fillform
# и переводить бота в состояние ожидания ввода имени
@event_router.message(F.text == 'Внести событие', StateFilter(default_state))
async def process_event_command(message: Message, state: FSMContext):
    await message.answer(text='Введите дату начала события\nФормат ввода "01-01-2025".',
                         reply_markup=await SimpleCalendar().start_calendar())
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_start_dt)


@event_router.callback_query(SimpleCalendarCallback.filter(), FSMFillForm.fill_start_dt)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(start_date=date.strftime("%d-%m-%Y"))
        await callback_query.message.answer(
            text=f'Вы выбрали дату начала: {date.strftime("%d-%m-%Y")}\n\n'
            'Теперь введите дату окончания события в формате "ДД-ММ-ГГГГ".',
            reply_markup=await SimpleCalendar().start_calendar()
            )
        await state.set_state(FSMFillForm.fill_end_dt)


@event_router.message(StateFilter(FSMFillForm.fill_start_dt))
async def warning_not_start_dt(message: Message):
    await message.answer(
        text='Неверный формат даты\n\n'
             'Пожалуйста, введите дату в формате "01-01-2025"\n\n'
             'Если вы хотите прервать внесение события - '
             'отправьте команду /cancel'
    )

@event_router.callback_query(SimpleCalendarCallback.filter(), FSMFillForm.fill_end_dt)
async def process_end_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(end_date=date.strftime("%d-%m-%Y"))
        await callback_query.message.delete()
        await callback_query.message.answer(
            text=f'Вы выбрали дату окончания: {date.strftime("%d-%m-%Y")}\n\n'
            'Теперь введите название события.'
        )
        await state.set_state(FSMFillForm.fill_name)


@event_router.message(StateFilter(FSMFillForm.fill_end_dt))
async def warning_not_end_dt(message: Message):
    await message.answer(
        text='Неверный формат даты\n\n'
             'Пожалуйста, введите дату в формате "01-01-2025"\n\n'
             'Если вы хотите прервать внесение события - '
             'отправьте команду /cancel'
    )

@event_router.message(StateFilter(FSMFillForm.fill_name), F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        'Введите тип события',
        reply_markup=select_mode_kb()
    )
    await state.set_state(FSMFillForm.fill_mode)


@event_router.message(StateFilter(FSMFillForm.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='Пустое сообщение\nВведите название события'
    )


@event_router.callback_query(StateFilter(FSMFillForm.fill_mode),
                             F.data.in_(['permanent', 'temporary']))
async def process_mode(callback_query: CallbackQuery,  state: FSMContext):
    await state.update_data(mode=callback_query.data)
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Введите место события'
    )
    await state.set_state(FSMFillForm.fill_place)


@event_router.message(StateFilter(FSMFillForm.fill_mode))
async def warning_not_mode(message: Message):
    await message.answer(
        text='Выберите тип события (временное, постоянное)'
    )


@event_router.message(StateFilter(FSMFillForm.fill_place), F.text)
async def process_place(message: Message, state: FSMContext):
    await state.update_data(place=message.text)
    await message.answer(
        text='Введите описание события'
    )
    await state.set_state(FSMFillForm.fill_description)


@event_router.message(StateFilter(FSMFillForm.fill_place))
async def warning_not_place(message: Message):
    await message.answer(
        text='Выберите место события'
    )


@event_router.message(StateFilter(FSMFillForm.fill_description), F.text)
async def process_description(message: Message, state: FSMContext, db: DB):
    await state.update_data(description=message.text)
    # user_dict[message.from_user.id] = await state.get_data()
    user_data = await state.get_data()
    logger.info(f"Данные из состояния: {user_data}")
    start_date_d = datetime.strptime(user_data.get('start_date'), '%d-%m-%Y')
    end_date_d = datetime.strptime(user_data.get('end_date'), '%d-%m-%Y')
    await db.events.add(
            user_id=message.from_user.id,
            start_dt=start_date_d,
            end_dt=end_date_d,
            name=user_data.get('name'),
            mode=user_data.get('mode'),
            place=user_data.get('place'),
            description=user_data.get('description'),
            duration=(end_date_d-start_date_d).days
        )
    await state.clear()
    await message.answer(
        text='Спасибо! Ваши данные сохранены!\n\n'
    )
    # Отправляем в чат сообщение с предложением посмотреть свою анкету
    await message.answer(
        text='Чтобы посмотреть данные вашей '
             'анкеты - отправьте команду /showdata'
    )

@event_router.message(Command(commands='showdata'), StateFilter(default_state))
async def process_showdata_command(message: Message, db: DB):
    # Отправляем пользователю анкету, если она есть в "базе данных"
    event_record: EventModel | None = await db.events.get_event(user_id=message.from_user.id)
    event_info = (
        f"Name: {event_record.name}\n"
        f"User ID: {event_record.user_id}\n"
        f"Created: {event_record.created}\n"
        f"Start Date: {event_record.start_dt}\n"
        f"End Date: {event_record.end_dt}\n"
        f"Mode: {event_record.mode}\n"
        f"Place: {event_record.place}\n"
        f"Description: {event_record.description}\n"
        f"Duration: {event_record.duration} seconds"
    )
    await message.answer(event_info)

@event_router.message(F.text == 'Посмотреть события', StateFilter(default_state))
async def show_events(message: Message, db: DB):

    event_load: EventModel | None = await db.events.load_events(user_id=message.from_user.id)
    columns = [
            "Дата начала",
            "Дата окончания",
            "Название события",
            "Место проведения",
            "Описание"
        ]

    # Создание DataFrame
    df = pd.DataFrame(event_load, columns=columns)
    df_message = df[['Название события']]
    pdf_path = get_pdf_path(df)

    await message.answer(text=f"<pre>{df_message.to_string(index=False,header=False)}</pre>", parse_mode='HTML')
    # Отправка PDF-файла
    await message.answer_document(document=FSInputFile(pdf_path))

    # Удаление файла после отправки
    os.remove(pdf_path)
