from unittest import TestCase
from unittest.mock import Mock, patch

from bot.command import Help, Subscribe, MyId

ALLOWED_USERS = {'111111': 'Alice'}


@patch('bot.command.settings', **{'get_allowed_users.return_value': ALLOWED_USERS})
class TestCommands(TestCase):

    def test_listen_for_help_event(self, settings_mock):
        dispatcher = Mock()

        command = Help(dispatcher)

        dispatcher.add_listener.assert_called_with('command_help', command.execute)

    def test_show_help_for_allowed_user(self, settings_mock):
        dispatcher = Mock()

        command = Help(dispatcher)

        command.execute(user=111111)

        dispatcher.dispatch.assert_called_with(
            'send_message',
            user=111111,
            text='Available commands are /myID and /subscribe'
        )

    def test_show_help_for_restricted_user(self, settings_mock):
        dispatcher = Mock()

        command = Help(dispatcher)

        command.execute(user='restricted')

        dispatcher.dispatch.assert_called_with(
            'send_message',
            user='restricted',
            text='Access denied. Please, use /myID command to get your ID and contact bot administrator'
        )

    def test_listen_for_subscribe_event(self, settings_mock):
        dispatcher = Mock()

        command = Subscribe(dispatcher)

        dispatcher.add_listener.assert_called_with('command_subscribe', command.execute)

    def test_dispatch_subscribe_for_allowed_user(self, settings_mock):
        dispatcher = Mock()

        command = Subscribe(dispatcher)

        command.execute(user=111111)

        dispatcher.dispatch.assert_any_call(
            'send_message',
            user=111111,
            text='subscription is done'
        )
        dispatcher.dispatch.assert_any_call(
            'subscribe_user',
            user=111111
        )

    def test_show_help_on_restricted_user_subscribe(self, settings_mock):
        dispatcher = Mock()

        command = Subscribe(dispatcher)

        command.execute(user='restricted')

        dispatcher.dispatch.assert_called_with(
            'send_message',
            user='restricted',
            text='Access denied. Please, use /myID command to get your ID and contact bot administrator'
        )

    def test_listen_for_my_id_event(self, settings_mock):
        dispatcher = Mock()

        command = MyId(dispatcher)

        dispatcher.add_listener.assert_called_with('command_my_id', command.execute)

    def test_show_id_for_allowed_user(self, settings_mock):
        dispatcher = Mock()

        command = MyId(dispatcher)

        command.execute(user=111111)

        dispatcher.dispatch.assert_called_with(
            'send_message',
            user=111111,
            text='111111'
        )

    def test_show_id_for_restricted_user(self, settings_mock):
        dispatcher = Mock()

        command = MyId(dispatcher)

        command.execute(user='restricted')

        dispatcher.dispatch.assert_called_with(
            'send_message',
            user='restricted',
            text='restricted'
        )
