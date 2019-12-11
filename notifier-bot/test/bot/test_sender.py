from unittest import TestCase
from unittest.mock import Mock, patch
from bot.sender import Sender


@patch("bot.sender.factory", **{'get_logger.return_value': Mock()})
class TestBotSender(TestCase):

    def test_subscribe_to_events_on_creation(self, factory_mock):
        event_dispatcher = Mock()
        sender = Sender(event_dispatcher)

        event_dispatcher.add_listener.assert_any_call('send_message', sender.send_message)
        event_dispatcher.add_listener.assert_any_call('send_broadcast', sender.send_broadcast)
        event_dispatcher.add_listener.assert_any_call('subscribe_user', sender.subscribe_user)

    def test_subscribe_users(self, factory_mock):
        event_dispatcher = Mock()
        sender = Sender(event_dispatcher)

        user = 'User-foo'

        sender.subscribe_user(user=user)

        self.assertListEqual([user], sender.get_subscribed_users())

    def test_pass_correct_params_to_send_message_on_send_to_user(self, factory_mock):
        bot = Mock()
        factory_mock.get_telebot.return_value = bot
        event_dispatcher = Mock()
        sender = Sender(event_dispatcher)

        sender.send_message(text='Message text', user='User')

        bot.send_message.assert_called_with('User', 'Message text')

    def test_pass_correct_params_to_send_message_on_broadcast(self, factory_mock):
        bot = Mock()
        factory_mock.get_telebot.return_value = bot
        event_dispatcher = Mock()
        sender = Sender(event_dispatcher)

        sender.subscribe_user(user='User')
        sender.send_broadcast(text='Message text')

        bot.send_message.assert_called_with('User', 'Message text')

    def test_send_message_to_each_subscribed_user_on_broadcast(self, factory_mock):
        bot = Mock()
        factory_mock.get_telebot.return_value = bot
        factory_mock.get_logger.return_value = Mock()
        event_dispatcher = Mock()
        sender = Sender(event_dispatcher)

        for idx in range(0, 5):
            sender.subscribe_user(user=f'User {idx}')

        sender.send_broadcast(text='Message text')

        self.assertEqual(5, bot.send_message.call_count)
