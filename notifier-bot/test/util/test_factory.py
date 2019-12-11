from unittest import TestCase
from unittest.mock import patch
import logging
from util import factory


class TestFactory(TestCase):

    def test_return_logger_instance(self):
        logger = factory.get_logger('Test')
        self.assertEqual(logging.Logger, type(logger))

    @patch("util.factory.settings")
    @patch("util.factory.telebot")
    def test_pass_token_to_build_bot(self, telebot_mock, settings_mock):
        settings_mock.get_bot_settings.return_value = {'token': 'foo-bar'}

        factory.get_telebot()

        telebot_mock.TeleBot.assert_called_with('foo-bar')

    @patch("util.factory.settings")
    @patch("util.factory.telebot")
    def test_return_created_bot(self, telebot_mock, settings_mock):
        settings_mock.get_bot_settings.return_value = {'token': 'foo-bar'}
        telebot_mock.TeleBot.return_value = 'Bot object'

        bot = factory.get_telebot()

        self.assertEqual('Bot object', bot)
