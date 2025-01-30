from ..core.base import BaseDevzeryMiddleware
from requests.adapters import HTTPAdapter
import requests
import threading
import time
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InterceptAdapter(HTTPAdapter, BaseDevzeryMiddleware):
    def __init__(self, api_endpoint=None, api_key=None, source_name=None, pool_connections=10, pool_maxsize=10,
                 max_retries=0, pool_block=False):
        HTTPAdapter.__init__(
            self,
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=max_retries,
            pool_block=pool_block
        )
        BaseDevzeryMiddleware.__init__(
            self,
            api_endpoint=api_endpoint,
            api_key=api_key,
            source_name=source_name
        )

    def should_intercept(self, request_url: str, exclude_patterns: list = None) -> bool:
        """
        Determine if a request should be intercepted based on URL and exclusion patterns.
        
        Args:
            request_url (str): The URL of the request
            exclude_patterns (list, optional): List of URL patterns to exclude. Defaults to None.
        
        Returns:
            bool: True if request should be intercepted, False otherwise
        """
        if not request_url:
            return False

        # Default exclude patterns if none provided
        if exclude_patterns is None:
            exclude_patterns = [
                'server-v3-7qxc7hlaka-uc.a.run.app',
            ]

        # Check if URL matches any exclude pattern
        for pattern in exclude_patterns:
            if pattern.lower() in request_url.lower():
                return False

        # Only intercept HTTP(S) requests
        if not request_url.startswith(('http://', 'https://')):
            return False

        return True

    def send(self, request, **kwargs):

        if not self.should_intercept(request.url):
            return super().send(request, **kwargs)

        start_time = time.time()
        if isinstance(request.body, bytes):
            body = request.body.decode('utf-8')
        else:
            body = request.body

        response = super().send(request, **kwargs)
        elapsed_time = time.time() - start_time

        try:
            response_content = response.json()
        except ValueError:
            response_content = response.text

        data = {
            'request': {
                'baseURL': f"{urlparse(request.url).scheme}://{urlparse(request.url).netloc}",
                'method': request.method,
                'path': urlparse(request.url).path,
                'headers': dict(request.headers),
                'body': body,
            },
            'response': {
                'status_code': response.status_code,
                'content': response_content
            },
            'elapsed_time': elapsed_time,
            'isExternal': True
        }

        threading.Thread(
            target=self.send_data_to_api_sync,
            args=(data, response_content)
        ).start()

        return response


def create_intercepted_session(api_endpoint=None, api_key=None, source_name=None):
    session = requests.Session()
    adapter = InterceptAdapter(api_endpoint, api_key, source_name)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
