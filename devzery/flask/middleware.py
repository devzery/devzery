try:
    from flask import request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from ..core.base import BaseDevzeryMiddleware
import json
import time
import threading
import logging

logger = logging.getLogger(__name__)

if FLASK_AVAILABLE:
    class DevzeryFlaskMiddleware(BaseDevzeryMiddleware):
        def __init__(self, app=None, api_endpoint=None, api_key=None, source_name=None):
            super().__init__(api_endpoint, api_key, source_name)
            self.app = app
            if app is not None:
                self.init_app(app)

        def init_app(self, app):
            self.app = app
            app.before_request(self.before_request)
            app.after_request(self.after_request)

            if not app.config.get('DEVZERY_URL'):
                app.config['DEVZERY_URL'] = self.api_endpoint
            if not app.config.get('DEVZERY_API_KEY'):
                app.config['DEVZERY_API_KEY'] = self.api_key
            if not app.config.get('DEVZERY_SOURCE_NAME'):
                app.config['DEVZERY_SOURCE_NAME'] = self.source_name

        def before_request(self):
            request.start_time = time.time()
            request._body = request.get_data()

        def after_request(self, response):
            try:
                if self.api_key and self.source_name:
                    elapsed_time = time.time() - request.start_time
                    headers = dict(request.headers)

                    logger.debug("Devzery: Request Body", request._body)

                    if request.is_json:
                        body = json.loads(request._body) if request._body else None
                    elif request.content_type and (
                            request.content_type.startswith('multipart/form-data') or
                            request.content_type.startswith('application/x-www-form-urlencoded')
                    ):
                        body = dict(request.form)
                    else:
                        try:
                            body = json.loads(request._body)
                        except Exception as e:
                            logger.debug(f"Devzery: Request body is not JSON or form data {e}")
                            body = None

                    try:
                        response_content = response.get_data(as_text=True)
                        response_content = json.loads(response_content)
                    except:
                        response_content = None

                    data = {
                        'request': {
                            'method': request.method,
                            'path': request.full_path,
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
    class FlaskRequestResponseLoggingMiddleware:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "Flask is required to use the Flask middleware. "
                "Install it with: pip install flask"
            )