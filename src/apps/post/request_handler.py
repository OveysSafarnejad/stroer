import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from apps.post.exceptions import JSONPlaceHolderResponseException


class RequestHandler:
    """HTTP request handler with retry"""

    def __init__(self, retries):
        self.session = requests.Session()
        retries = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def try_post(self, url, body):
        """Sends post-request with retries"""
        try:
            response = self.session.post(url, data=body)
        except Exception:
            raise JSONPlaceHolderResponseException()

        return response

    def try_put(self, url, body):
        """Sends put-request with retries"""

        try:
            response = self.session.put(url, data=body)
        except Exception:
            raise JSONPlaceHolderResponseException()

        return response

    def try_delete(self, url):
        """Sends delete-request with retries"""

        try:
            response = self.session.delete(url)
        except Exception:
            raise JSONPlaceHolderResponseException()

        return response
