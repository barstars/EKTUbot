#data_select.py
import sqlite3
import json

def init_db():
    db = sqlite3.connect('user_datas/data_user.db')
    cur = db.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS data(
        user_id INTEGER,
        branch TEXT,
        message_id INTEGER
    )
    """)
    db.commit()
    db.close()

def creater_data(user_id, data, message_id=None):
	with sqlite3.connect('user_datas/data_user.db') as db:
		cur = db.cursor()

		data_json = json.dumps(data)

		# Проверяем наличие пользователя
		cur.execute("SELECT user_id FROM data WHERE user_id = ?", (user_id,))
		result = cur.fetchone()

		if (result and message_id):
			# Если пользователь существует, обновляем запись
			cur.execute("UPDATE data SET branch = ?, message_id = ? WHERE user_id = ?", (data_json, message_id, user_id))
		elif (result):
			cur.execute("UPDATE data SET branch = ? WHERE user_id = ?", (data_json, user_id, ))
		else:
			# Если пользователя нет, добавляем новую запись
			cur.execute("INSERT INTO data (user_id, branch) VALUES (?, ?)", (user_id, data_json))

		# Сохраняем изменения и закрываем соединение
		db.commit()


def get_branch_data(user_id,expect_a_result=0):
	with sqlite3.connect('user_datas/data_user.db') as db:
		cur = db.cursor()

		cur.execute("SELECT branch FROM data WHERE user_id = ?", (user_id,))
		row = cur.fetchone()
	result = json.loads(row[0]) if row else None
	return result #[branch]

def get_message_id(user_id):
	with sqlite3.connect('user_datas/data_user.db') as db:
		cur = db.cursor()

		cur.execute("SELECT message_id FROM data WHERE user_id = ?", (user_id,))
		result = cur.fetchone()

	return result[0] if result else None