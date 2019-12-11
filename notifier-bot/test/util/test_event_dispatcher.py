from unittest import TestCase
from unittest.mock import Mock

from util.event_dispatcher import EventDispatcher


class TestEventDispatcher(TestCase):

    def test_add_listener(self):
        def event_handler():
            pass

        dispatcher = EventDispatcher()
        event_name = 'foo'

        dispatcher.add_listener(event_name, event_handler)

        self.assertListEqual([event_handler], dispatcher.get_listeners(event_name))

    def test_get_listeners(self):
        def event_handler_one():
            pass

        def event_handler_two():
            pass

        dispatcher = EventDispatcher()
        event_name = 'foo'

        dispatcher.add_listener(event_name, event_handler_one)
        dispatcher.add_listener(event_name, event_handler_two)

        self.assertListEqual([event_handler_one, event_handler_two], dispatcher.get_listeners(event_name))

    def test_invoke_listeners_on_dispatch(self):
        dispatcher = EventDispatcher()
        event_name = 'foo'

        handler_one = Mock()
        handler_one.handle.response_value = None
        dispatcher.add_listener(event_name, handler_one.handle)

        handler_two = Mock()
        handler_two.handle.response_value = None
        dispatcher.add_listener(event_name, handler_two.handle)

        event_payload = {'foo': 'bar'}
        dispatcher.dispatch(event_name, **event_payload)

        handler_one.handle.assert_called_with(**event_payload)
        handler_two.handle.assert_called_with(**event_payload)
