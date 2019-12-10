from unittest import TestCase, main
from unittest.mock import patch, Mock, call
from connection_monitor import ConnectionMonitor


@patch("connection_monitor.settings")
@patch("connection_monitor.ActiveMacExtractor")
class TestSettings(TestCase):

    def test_fill_status_map_on_first_run(self, extractor_mock, settings_mock):
        extractor_mock.get_list.return_value = ['111', '222', '333']
        settings_mock.get_residents.return_value = self._getResidents()

        monitor = ConnectionMonitor(Mock())

        monitor.check_connections()

        self.assertDictEqual(
            self._getInitialState(),
            monitor.status_map
        )

    def test_change_last_state_on_subsequent_run(self, extractor_mock, settings_mock):
        extractor_mock.get_list.return_value = ['222', '333']
        settings_mock.get_residents.return_value = self._getResidents()

        monitor = ConnectionMonitor(Mock())

        monitor.status_map = self._getInitialState()

        monitor.check_connections()

        self.assertDictEqual(
            {
                'Alice': False,
                'Bob': True,
                'Kate': False
            },
            monitor.status_map
        )

    def test_call_notification_for_every_change(self, extractor_mock, settings_mock):
        extractor_mock.get_list.return_value = ['111', '444']
        settings_mock.get_residents.return_value = self._getResidents()

        notificator = Mock()

        monitor = ConnectionMonitor(notificator.notify)

        monitor.status_map = self._getInitialState()

        monitor.check_connections()

        self.assertListEqual(
            [call('Bob out'), call('Kate in')],
            notificator.notify.mock_calls
        )

    @patch("connection_monitor.time")
    def test_run_indefinite_loop_to_monitor(self, time_mock, extractor_mock, settings_mock):
        extractor_mock.get_list.return_value = []
        settings_mock.get_residents.return_value = self._getResidents()
        time_mock.sleep.side_effect = [None, None, Exception('foo')]

        monitor = ConnectionMonitor(Mock())

        # noinspection PyBroadException
        try:
            monitor._monitor_connections()
        except Exception:
            self.assertEqual(3, time_mock.sleep.call_count)

    @staticmethod
    def _getResidents():
        return {
            'Alice': '111',
            'Bob': '222',
            'Kate': '444'
        }

    @staticmethod
    def _getInitialState():
        return {
            'Alice': True,
            'Bob': True,
            'Kate': False
        }


if __name__ == '__main__':
    main()
