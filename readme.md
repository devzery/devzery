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
from devzery import Devzery

MIDDLEWARE = [
    'devzery.django.middleware.DevzeryDjangoMiddleware',
    # ... other middleware
]

DEVZERY_API_KEY = 'your-api-key'
DEVZERY_SOURCE_NAME = 'your-source-name'
DEVZERY_URL = 'your-custom-url'  #only for testing 

# Initialize middleware
devzery = Devzery(
    api_key=DEVZERY_API_KEY,
    source_name=DEVZERY_SOURCE_NAME,
    api_endpoint=DEVZERY_URL 
)
middleware = devzery.django_middleware()
```

### Flask

```python
from devzery import Devzery
from flask import Flask

# Method 1: Pass app during initialization
app = Flask(__name__)
devzery = Devzery(
    app=app,
    api_key='your-api-key',
    source_name='your-source-name'
)
middleware = devzery.flask_middleware()

# Method 2: Using factory pattern
app = Flask(__name__)
devzery = Devzery(
    api_key='your-api-key',
    source_name='your-source-name'
)
middleware = devzery.flask_middleware(app)
```

### Requests

In your app.py or init.py or any file that is executed when your app starts, add the following code:

```python
from devzery import patch_requests

patch_requests() 
```

### Requests

```python
from devzery import Devzery

# Initialize and patch requests
devzery = Devzery(
    api_key='your-api-key',
    source_name='your-source-name'
)
devzery.requests_middleware()
```