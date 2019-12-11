from util import factory

logger = factory.get_logger('Bot sender')


class Sender:
    def __init__(self, event_dispatcher):
        self._bot = factory.get_telebot()
        self._bot_users = []
        self.event_dispatcher = event_dispatcher
        event_dispatcher.add_listener('send_message', self.send_message)
        event_dispatcher.add_listener('send_broadcast', self.send_broadcast)
        event_dispatcher.add_listener('subscribe_user', self.subscribe_user)

    def send_message(self, **kwargs):
        user = kwargs.get('user')
        text = kwargs.get('text')
        logger.info(f'Message for {user}: {text}')
        self._bot.send_message(user, text)

    def send_broadcast(self, **kwargs):
        text = kwargs.get('text')
        logger.info(f'Message for users {text}')
        for user in self._bot_users:
            self._bot.send_message(user, text)

    def subscribe_user(self, **kwargs):
        user = kwargs.get('user')
        logger.info(f'Subscribe user {user}')
        self._bot_users.append(user)

    def get_subscribed_users(self):
        return self._bot_users
