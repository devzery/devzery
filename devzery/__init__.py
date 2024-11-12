from importlib import import_module
import warnings
from .requests.patcher import DevzeryRequestsMiddleware  # Import the patch_requests function
from .requests import interceptor

__version__ = "0.1.0"

def get_django_middleware():
    try:
        return import_module('.django.middleware', 'devzery').RequestResponseLoggingMiddleware
    except ImportError as e:
        warnings.warn(
            "Django middleware is not available. "
            "Install Django first: pip install django"
        )
        raise

def get_flask_middleware():
    try:
        return import_module('.flask.middleware', 'devzery').FlaskRequestResponseLoggingMiddleware
    except ImportError as e:
        warnings.warn(
            "Flask middleware is not available. "
            "Install Flask first: pip install flask"
        )
        raise

