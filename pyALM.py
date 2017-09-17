import requests
from base64 import b64encode
import json
import logging
from logging.config import fileConfig
from pprint import pprint

# Logger configuration
import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
__log = logging.getLogger()

_URL = ''
_headers = {}
_request = None
_loginCookies = {}


def getURL():
    return _URL


def getHeaders():
    global _headers
    return _headers


def getRequest():
    global _request
    return _request


def setRequest(requestObject):
    global _request
    _request = requestObject


def setCookies(cookie_dict):
    global _loginCookies
    _loginCookies = cookie_dict


def getCookies():
    return _loginCookies


def getDefaultHeader():
    return {'accept': 'application/json'}


# Methods
def initConnection(almServerURL):
    global _URL
    _URL = 'http://' + almServerURL + '/qcbin'
    __log.info('URL is set to {}'.format(_URL))


def login(username, password):
    global _URL, _headers, _request, _loginCookies
    encodedCredential = 'Basic ' + b64encode((username + ':' + password).encode()).decode()
    __log.debug('encoded credential {}'.format(encodedCredential))
    LoginURL = _URL + '/api/authentication/sign-in'
    __log.debug('Login URL'.format(LoginURL))
    _headers = {
        'accept': 'application/json',
        'Authorization': encodedCredential
    }

    _request = requests.get(LoginURL, headers=_headers)
    __log.debug('Status Code: {}'.format(_request.status_code))
    _loginCookies = _request.cookies.get_dict()
    return _request.status_code


def Domains():
    global _URL, _headers, _request
    DomainURL = _URL + '/rest/domains/'
    __log.debug('Domain URL: {}'.format(DomainURL))
    _headers = {
        'accept': 'application/json'
    }
    _request = requests.get(DomainURL, headers=_headers, cookies=getCookies())
    if _request.status_code < 299:
        __log.debug('Status Code: {}'.format(_request.status_code))
    else:
        __log.debug('Status Code: {}'.format(_request.status_code))
        __log.debug('content: ')
        __log.debug(_request.content)
    JsonObject = _request.json()
    DomainList = [item['Name'] for item in JsonObject['Domains']['Domain']]

    return DomainList


def Projects(Domain):
    ProjectURL = getURL() + '/rest/domains/' + Domain + '/projects/'
    __log.debug('ProjectURL {}'.format(ProjectURL))
    __log.debug('Default Header {}'.format(getDefaultHeader()))
    __log.debug('Sending Request to the server {}'.format(getURL()))
    setRequest(requests.get(ProjectURL, headers=getDefaultHeader(), cookies=getCookies()))
    JsonObject = _request.json()
    __log.debug('response: {}'.format(_request.content))
    __log.debug('Type of the value of the key: {}'.format(type(JsonObject['Projects']['Project'])))

    if type(JsonObject['Projects']['Project']) is list:
        ProjectList = [item['Name'] for item in JsonObject['Projects']['Project']]
    if type(JsonObject['Projects']['Project']) is dict:
        ProjectList = [JsonObject['Projects']['Project']['Name']]
    return ProjectList
