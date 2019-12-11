import time

import settings
from util import factory

logger = factory.get_logger('Bot receiver')


class Receiver:
    def __init__(self, event_dispatcher):
        self._bot_settings = settings.get_bot_settings()
        self._bot = factory.get_telebot()
        self._event_dispatcher = event_dispatcher

    def start(self):
        self._bot.add_message_handler({
                'function': self.handle_message,
                'filters': {'content_types': ['text']}
            })
        self._start_polling_loop()

    def _start_polling_loop(self):
        while True:
            try:
                self._bot.polling(none_stop=True, interval=self._bot_settings.get('polling_interval'))
            except Exception as err:
                logger.error(err)
                time.sleep(1)

    def handle_message(self, message):
        if message.text == '/help':
            self._event_dispatcher.dispatch(
                'send_message',
                user=message.from_user.id,
                text='Sorry, no help message yet'
            )

        if message.text == '/subscribe':
            self._event_dispatcher.dispatch('subscribe_user', user=message.from_user.id)
            self._event_dispatcher.dispatch('send_message', user=message.from_user.id, text='subscription is done')