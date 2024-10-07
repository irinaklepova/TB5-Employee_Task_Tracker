import requests
from config.settings import BOT_TOKEN, TELEGRAM_URL


def send_tg_message(chat_id, message):
    """Функция отправки сообщения в телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)


def create_telegram_message(task):
    """Функция создания сообщения в телеграм"""

    chat_id = task.executor.chat_id
    if chat_id:
        message = (f'Привет, тебе назначена задача - {task.title}. \n'
                   f'Описание задачи: {task.description} \n'
                   f'Дедлайн - {task.time_complete}!')
        send_tg_message(chat_id, message)

