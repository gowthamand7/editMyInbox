import os

import httplib2
from flask import json
from googleapiclient import errors
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets

from src import config


class Google(object):

    def __init__(self):
        pass

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
        return flow.step2_exchange(code)

    @staticmethod
    def get_user_info(credentials):
        user_info_service = build(
            serviceName='oauth2', version='v2',
            http=credentials.authorize(httplib2.Http()))
        user_info = None
        try:
            user_info = user_info_service.userinfo().get().execute()
        except errors.HttpError as e:
            if user_info and user_info.get('id'):
                return user_info
            else:
                raise NoUserIdException()
        return user_info


class NoUserIdException(Exception):
    pass