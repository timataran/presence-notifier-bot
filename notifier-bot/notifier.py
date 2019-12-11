from util import factory
from bot.sender import Sender
from bot.receiver import Receiver
from connection_monitor import ConnectionMonitor
from util.event_dispatcher import EventDispatcher

logger = factory.get_logger('Notifier starter')


class Notifier:
    def __init__(self):
        self._event_dispatcher = EventDispatcher()

    def start(self):
        connection_monitor = ConnectionMonitor(self._event_dispatcher)
        connection_monitor.start()
        bot_sender = Sender(self._event_dispatcher)
        bot_receiver = Receiver(self._event_dispatcher)
        bot_receiver.start()

    def get_dispatcher(self):
        return self._event_dispatcher


if __name__ == '__main__':
    logger.info('Start notifier bot')
    notifier = Notifier()
    notifier.start()
