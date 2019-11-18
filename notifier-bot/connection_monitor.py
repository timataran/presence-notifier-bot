import time
from threading import Thread

from router.mac_extractor import ActiveMacExtractor
import settings
import utils

logger = utils.get_logger('Connection monitor')


class ConnectionMonitor:
    def __init__(self, notification_function):
        self._notification_function = notification_function
        self._execution_thread = Thread(target=self._monitor_connections)
        self.status_map = {}
        self.MAC_MAP = settings.get_residents()

    def start(self):
        self._execution_thread.start()

    def _monitor_connections(self):
        logger.info('Monitoring started')
        while True:
            try:
                self.check_connections()
            except Exception as err:
                logger.error(err)
            bot_settings = settings.get_bot_settings()
            time.sleep(bot_settings.get('router_polling_period'))

    def check_connections(self):
        mac_extractor = ActiveMacExtractor
        active_macs = mac_extractor.get_list()

        for name, mac in self.MAC_MAP.items():
            status = mac in active_macs

            if status != self.status_map.get(name):
                self.status_map[name] = status
                action = 'in' if status else 'out'
                self._notification_function(f"{name} {action}")
