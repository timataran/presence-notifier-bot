import threading


class EventDispatcher:
    def __init__(self):
        self._lock = threading.RLock()
        self._listeners = {}

    def add_listener(self, event_name, handler):
        with self._lock:
            event_listeners = self._get_event_listeners(event_name)

            event_listeners.append(handler)
            self._listeners[event_name] = event_listeners

    def get_listeners(self, event_name):
        return self._get_event_listeners(event_name)

    def dispatch(self, event_name, **payload):
        event_listeners = self._get_event_listeners(event_name)

        with self._lock:
            for listener in event_listeners:
                listener(**payload)

    def _get_event_listeners(self, event_name):
        return self._listeners.get(event_name) or []

