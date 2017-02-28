import base64
import datetime
import os
from email import message_from_file
from io import StringIO

import httplib2
from googleapiclient import discovery
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets

from src import config


class Google(object):

    def __init__(self, json_credentials):
        self.credentials = client.OAuth2Credentials.from_json(json_credentials)
        self.mail_service = self.build_mail_service()
        self.user_info = None
        self.user_info = self.get_user_info()

    def get_user_info(self):
        if self.user_info is None:
            user_info_service = build(
                serviceName='oauth2', version='v2',
                http=self.credentials.authorize(httplib2.Http()))
            user_info = user_info_service.userinfo().get().execute()
            return user_info
        else:
            return self.user_info

    def get_labels(self):
        labels = self.mail_service.users().labels().list(userId='me').execute()
        return labels['labels']

    def get_message(self, message_id):
        message = self.mail_service.users().messages().get(userId='me', id=message_id,format='raw').execute()
        orginal_response = base64.urlsafe_b64decode(message['raw'])
        orginal_response = orginal_response.decode("utf-8")

        b = message_from_file(StringIO(orginal_response))
        returnO = ''
        if b.is_multipart():
            for payload in b.get_payload():
                # if payload.is_multipart(): ...
                returnO += payload.get_payload()
        else:
            returnO = b.get_payload()
        return returnO


    def parse_raw_data(self):
        pass

    def get_messages_by_subject(self, search_query, page_token=None):
        return self._process_request(user_id='me', page_token=page_token, search_query=search_query)

    def get_messages_by_labels(self, label_ids, page_token=None):
        label_ids = [label_ids]
        return self._process_request(user_id='me', page_token=page_token, label_ids=label_ids)

    def _process_request(self, user_id='me', page_token=None, label_ids=None, search_query=None):
        if search_query is not None:
            search_query = "!in:chats {}".format(search_query)
        else:
            search_query = "!in:chats"
        mails = self.mail_service.users().messages().list(userId=user_id,
                                                          maxResults=config.MAX_RESULT,
                                                          pageToken=page_token,
                                                          labelIds=label_ids,
                                                          q=search_query).execute()
        msg = []
        if 'messages' in mails:
            for mail in mails['messages']:
                metadata = self.mail_service.users().messages().get(userId='me', id=mail['id'], format='metadata').execute()
                msg.append(Google.parse_metadata(metadata))
        if 'nextPageToken' in mails:
            return msg, mails['nextPageToken']
        else:
            return msg, None

    def get_messages(self, page_token=None):
        return self._process_request(user_id='me', page_token=page_token)

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
