import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

GOOGLE_API_SCOPE = "https://www.googleapis.com/auth/analytics"


def get_contents(path_to_file):
    with open(path_to_file) as file_to_load:
        contents = file_to_load.read()
    return contents


class Realtime(object):
    def __init__(self, config_path):
        config = json.loads(get_contents(config_path))

        self._authenticate(config["PATH_TO_CLIENT_SECRET"],
                           config["PATH_TO_STORAGE"])

    def _authenticate(self, client_secrets, storage_path):
        flow = flow_from_clientsecrets(client_secrets, scope=GOOGLE_API_SCOPE)
        storage = Storage(storage_path)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run(flow, storage)

        self.service = build(
            serviceName="analytics",
            version="v3alpha",
            http=credentials.authorize(Http())
        )

    def query(self, path_to_query):
        query = json.loads(get_contents(path_to_query))
        response = self.service.data().realtime().get(
            **query
        ).execute()

        print response
