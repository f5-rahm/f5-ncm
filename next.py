# External Imports
# Import only with "import package",
# it will make explicitly in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
from typing import Union
import datetime
import json
import requests
import urllib3

# Internal Imports
# Import only with "from x import y", to simplify the code.

from common.restobject import NextObject
from common.exceptions import NextAPIError
from common.exceptions import InvalidMethodError
from common.exceptions import InvalidPathError

from version import __version__


# Disable urllib3 SSL warnings (at cli)
urllib3.disable_warnings()


def _load_spec():
    with open('files/f5cm-apispec.json') as f:
        spec = json.loads(f.read())
    return [public_path.get('x-f5-cm-public-api-path') for _, public_path in spec.get('paths').items()]


class NEXT:
    """
    Defines methods to call the REST API that can be used
    by Central Manager.

    Arguments:
        device: Name or IP of the device to send the HTTP requests.
        username: Username used to login to the device.
        password: Password used to login to the device.
        debug: Debug file name to be used to output the debug information.
        session_verify: Disables SSL certificate validation if set to False

    Exceptions:
        InvalidOptionError: Raised when invalid options are used as arguments.
    """

    def __init__(self,
                 device: str,
                 username: str = None,
                 password: str = None,
                 session_verify: bool = True,
                 debug: str = None):

        # Variables
        self.device = device
        self.username = username
        self.password = password
        self.debug = debug
        self.session_verify = session_verify
        self.valid_api_paths = _load_spec()
        self.token_access = None
        self.token_refresh = None
        self.refresh_timestamp = None
        self.session = requests.Session()

        # Session settings
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.verify = session_verify
        self.session.headers.update({"User-Agent": f"BIGGIN/{__version__}"})

        # Login to Central Manager
        self._login()

    def _login(self) -> None:
        """
        Login to the device and retrieve the bearer token for future connections

        Exceptions:
            NextAPIError: Raised when the API returns an error.
        """
        # TODO add support for additional authentication models
        login_payload = {"username": self.username, "password": self.password}
        response = self.session.post(f"https://{self.device}/api/login", json=login_payload)
        if response.status_code != 200:
            raise NextAPIError(response, self.debug)
        else:
            self.username = None
            self.password = None
            tokens_payload = NextObject(response.json())
            self.token_access = tokens_payload.properties.get("access_token")
            self.token_refresh = tokens_payload.properties.get("refresh_token")
            self.session.headers.update({"Authorization": f"Bearer {self.token_access}"})

    def _refresh_token(self) -> None:
        refresh_payload = {"refresh_token": self.token_refresh}
        response = self.session.post(f"https://{self.device}/api/token-refresh", json=refresh_payload)
        if response.status_code != 200:
            raise NextAPIError(response, self.debug)
        else:
            token = NextObject(response.json())
            self.token_access = token.properties.get("access_token")
            self.session.headers.update({"Authorization": f"Bearer {self.token_access}"})
            self.refresh_timestamp = datetime.datetime.now()

    def _get_url(self, path: str) -> str:
        """
        Creates the URL to be used to connect to the device.

        Arguments:
            path: HTTP path used to create the URL.
        """
        if path.endswith("/"):
            path = path[:-1]
        return f"https://{self.device}{path}"

    def _api_call(self, method, path, data=None):
        if method not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            raise InvalidMethodError(f'Invalid method: {method}')
        elif path not in self.valid_api_paths:
            raise InvalidPathError(f'Invalid path: {path}')
        else:
            url = self._get_url(path)
            match method:
                case "GET":
                    response = self.session.get(url)
                case "POST":
                    response = self.session.post(url, data=data)
                case "PUT":
                    response = self.session.put(url, data=data)
                case "PATCH":
                    response = self.session.patch(url, data=data)
                case "DELETE":
                    response = self.session.delete(url)
            if response.status_code != 200:
                if response.status_code == 401:  # Assuming 401 indicates an expired token
                    self._refresh_token()  # Refresh token if expired
                    return self._api_call(method, path, data=None)  # Retry API call with new token
                raise NextAPIError(response, self.debug)
            return response.json()

    def load(self, path: str) -> Union[list[NextObject], NextObject]:
        """
        Loads one object or a list of objects from the device.
        If you call with a specific object name, it returns a single object.
        If you call without an object name, it returns a list of objects.

        Sends an HTTP GET request to the Central Manager REST API.

        Arguments:
            path: HTTP path used in the HTTP request sent to the device.
        """
        response = self._api_call('GET', path)
        return response
