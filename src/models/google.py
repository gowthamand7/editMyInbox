import datetime
import os

import flask
import httplib2
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets

from src import config


class Google(object):

    def __init__(self,json_credentials):
        self.credentials = client.OAuth2Credentials.from_json(json_credentials)
        self.mail_service = self.build_mail_service()
        self.user_info = self.get_user_info()

    def get_user_info(self):
        user_info_service = build(
            serviceName='oauth2', version='v2',
            http=self.credentials.authorize(httplib2.Http()))
        user_info = user_info_service.userinfo().get().execute()
        return user_info

    def get_labels(self):
        labels = self.mail_service.users().labels().list(userId='me').execute()
        return labels['labels']

    def get_messages(self, page_token=None):
        mails = self.mail_service.users().messages().list(userId='me',maxResults=20,pageToken=page_token, q='!in:chats').execute()
        msg = []
        for mail in mails['messages']:
            metadata = self.mail_service.users().messages().get(userId='me', id=mail['id'], format='metadata').execute()
            msg.append(Google.parse_metadata(metadata))
        return msg, mails['nextPageToken']

    @staticmethod
    def parse_metadata(metadata):
        id = metadata['id']
        date = metadata['internalDate']
        subject = None
        from_email = None
        for headers in metadata['payload']['headers']:
            if headers['name'] == 'Subject':
                subject = headers['value']
            if headers['name'] == 'From':
                from_email = headers['value']
        return {
            "id": id,
            "date": datetime.datetime.fromtimestamp(int(date)/1e3).strftime('%Y-%m-%d %H:%M:%S'),
            "subject": subject,
            "from_email": from_email
        }


    def build_mail_service(self):
        http_auth = self.credentials.authorize(httplib2.Http())
        return discovery.build(serviceName='gmail', version='v1', http=http_auth)

    @staticmethod
    def get_auth_uri():
        flow = Google.get_flow()
        return flow.step1_get_authorize_url()

    @staticmethod
    def get_flow():
        return flow_from_clientsecrets(os.path.join(config.PATH, 'client_id.json'),
                                       scope=config.SCOPE,
                                       redirect_uri=config.redirect_uri)

    @staticmethod
    def get_credentials(code):
        flow = Google.get_flow()
        credentials = flow.step2_exchange(code)
        return credentials


class NoUserIdException(Exception):
    pass