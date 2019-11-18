import unittest
import logging
import utils


class TestSettings(unittest.TestCase):

    def test_return_logger_instance(self):
        logger = utils.get_logger('Test')
        self.assertEqual(logging.Logger, type(logger))
