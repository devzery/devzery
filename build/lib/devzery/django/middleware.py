try:
    from django.utils.deprecation import MiddlewareMixin
    from django.conf import settings

    DJANGO_AVAILABLE = True
except ImportError:
    DJANGO_AVAILABLE = False

from ..core.base import BaseDevzeryMiddleware
import json
from urllib.parse import parse_qs
import time
import threading
import logging

logger = logging.getLogger(__name__)

if DJANGO_AVAILABLE:
    class DevzeryDjangoMiddleware(MiddlewareMixin, BaseDevzeryMiddleware):
        def __init__(self, get_response=None):
            MiddlewareMixin.__init__(self, get_response)
            BaseDevzeryMiddleware.__init__(
                self,
                api_endpoint=getattr(settings, 'DEVZERY_URL', None),
                api_key=getattr(settings, 'DEVZERY_API_KEY', None),
                source_name=getattr(settings, 'DEVZERY_SOURCE_NAME', None)
            )

        def process_request(self, request):
            request.start_time = time.time()
            request._body = request.body

        def process_response(self, request, response):
            try:
                if (self.api_key and self.source_name):
                    elapsed_time = time.time() - request.start_time
                    headers = {key: value for key, value in request.META.items() if
                               key.startswith('HTTP_') or key in ['CONTENT_LENGTH', 'CONTENT_TYPE']}

                    if request.content_type == 'application/json':
                        body = json.loads(request._body) if request._body else None
                    elif request.content_type and (
                        request.content_type.startswith('multipart/form-data') or
                        request.content_type.startswith('application/x-www-form-urlencoded')
                    ):
                        body = parse_qs(request._body.decode('utf-8'))
                    else:
                        body = None

                    try:
                        response_content = response.content.decode('utf-8')
                        response_content = json.loads(response_content)
                    except:
                        response_content = None

                    data = {
                        'request': {
                            'method': request.method,
                            'path': request.get_full_path(),
                            'headers': headers,
                            'body': body,
                        },
                        'response': {
                            'status_code': response.status_code,
                            'content': response_content
                        },
                        'elapsed_time': elapsed_time,
                    }

                    threading.Thread(
                        target=self.send_data_to_api_sync,
                        args=(data, response_content)
                    ).start()

                else:
                    if not self.api_key:
                        logger.debug("Devzery: No API KEY")
                    if not self.source_name:
                        logger.debug("Devzery: No Source Name")

            except Exception as e:
                logger.debug(f"Devzery: Error occurred Capturing: {e}")

            return response

else:
    class RequestResponseLoggingMiddleware:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "Django is required to use the Django middleware. "
                "Install it with: pip install django"
            )