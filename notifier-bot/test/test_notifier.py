from unittest import TestCase
from unittest.mock import patch, Mock

from notifier import Notifier


@patch('bot.command.settings')
class TestNotifierStarter(TestCase):

    @patch('notifier.EventDispatcher')
    def test_create_event_dispatcher_on_init(self, dispatcher_constructor_mock, settings):
        dispatcher = Mock()
        dispatcher_constructor_mock.return_value = dispatcher

        notifier = Notifier()

        self.assertEqual(dispatcher, notifier.get_dispatcher())

    @patch('notifier.EventDispatcher')
    @patch('notifier.ConnectionMonitor')
    @patch('notifier.Receiver')
    @patch('notifier.Sender')
    def test_pass_dispatcher_to_components_on_start(self, sender, receiver, connection_monitor, dispatcher, settings):
        event_dispatcher = Mock()
        dispatcher.return_value = event_dispatcher

        notifier = Notifier()
        notifier.start()

        sender.assert_called_with(event_dispatcher)
        receiver.assert_called_with(event_dispatcher)
        connection_monitor.assert_called_with(event_dispatcher)

    @patch('notifier.EventDispatcher')
    @patch('notifier.ConnectionMonitor')
    @patch('notifier.Receiver')
    @patch('notifier.Sender')
    def test_invoke_connection_monitor_start(self, sender, receiver, connection_monitor, dispatcher, settings):
        monitor = Mock()
        connection_monitor.return_value = monitor

        notifier = Notifier()
        notifier.start()

        monitor.start.assert_called()

    @patch('notifier.EventDispatcher')
    @patch('notifier.ConnectionMonitor')
    @patch('notifier.Receiver')
    @patch('notifier.Sender')
    def test_invoke_receiver_start(self, sender, receiver, connection_monitor, dispatcher, settings):
        bot_receiver = Mock()
        receiver.return_value = bot_receiver

        notifier = Notifier()
        notifier.start()

        bot_receiver.start.assert_called()

    @patch('notifier.EventDispatcher')
    @patch('notifier.ConnectionMonitor')
    @patch('notifier.Receiver')
    @patch('notifier.Sender')
    @patch('notifier.Help')
    @patch('notifier.Subscribe')
    @patch('notifier.MyId')
    def test_create_commands(self,
                             cmd_id,
                             cmd_subscribe,
                             cmd_help,
                             sender, receiver, connection_monitor, dispatcher, settings):
        event_dispatcher = Mock()
        dispatcher.return_value = event_dispatcher

        notifier = Notifier()
        notifier.start()

        cmd_help.assert_called_with(event_dispatcher)
        cmd_id.assert_called_with(event_dispatcher)
        cmd_subscribe.assert_called_with(event_dispatcher)

