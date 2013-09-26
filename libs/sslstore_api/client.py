# -*- coding: utf-8 -*-
"""
    sslstore_api.client
    ~~~~~~~~~~~~~~~~~~~

    The client for sending requests to the SSLStore API

    :copyright: (c) 2013 by Daniel Chatfield
"""

import json
import logging

from google.appengine.api import urlfetch

from .errors import SSLStoreApiError


class Client():
    def __init__(self, partner_code, auth_token, sandbox=True):
        self.partner_code = str(partner_code)
        self.auth_token = auth_token
        self.sandbox = sandbox

        if sandbox:
            self.api_url = "https://sandbox-wbapi.thesslstore.com/rest/"
        else:
            self.api_url = "https://api.thesslstore.com/rest/"

    def api_call(self, endpoint, fields):
        url = self.api_url + endpoint;
        fields['AuthRequest'] = {
            "PartnerCode": self.partner_code,
            "AuthToken": self.auth_token
        }
        payload = json.dumps(
            fields, sort_keys=True, indent=4, separators=(',', ': '))
        headers = {
            'Content-Type': 'application/json'
        }
        #BQ (tag to remind me that this data could be streamed to Big Query)
        logging.info('SSLStore API request')
        logging.info(payload)

        result = urlfetch.fetch(url, payload, 'POST', headers)

        if result.status_code != 200:
            raise SSLStoreApiError()

        result = json.loads(result.content)
        logging.info(result)
        return result


    def get_approver_emails(self, domain, product_code='rapidssl'):
        fields = {
            "DomainName": domain,
            "ProductCode": product_code
        }
        result = self.api_call('order/approverlist', fields)
        return result['ApproverEmailList']
