import unittest
import os
import settings

DEFAULT_ENVIRONMENT = {
    'ROUTER_IP': '192.168.0.1',
    'ROUTER_USERNAME': 'admin',
    'ROUTER_PASSWORD': 'admin',
    'BOT_TOKEN': 'foobar:foobarfoobarfoobar',
    'BOT_POLLING_INTERVAL': 4,
    'BOT_ROUTER_POLLING_PERIOD': 4,
    'RESIDENTS_JSON':'{}'
}


class TestSettings(unittest.TestCase):

    def setUp(self):
        pass

    def test_throw_on_router_parameters_are_not_set(self):
        for env_name in ('ROUTER_IP', 'ROUTER_USERNAME', 'ROUTER_PASSWORD'):
            self._set_valid_environment(**{env_name: None})
            self.assertRaises(Exception, settings.get_router_settings)

    def test_return_router_settings(self):
        self._set_valid_environment(**{
            'ROUTER_IP': '10.10.10.2',
            'ROUTER_USERNAME': 'root',
            'ROUTER_PASSWORD': 'root'
        })

        router_settings = settings.get_router_settings()

        self.assertDictEqual(
            {
                'ip': '10.10.10.2',
                'username': 'root',
                'password': 'root'
            },
            router_settings
        )

    def test_throw_on_required_bot_settings_is_not_set(self):
        self._set_valid_environment(**{'BOT_TOKEN': None})
        self.assertRaises(Exception, settings.get_bot_settings)

    def test_use_defaults_for_optional_settings(self):
        with_empty_optionals = {
            'BOT_TOKEN': 'qwerty qwerty',
            'BOT_POLLING_INTERVAL': None,
            'BOT_ROUTER_POLLING_PERIOD': None
        }

        self._set_valid_environment(**with_empty_optionals)

        bot_settings = settings.get_bot_settings()

        self.assertDictEqual(
            {
                'token': 'qwerty qwerty',
                'polling_interval': 3,
                'router_polling_period': 3
            },
            bot_settings
        )

    def test_return_bot_settings(self):
        self._set_valid_environment(**{
            'BOT_TOKEN': 'qwerty qwerty',
            'BOT_POLLING_INTERVAL': 4,
            'BOT_ROUTER_POLLING_PERIOD': 4
        })

        bot_settings = settings.get_bot_settings()

        self.assertDictEqual(
            {
                'token': 'qwerty qwerty',
                'polling_interval': 4,
                'router_polling_period': 4
            },
            bot_settings
        )

    def test_return_residents(self):
        self._set_valid_environment(RESIDENTS_JSON='{"Alice":"A0:B1:C2:D3:E4:F5", "Bob":"F6:E5:D4:C3:B2:A1"}')

        residents = settings.get_residents()

        self.assertDictEqual(
            {
                'Alice': 'A0:B1:C2:D3:E4:F5',
                'Bob': 'F6:E5:D4:C3:B2:A1'
            },
            residents
        )

    @staticmethod
    def _set_valid_environment(**kwargs):
        environment = DEFAULT_ENVIRONMENT.copy()
        environment.update(**kwargs)
        os.environ = environment
