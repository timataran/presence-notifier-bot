import unittest
from unittest.mock import Mock, patch
from router.mac_extractor import ActiveMacExtractor


class TestMacExtractor(unittest.TestCase):

    def setUp(self):
        self.ssh_client_mock = self._buildSshClientMock()

    @patch('router.mac_extractor.settings')
    @patch('router.mac_extractor.paramiko')
    def test_get_router_params_from_settings(self, mock_paramiko, mock_settings):
        mock_paramiko.SSHClient.return_value = self.ssh_client_mock
        extractor = ActiveMacExtractor()
        extractor.get_list()
        self.assertEqual(1, mock_settings.get_router_settings.call_count)

    @patch('router.mac_extractor.settings')
    @patch('router.mac_extractor.paramiko')
    def test_pass_router_settings_to_connect(self, mock_paramiko, mock_settings):
        mock_paramiko.SSHClient.return_value = self.ssh_client_mock
        mock_settings.get_router_settings.return_value = {
            'ip': '192.168.0.2',
            'username': 'name',
            'password': 'pass'
        }
        extractor = ActiveMacExtractor()
        extractor.get_list()
        self.ssh_client_mock.connect.assert_called_with(
            '192.168.0.2',
            username='name',
            password='pass',
            allow_agent=False,
            look_for_keys=False
        )

    @patch('router.mac_extractor.settings')
    @patch('router.mac_extractor.paramiko')
    def test_execute_command_over_ssh(self, mock_paramiko, mock_settings):
        mock_paramiko.SSHClient.return_value = self.ssh_client_mock
        extractor = ActiveMacExtractor()
        extractor.get_list()
        self.ssh_client_mock.exec_command.assert_called_with('interface wireless registration-table print')

    @patch('router.mac_extractor.settings')
    @patch('router.mac_extractor.paramiko')
    def test_parse_router_response(self, mock_paramiko, mock_settings):
        mock_paramiko.SSHClient.return_value = self.ssh_client_mock
        extractor = ActiveMacExtractor()
        mac_list = extractor.get_list()
        self.assertListEqual(
            [
                'BB:22:EE:FF:CC:77',
                '44:AA:00:DD:DD:DD',
                '44:22:AA:AA:66:55',
                'BB:EE:77:00:77:BB'
            ],
            mac_list
        )

    @staticmethod
    def _buildSshClientMock():
        client = Mock()
        client.exec_command.return_value = (None, ROUTER_RESPONSE, None)
        return client


ROUTER_RESPONSE = [
    ' # INTERFACE           RADIO-NAME       MAC-ADDRESS       AP  SIGNAL... TX-RATE',
    ' 0 ;;; User 0',
    '   wlan1                                BB:22:EE:FF:CC:77 no  -43dBm... 54Mbps',
    ' 1 ;;; User 1',
    '   wlan1                                44:AA:00:DD:DD:DD no  -50dBm... 150M...',
    ' 2 ;;; User 2',
    '   wlan1                                44:22:AA:AA:66:55 no  -44dBm... 72.2...',
    ' 3 ;;; User 3',
    '   wlan1                                BB:EE:77:00:77:BB no  -45dBm... 150M...',
]
