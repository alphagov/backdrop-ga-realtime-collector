from datetime import datetime
import json
from pprint import pprint
import pytz
import requests


class Backdrop(object):
    def __init__(self, config):
        self.token = config["BACKDROP_BEARER_TOKEN"]
        self.location = config["BACKDROP_LOCATION"]
        self.timezone = pytz.timezone("Europe/London")

    def send_current_user_event(self, visitor_count, for_url):
        headers = {
            "Content-type": "application/json",
            "Authorization": "Bearer " + self.token
        }

        data = {
            "_timestamp": self._timestamp(),
            "_id": self._timestamp(),
            "unique_visitors": visitor_count,
            "for_url": for_url
        }

        pprint(data)

        response = requests.post(
            url=self.location,
            data=json.dumps(data),
            headers=headers
        )

        print response.text

    def _timestamp(self):
        return self.timezone.localize(datetime.now().replace(microsecond=0))\
            .isoformat()
