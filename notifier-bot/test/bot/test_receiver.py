from unittest import TestCase
from unittest.mock import Mock, patch
from bot.receiver import Receiver

bot = Mock()
bot.polling.side_effect = Exception('Polling failed')
bot_settings = {'polling_interval': 3}


# noinspection PyBroadException
@patch('bot.receiver.settings', **{'get_bot_settings.return_value': bot_settings})
@patch('bot.receiver.factory', **{'get_telebot.return_value': bot})
class TestBotSender(TestCase):

    @patch('bot.receiver.time', **{'sleep.side_effect': Exception('Test')})
    def test_add_message_handler_to_bot_on_start(self, factory_mock, settings_mock, time_mock):
        event_dispatcher = Mock()
        receiver = Receiver(event_dispatcher)

        try:
            receiver.start()
        except Exception:
            bot.add_message_handler.assert_called_with({
                'function': receiver.handle_message,
                'filters': {'content_types': ['text']}
            })

    @patch('bot.receiver.time', **{'sleep.side_effect': Exception('Test')})
    def test_run_message_polling_on_start(self, factory_mock, settings_mock, time_mock):
        event_dispatcher = Mock()
        receiver = Receiver(event_dispatcher)

        try:
            receiver.start()
        except Exception:
            bot.polling.assert_called_with(
                none_stop=True,
                interval=bot_settings.get('polling_interval')
            )

    def test_dispatch_event_on_handle_help_message(self, factory_mock, settings_mock):
        event_dispatcher = Mock()
        receiver = Receiver(event_dispatcher)

        receiver.handle_message(self._get_message_mock(text='/help', sender='user_id'))

        event_dispatcher.dispatch.assert_called_with('command_help', user='user_id')

    def test_dispatch_events_on_handle_subscribe_message(self, factory_mock, settings_mock):
        event_dispatcher = Mock()
        receiver = Receiver(event_dispatcher)

        receiver.handle_message(self._get_message_mock(text='/subscribe', sender='user_id'))

        event_dispatcher.dispatch.assert_called_with('command_subscribe', user='user_id')

    def test_dispatch_event_on_handle_my_id(self, factory_mock, settings_mock):
        event_dispatcher = Mock()
        receiver = Receiver(event_dispatcher)

        receiver.handle_message(self._get_message_mock(text='/myID', sender='user_id'))

        event_dispatcher.dispatch.assert_any_call('command_my_id', user='user_id')

    @staticmethod
    def _get_message_mock(**kwargs):
        message = Mock()
        message.text = kwargs.get('text')
        message.from_user.id = kwargs.get('sender')

        return message

