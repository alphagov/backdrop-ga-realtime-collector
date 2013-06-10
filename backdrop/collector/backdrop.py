from datetime import datetime
from pprint import pprint
import pytz


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

        # requests.post(
        #     url=self.location,
        #     data=data,
        #     headers=headers
        # )

    def _timestamp(self):
        return self.timezone.localize(datetime.now()).isoformat()
