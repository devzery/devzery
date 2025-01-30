import os
from importlib import import_module
import warnings
from .requests.patcher import DevzeryRequestsMiddleware  # Import the patch_requests function
from .requests import interceptor
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

__version__ = "0.0.7"

class Devzery:
    def __init__(self, app=None, api_endpoint=None, api_key=None, source_name=None):
        self.api_endpoint = api_endpoint
        self.api_key = os.getenv("DEVZERY_API_KEY") if api_key is None else api_key
        self.source_name = source_name
        self.app = app
        self._django_middleware = None
        self._flask_middleware = None
        self._requests_middleware = None

    def django_middleware(self):
        if not self._django_middleware:
            try:
                DjangoMiddleware = import_module('.django.middleware', 'devzery').DevzeryDjangoMiddleware
                self._django_middleware = DjangoMiddleware
            except ImportError:
                warnings.warn("Django middleware is not available. Install Django first: pip install django")
                raise
        return self._django_middleware

    def flask_middleware(self, app=None):
        """
        Initialize Flask middleware with an app instance.
        App can be passed either during client init or here.
        """
        if app:
            self.app = app
            
        if not self._flask_middleware:
            try:
                FlaskMiddleware = import_module('.flask.middleware', 'devzery').DevzeryFlaskMiddleware
                self._flask_middleware = FlaskMiddleware(
                    app=self.app,
                    api_endpoint=self.api_endpoint,
                    api_key=self.api_key,
                    source_name=self.source_name
                )
            except ImportError:
                warnings.warn("Flask middleware is not available. Install Flask first: pip install flask")
                raise
        return self._flask_middleware

    def requests_middleware(self):
        if not self._requests_middleware:
            self._requests_middleware = DevzeryRequestsMiddleware(
                api_endpoint=self.api_endpoint,
                api_key=self.api_key,
                source_name=self.source_name
            )
        return self._requests_middleware.intercept_requests()

# For backwards compatibility
def get_django_middleware():
    warnings.warn("Use Devzery().django_middleware() instead", DeprecationWarning)
    return import_module('.django.middleware', 'devzery').DevzeryDjangoMiddleware

def get_flask_middleware():
    warnings.warn("Use Devzery().flask_middleware() instead", DeprecationWarning)
    return import_module('.flask.middleware', 'devzery').DevzeryFlaskMiddleware

