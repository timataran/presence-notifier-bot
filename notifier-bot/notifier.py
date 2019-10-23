import logging
import telebot

from connection_monitor import ConnectionMonitor
import settings


class Notifier:
    def __init__(self):
        self.bot_settings = settings.get_bot_settings()
        self.bot = self._build_bot_object(self.bot_settings.get('token'))
        self.MAC_MAP = settings.get_residents()
        self.bot_users = []

    def start(self):
        self.bot.add_message_handler({
            'function': self._handle_message,
            'filters': {'content_types': ['text']}
        })
        monitor = ConnectionMonitor(self._notify_users)
        monitor.start()
        self.bot.polling(none_stop=True, interval=self.bot_settings.get('polling_interval'))

    def _handle_message(self, message):
        if message.text == '/help':
            self.bot.send_message(message.from_user.id, 'Sorry, no help message yet')

        if message.text == '/subscribe':
            self.bot_users.append(message.from_user.id)
            self.bot.send_message(message.from_user.id, "subscription is done")

    def _notify_users(self, message):
        logging.info(f'Message for users {message}')
        for user in self.bot_users:
            self.bot.send_message(user, message)

    @staticmethod
    def _build_bot_object(token):
        return telebot.TeleBot(token)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Start notifier bot')
    notifier = Notifier()
    notifier.start()
