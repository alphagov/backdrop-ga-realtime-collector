from mock import Mock, patch, ANY
from nose.tools import *
import collector
from collector.realtime import Collector, Realtime
from hamcrest.library.text.stringmatches import matches_regexp
from hamcrest.library.integration import match_equality
import re

TIMESTAMP_PATTERN = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+\d\d')


def mock_instance(cls):
    mock = Mock()
    cls.return_value = mock
    return mock


def is_timestamp():
    return match_equality(matches_regexp(TIMESTAMP_PATTERN))


class TestCollector(object):
    @patch("collector.realtime.Bucket")
    @patch("collector.realtime.Realtime")
    def test_send_records_for(self, Realtime, Bucket):
        realtime = mock_instance(Realtime)
        bucket = mock_instance(Bucket)

        realtime.query.return_value = 12

        collector = Collector('credentials')

        collector.send_records_for({},
                                   to={"url": 'url', "token": 'token'})

        Realtime.assert_called_with('credentials')
        Bucket.assert_called_with(url='url', token='token')

        realtime.query.assert_called_with({})
        bucket.post.assert_called_with({
            '_timestamp': is_timestamp(),
            '_id': is_timestamp(),
            'unique_visitors': 12,
            'for_url': '',
        })

    @patch("collector.realtime.Realtime")
    def test_sending_records_fails_with_invalid_target(self, _):
        collector = Collector(None)
        assert_raises(TypeError, collector.send_records_for,
                      None, {'foo': 'bar'})

    @patch("collector.realtime.Bucket")
    @patch("collector.realtime.Realtime")
    def test_sending_records_sends_for_url(self, _, Bucket):
        bucket = mock_instance(Bucket)

        collector = Collector(None)
        collector.send_records_for({'filters': 'myurl'},
                                   to={})

        bucket.post.assert_called_with({
            '_timestamp': ANY,
            '_id': ANY,
            'unique_visitors': ANY,
            'for_url': 'myurl',
        })

class TestRealtime(object):
    """No tests for Realtime class
    This class just deals with the google analytics client. Testing it would
    require a lot of mocking and would be quite brittle.
    """
    @patch.object(collector.realtime.Realtime, "_authenticate")
    @patch.object(collector.realtime.Realtime, "execute_ga_query")
    def test_should_return_zero_if_no_rows_returned_from_ga(
            self, execute_ga_query, authenticate):
        execute_ga_query.return_value = {}
        realtime = Realtime({"CLIENT_SECRETS": None, "STORAGE_PATH": None})
        value = realtime.query(None)
        assert_equal(value, 0)
