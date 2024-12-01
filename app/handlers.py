#handlers.py
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.filters import Command
from aiogram import Bot

import app.keyboard as kb

from aiogram import Router, F, Bot

# import DB
from app.data_select import *

# read excel
from app.read_excel import *

router = Router()

# Инициализация базы данных при запуске
init_db()

url="datas/images/"

# LANGUAGE AND START
@router.message(Command('start'))
async def cmd_start(message:Message, bot: Bot):
	media_url = FSInputFile(f'{url}ektu_logo.png')  # URL изображения
	chat = await bot.send_photo(
	    chat_id=message.chat.id,  # ID чата
	    photo=media_url,                   # URL или файл изображения
	    caption=kb.language[1],            # Подпись к изображению
	    reply_markup=kb.language[0]        # Инлайн-клавиатура
	)
	creater_data(message.from_user.id, [],message_id=chat.message_id)

# SCHOOL
@router.callback_query(F.data.in_({"rus", "kaz", "eng"}))
async def school(callback: CallbackQuery, bot: Bot):
	media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.school[callback.data][1])
	await bot.edit_message_media(
		chat_id=callback.message.chat.id,
		message_id=get_message_id(callback.from_user.id),
		media=media,  # Изображение
		reply_markup=kb.school[callback.data][0]  # Клавиатура, если нужна
		)
	creater_data(callback.from_user.id, [callback.data])

# PROFESSION
@router.callback_query(F.data.in_({"SoG"}))
async def profession(callback: CallbackQuery, bot: Bot):
	user_id = callback.from_user.id
	branch = get_branch_data(user_id,1)
	if (not branch):
		media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.language[0])
		await bot.edit_message_media(chat_id=callback.message.chat.id,
			message_id=get_message_id(callback.from_user.id),
			media=media, reply_markup=kb.language[0])
		return None
	lang = branch[0]
	media = InputMediaPhoto(media=FSInputFile(f'{url}{callback.data}.png'),caption=kb.generate_profession(callback.data,lang)[1])
	await bot.edit_message_media(
		chat_id=callback.message.chat.id,
		message_id=get_message_id(callback.from_user.id),
		media=media,  # Изображение
		reply_markup=kb.generate_profession(callback.data,lang)[0]  # Клавиатура, если нужна
    )

	creater_data(user_id, [lang,callback.data])

# INFO
@router.callback_query(F.data.in_(kb.profession_index))
async def get_info(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    branch = get_branch_data(user_id, 2)

    if not branch:
    	media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.language[1])
    	await bot.edit_message_media(
    		chat_id=callback.message.chat.id,
    		message_id=get_message_id(callback.from_user.id),
    		media=media,
    		reply_markup=kb.language[0]
    		)
    	return None

    lang = branch[0]
    school = branch[1]

    text = kb.generate_info_text(school,callback.data,lang)

    # Используем edit_message_media для обновления медиа и текста
    media = InputMediaPhoto(media=FSInputFile(f'{url}{callback.data}.png'),caption=text[1])  # Передаем путь к фото через named аргумент 'media'
    await bot.edit_message_media(
        chat_id=callback.message.chat.id,
        message_id=get_message_id(callback.from_user.id),
        media=media,  # Изображение
        reply_markup=text[0]  # Клавиатура, если нужна
    )

    creater_data(user_id, [lang, school, callback.data])

# GET INFO
@router.callback_query(F.data.in_({"pro_act", "admission", "score", "contact"}))
async def info(callback: CallbackQuery, bot: Bot):
	user_id = callback.from_user.id
	branch = get_branch_data(user_id,3)
	if not branch:
		media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.kb.language[1])
		await bot.edit_message_media(
			chat_id=callback.message.chat.id,
			message_id=get_message_id(callback.from_user.id),
			media=media,
			reply_markup=kb.language[0]
			)
		return None
	lang = branch[0]
	school = branch[1]
	profession = branch[2]

	media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=read_excel_cell(school,profession,lang,callback.data))
	await bot.edit_message_media(chat_id=callback.message.chat.id,
		message_id=get_message_id(callback.from_user.id),
		media=media,
		reply_markup=kb.back[lang])
	
	creater_data(user_id, [lang,school,profession,callback.data])

# BACK
@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery, bot: Bot):
	user_id = callback.from_user.id
	branch = get_branch_data(user_id,1)
	if (not branch):
		media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.language[1])
		await bot.edit_message_media(chat_id=callback.message.chat.id,
			message_id=get_message_id(callback.from_user.id),
			media=media, reply_markup=kb.language[0])
		creater_data(user_id, [])
		return None

	if (len(branch) > 1):
		branch.pop()
		lang = branch[0]
		
		if (len(branch) == 1):
			media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.school[lang][1])
			await bot.edit_message_media(chat_id=callback.message.chat.id,
				message_id=get_message_id(callback.from_user.id),
				media=media,
				reply_markup=kb.school[lang][0])
		elif (len(branch) == 2):
			text_and_button = kb.generate_profession(branch[1],lang)
			media = InputMediaPhoto(media=FSInputFile(f'{url}{branch[1]}.png'),caption=text_and_button[1])
			await bot.edit_message_media(chat_id=callback.message.chat.id,
				message_id=get_message_id(callback.from_user.id),
				media=media,
				reply_markup=text_and_button[0])
		elif (len(branch) == 3):
			text = kb.generate_info_text(branch[1],branch[2],lang)
			media = InputMediaPhoto(media=FSInputFile(f'{url}{branch[-1]}.png'),caption=text[1])
			await bot.edit_message_media(chat_id=callback.message.chat.id,
				message_id=get_message_id(callback.from_user.id),
				media=media,
				reply_markup=text[0])
		creater_data(user_id, branch)
			
	else:
		media = InputMediaPhoto(media=FSInputFile(f'{url}ektu_logo.png'),caption=kb.language[1])
		await bot.edit_message_media(chat_id=callback.message.chat.id,
			message_id=get_message_id(callback.from_user.id),
			media=media, reply_markup=kb.language[0])
		creater_data(user_id, [])

# user_id : [lang,school,profession,get_info]