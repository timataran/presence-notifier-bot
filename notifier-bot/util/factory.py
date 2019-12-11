import logging
import telebot

import settings


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(settings.get_log_format())
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_telebot():
    bot_settings = settings.get_bot_settings()
    return telebot.TeleBot(bot_settings.get('token'))

