import requests
from .interceptor import create_intercepted_session

class DevzeryRequestsMiddleware:
    def __init__(self, api_endpoint=None, api_key=None, source_name=None):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.source_name = source_name

    def intercept_requests(self):
        # Create the intercepted session with your custom parameters
        intercepted_session = create_intercepted_session(
            api_endpoint=self.api_endpoint,
            api_key=self.api_key,
            source_name=self.source_name
        )

        # Monkey-patch the requests methods globally
        requests.get = intercepted_session.get
        requests.post = intercepted_session.post
        requests.put = intercepted_session.put
        requests.delete = intercepted_session.delete
        requests.patch = intercepted_session.patch
        requests.request = intercepted_session.request

        return requests