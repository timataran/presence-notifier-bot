import time

from util import factory, settings

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
                text='Available commands are /myID and /subscribe'
            )

        if message.text == '/subscribe':
            self._event_dispatcher.dispatch('subscribe_user', user=message.from_user.id)
            self._event_dispatcher.dispatch('send_message', user=message.from_user.id, text='subscription is done')

        if message.text == '/myID':
            user_id = message.from_user.id
            self._event_dispatcher.dispatch('send_message', user=user_id, text=f'{user_id}')
