import os
import unittest
import sys
from hamcrest import *
from statsd.tests import assert_raises

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'hooks'))

from manage_crontab import generate_crontab, ParseError

class TestManageCrontab(unittest.TestCase):
    def path_to_jobs(self, name):
        return os.path.join(os.path.dirname(__file__), 'fixtures', name)

    def test_other_cronjobs_are_preserved(self):
        generated_jobs = generate_crontab(
            ['other cronjob'],
            self.path_to_jobs('no_jobs'),
            "", "")
        assert_that(generated_jobs, has_item("other cronjob"))

    def test_some_cronjobs_are_added(self):
        generated_jobs = generate_crontab(
            [],
            self.path_to_jobs('some_jobs'),
            "app", "python")
        assert_that(generated_jobs,
                    has_item(contains_string("schedule")))
        assert_that(generated_jobs,
                    has_item(contains_string("-q app/query.json")))
        assert_that(generated_jobs,
                    has_item(contains_string("-c app/config.json")))

    def test_added_jobs_get_tagged_with_comment(self):
        generated_jobs = generate_crontab(
            [],
            self.path_to_jobs('some_jobs'),
            "app", "python")

        assert_that(generated_jobs,
                    has_item(ends_with('# backdrop-ga-realtime-collector')))

    def test_existing_tagged_cronjobs_are_purged(self):
        generated_jobs = generate_crontab(
            ['other job # backdrop-ga-realtime-collector'],
            self.path_to_jobs('some_jobs'),
            "app", "python"
        )
        assert_that(generated_jobs,
                    is_not(has_item(contains_string("other job"))))

    def test_invalid_jobs_file_causes_failure(self):
        self.assertRaises(ParseError, generate_crontab,
                          [],
                          self.path_to_jobs('bad_jobs'),
                          "app", "python")
