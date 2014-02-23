# -*- coding: utf-8 -*-
"""
    sslstore_api.client
    ~~~~~~~~~~~~~~~~~~~

    The client for sending requests to the SSLStore API

    :copyright: (c) 2013 by Daniel Chatfield
"""

import json
import logging
import pprint
from urllib import quote_plus

from google.appengine.api import urlfetch

from .errors import SSLStoreApiError, WildCardCSRError

pp = pprint.PrettyPrinter(indent=4)


def escape(s):
    return quote_plus(s.encode("utf-8"))


def parseError(result):
        try:
            message = result['AuthResponse']['Message'][0]
        except:
            message = "unknown error message"

        if "The Common Name (Domain Name) may not contain a *" in message:
            raise WildCardCSRError()
        raise SSLStoreApiError(result['AuthResponse']['Message'][0])


def checkForError(result, endpoint):
    if result['AuthResponse']['isError']:
        parseError(result)
    return False

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
        logging.info(pp.pformat(result))
        checkForError(result, endpoint)
        return result


    def get_approver_emails(self, domain, product_code='positivessl'):
        fields = {
            "DomainName": domain,
            "ProductCode": product_code
        }
        result = self.api_call('order/approverlist', fields)
        return result['ApproverEmailList']

    def check_csr(self, csr, product_code='positivessl'):
        csr = escape(csr)
        fields = {
            "CSR": csr,
            "ProductCode": product_code
        }
        return self.api_call('csr', fields)

    def create_dv_ssl_order(
        self, csr, domain, approver_email, product_code='positivessl',
        web_server_type="Other", custom_order_id=None, technical_contact=None):

        csr = escape(csr)

        if technical_contact is None:
            technical_contact = {
                "FirstName": "Daniel",
                "LastName": "Chatfield",
                "Phone": "441425474580",
                "Email": "business+ssl@platinummirror.com",
                "Title": "Mr",
                "OrganizationName": "Volcanic Pixels",
                "Country": "GB"
            }

        fields = {
            "ProductCode": product_code,
            "TechnicalContact": technical_contact,
            "ValidityPeriod": 12,
            "ServerCount": 1,
            "WebServerType": web_server_type,
            "CSR": csr,
            "DomainName": domain,
            "ApproverEmail": approver_email
        }

        if custom_order_id:
            fields['CustomOrderID'] = str(custom_order_id)

        return self.api_call('order/neworder', fields)

    def get_order_status(self, order_id):
        return self.api_call('order/status', {"TheSSLStoreOrderID": order_id})

    def get_certificates(self, order_id):
        return self.api_call(
            'order/download',
            {"TheSSLStoreOrderID": order_id}
        )

    def resend_email(self, order_id):
        try:
            return self.api_call(
                'order/resend',
                {
                    "TheSSLStoreOrderID": order_id,
                    "ResendEmailType": "ApproverEmail"
                }
            )
        except KeyError:
            # THis is normal - the API is inconsistent
            return True
