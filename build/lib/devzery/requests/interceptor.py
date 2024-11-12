from ..core.base import BaseDevzeryMiddleware
from requests.adapters import HTTPAdapter
import requests
import threading
import time
from urllib.parse import urlparse


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

        self.backend_host = [urlparse(api_endpoint).netloc if api_endpoint else None]

        if(self.backend_host is None):
            self.backend_host = ["server-v3-7qxc7hlaka-uc.a.run.app"]

    def should_intercept(self, request_url):
        """
        Determine if the request should be intercepted and logged
        Returns False if the request is to the logging backend
        """
        if not self.backend_host:
            return True

        request_host = urlparse(request_url).netloc
        return request_host not in self.backend_host

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
                'method': request.method,
                'path': request.url,
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
