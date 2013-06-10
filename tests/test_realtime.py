import unittest
from hamcrest import *
from backdrop.collector.realtime import Realtime


class TestRealtime(unittest.TestCase):
    def setUp(self):
        self.path_to_config = "config/config.json"

    def test_it_exists(self):
        assert_that(Realtime(self.path_to_config), is_(instance_of(Realtime)))
