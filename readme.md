# Devzery Middleware

A Python package that provides request-response logging middleware for both Django and Flask applications.

## Installation

```bash
# For both Django and Flask support
pip install devzery[all]

# Or

pip install <path-to-local>

# For Django only
pip install devzery-middleware[django]

# For Flask only
pip install devzery-middleware[flask]
```

## Usage

### Django

```python
# settings.py
MIDDLEWARE = [
    'devzery.django.middleware.RequestResponseLoggingMiddleware',
    # ... other middleware
]

DEVZERY_API_KEY = 'your-api-key'
DEVZERY_SOURCE_NAME = 'your-source-name'
DEVZERY_URL = 'your-custom-url'  # optional
```

### Flask

```python
from devzery.flask.middleware import FlaskRequestResponseLoggingMiddleware as DevzeryFlaskMiddleware
from flask import Flask

app = Flask(__name__)
middleware = DevzeryFlaskMiddleware(
    app=app,
    api_key='your-api-key',
    source_name='your-source-name'
)

# Or using factory pattern
app = Flask(__name__)
app.config['DEVZERY_API_KEY'] = 'your-api-key'
app.config['DEVZERY_SOURCE_NAME'] = 'your-source-name'
middleware = DevzeryFlaskMiddleware()
middleware.init_app(app)
```

### Requests

In your app.py or init.py or any file that is executed when your app starts, add the following code:

```python
from devzery import patch_requests

patch_requests() 
```