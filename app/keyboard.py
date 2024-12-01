#keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.read_excel import *

back_lang = {"rus":"Назад",
			"kaz":"Артқа",
			"eng":"Back"}

def generate_keyboard(buttons,back_text="Back", back=True):
	keyboard = [[InlineKeyboardButton(text=btn[0], callback_data=btn[1])] for btn in buttons]
	if back:
		keyboard.append([InlineKeyboardButton(text=back_text, callback_data="back")])
	return InlineKeyboardMarkup(inline_keyboard=keyboard)

# PROFESSION
def generate_profession(school, lang):
	value = get_name_and_index_and_info(school,lang)
	return [generate_keyboard(value[0],back_text=back_lang[lang]),
			value[1]]

# INFO
def generate_info_text(school, ind, lang):
	buttons = {"rus":[['Сфера профессиональной деятельности','pro_act'],
					['Профильные предметы на ЕНТ','admission'],
					['Проходной балл','score'],
					['Контакты','contact']],
				"kaz":[['Кəсіби қызмет саласы','pro_act'],
					['Оқуға түсу пәндері','admission'],
					['Өту балы','score'],
					['Байланыс','contact']],
				"eng":[['The field of professional activity','pro_act'],
					['Specialized subjects at the UNT','admission'],
					['Passing score','score'],
					['Contacts','contact']]}
	return [generate_keyboard(buttons[lang],back_text=back_lang[lang]),
			get_text_for_info(school, ind, lang)]


# LANGUAGE
language = [generate_keyboard([["ҚАЗ","kaz"],
								["РУС","rus"],
								["ENG","eng"]], back=False),
			"Привет, выберай язык"]

# SCHOOL
school = {"rus":[generate_keyboard([['ШНоЗ','SoG']],back_text='Назад'),
			get_text_answer("ASthelang","rus")],
		"kaz":[generate_keyboard([['ЖтғМ',"SoG"]],back_text="Артқа"),
			get_text_answer("ASthelang","kaz")],
		"eng":[generate_keyboard([['SoG',"SoG"]],back_text="Back"),
			get_text_answer("ASthelang","eng")]
}




back = {"rus":generate_keyboard([],back_text='Назад'),
		"kaz":generate_keyboard([],back_text='Артқа'),
		"eng":generate_keyboard([],back_text='Back')}

profession_index = get_profession_index(['SoG'])