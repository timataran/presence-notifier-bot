import os
import json

ROUTER_SETTINGS = ['ip', 'username', 'password']

BOT_SETTINGS = ['token', 'polling_interval', 'router_polling_period']
BOT_DEFAULTS = {'polling_interval': 3, 'router_polling_period': 3}

RESIDENTS = ['json']

ALLOWED = ['users']


def get_router_settings():
    return _load_from_env('router', ROUTER_SETTINGS)


def get_bot_settings():
    return _load_from_env('bot', BOT_SETTINGS, **BOT_DEFAULTS)


def get_residents():
    data = _load_from_env('residents', RESIDENTS)
    return json.loads(data.get('json'))


def get_allowed_users():
    data = _load_from_env('allowed', ALLOWED)
    return json.loads(data.get('users'))


def get_log_format():
    return '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'


def _load_from_env(prefix, variable_names, **defaults):
    defaults = {} if defaults is None else defaults

    settings = {v: os.getenv(f'{prefix}_{v}'.upper()) for v in variable_names}

    for field, value in settings.items():
        if settings.get(field) is None:
            default_value = defaults.get(field)
            if default_value is not None:
                settings[field] = default_value
            else:
                raise Exception(f'The required variable {field} is not set in environment')

    return settings

