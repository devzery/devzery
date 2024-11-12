try:
    from flask import request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

from ..core.base import BaseDevzeryMiddleware
import json
import time
import threading

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
            try:
                # Cache the raw data so it can be read multiple times
                request._raw_body = request.get_data(cache=True, parse_form_data=True)
                print(f"Devzery: Request Method: {request.method}")
                print(f"Devzery: Content Type: {request.headers.get('Content-Type', '')}")
                print(f"Devzery: Request Data: {request._raw_body}")
                
                # Additional checks for different request types
                if request.is_json:
                    print(f"Devzery: JSON Data: {request.get_json()}")
                if request.form:
                    print(f"Devzery: Form Data: {request.form}")
                if request.files:
                    print(f"Devzery: Files: {request.files}")
                    
            except Exception as e:
                print(f"Devzery: Error capturing request data: {e}")
                request._raw_body = b''

        def after_request(self, response):
            try:
                if self.api_key and self.source_name:
                    elapsed_time = time.time() - request.start_time
                    headers = dict(request.headers)

                    # Handle request body based on content type
                    request._raw_body = request.get_data()

                    body = None
                    content_type = request.headers.get('Content-Type', '')
                    # print(f"Devzery: Content Type: {request.body}")
                    try:
                        if content_type.startswith('application/json'):
                            body = json.loads(request._raw_body) if request._raw_body else None
                        elif content_type.startswith('multipart/form-data'):
                            body = dict(request.form)
                            # Include files if present
                            if request.files:
                                body['files'] = {k: v.filename for k, v in request.files.items()}
                        elif content_type.startswith('application/x-www-form-urlencoded'):
                            body = dict(request.form)
                        else:
                            # For raw body or other content types
                            try:
                                try:
                                    body = request.json.loads(request._raw_body) if request._raw_body else None
                                except AttributeError:
                                    body = request._raw_body.decode('utf-8')
                            except:
                                body = str(request._raw_body)
                    except Exception as e:
                        print(f"Devzery: Error parsing request body: {e}")
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
                        print("Devzery: No API KEY")
                    if not self.source_name:
                        print("Devzery: No Source Name")

            except Exception as e:
                print(f"Devzery: Error occurred Capturing: {e}")

            return response

else:
    class FlaskRequestResponseLoggingMiddleware:
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "Flask is required to use the Flask middleware. "
                "Install it with: pip install flask"
            )