from apiclient.discovery import build
from httplib2 import Http
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

GOOGLE_API_SCOPE = "https://www.googleapis.com/auth/analytics"


class Realtime(object):
    def __init__(self, credentials):
        self._authenticate(credentials["CLIENT_SECRETS"],
                           credentials["STORAGE_PATH"])

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

    def query(self, query):
        response = self.service.data().realtime().get(
            **query
        ).execute()
        return response["rows"][0][0]
