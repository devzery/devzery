# Devzery Middleware SDK  

The Devzery Middleware SDK enables easy integration of request and response logging functionality into your Django application, enhancing the debugging and monitoring of API requests and responses.

## 🎯 Purpose of Integration  

The Devzery Middleware SDK helps you:  
- **Monitor API traffic**: Capture detailed logs of requests and responses for all API calls in your application.  
- **Debug efficiently**: Identify issues in real-time by analyzing API behavior through captured logs.  
- **Improve reliability**: Track and monitor API performance across environments (e.g., staging, production).  

By integrating this SDK, you can streamline debugging and enhance observability for your microservices.

**Prerequisites**
- Basic understanding of Python and Django.
- Django project set up and running.
- Devzery API Key for integration.

**System Requirements**
- Python version: >= 3.7
- Internet connectivity to send logs to Devzery.



## 🛠️ Quick Start Guide 

### Django

**Step 1:** 📦 Install Devzery

```bash  
pip install devzery
```


**Step 2:** Add the middleware to your Django settings.py file:

Add RequestResponseLoggingMiddleware to the MIDDLEWARE list.
```python
MIDDLEWARE = [
    # Other middlewares...
    "devzery_middleware.middleware.RequestResponseLoggingMiddleware",
]
```


**Step 3:** Configure your Devzery API key and server name:

Add your Devzery API credentials in the settings.py file
```python
DEVZERY_API_KEY = "YOUR_API_KEY"  # Replace with your Devzery API key
DEVZERY_SERVER_NAME = "YOUR_MICROSERVICE_NAME"  # Replace with an identifier for your microservice
```
Make sure to apply the middleware before defining your routes or other middlewares.

Example:
```python
MIDDLEWARE = [
    "devzery_middleware.middleware.RequestResponseLoggingMiddleware",
]

DEVZERY_API_KEY = "YOUR API KEY"
DEVZERY_SERVER_NAME = "ANY NAME AS YOU WISH, FOR YOU TO IDENTIFY THE MICROSERVICE"
```


**Step 4:** Run your Django application

```bash
python manage.py runserver
```

The middleware will now automatically log request and response data for each incoming request.

**Step 5:** Verify SDK Integration:

- Start using your application either by interacting with the User Interface or hitting APIs.
- Go back to the Devzery dahsboard and check for the integration status whether it is successful or not.

### Flask

**Step 1:** 📦 Install Devzery

```bash  
pip install devzery
```
**Step 2:** Add the middleware to your Flask application:
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

**Step 3:** Run your Flask application
```bash
python app.py
```

The middleware will now automatically log request and response data for each incoming request.

**Step 4:** Verify SDK Integration:

- Start using your application either by interacting with the User Interface or hitting APIs.
- Go back to the Devzery dashboard and check for the integration status whether it is successful or not.

## ⚙️ Configuration  
Parameters and Payloads
- `apiKey`: Authenticates requests to the Devzery API. 
- `serverName`: Identifies your Mircoservice in logs. 

| **Prameter**   | **Type**   | **Description**    | **Required**   |
|------------|------------|------------|------------|
| `apiKey` | `String` | Your unique Devzery API key | Yes |
| `serverName` | `String` | Mircoservice name or identifier | Yes |


## 📝 Features and Functionality: 

**Overview of Features**
- Captures request and response data automatically.
- Sends data to Devzery for centralized logging.
- Built-in error handling and debugging logs.

**Detailed Functionality**
- Request Logging: Captures HTTP method, headers, and body.
- Response Logging: Captures status codes, headers, and response body.
- Error Reporting: Logs transmission errors to the console.

## 💡Troubleshooting:

**Verify API Key**:
- Ensure the API key provided is correct and active.  

**Check Microservice Name**:
- Confirm that the server name matches the microservice name and URL being logged. 
 
**Environment Mismatch**:
- Ensure the SDK is integrated into the same environment you want to monitor (e.g., staging or production). e.g., Logs will not appear if APIs are hit on production while Devzery SDK is integrated on staging.

**Middleware not logging data:**
- Ensure the middleware is applied before defining routes.

**Error Codes**
- 401 Unauthorized: Invalid API key.
- 500 Internal Server Error: Devzery server issue.

**Best Practices**
- Use environment variables for sensitive data.
- Apply middleware before any route definitions or other middlewares.
- Monitor console logs during development for debugging.

**Glossary**
- API Key: A unique identifier for authenticating API requests.
- Middleware: A function that processes requests and responses in a python application.

## 🙋 Support:

- Email: support@devzery.com
- Feedback Mechanism: Submit feedback or issues on the [GitHub Repository](https://github.com/devzery/devzery_middleware/issues).

## ⚡ Updates and Version History:

**Changelog:**
- `v1.0.0` Initial release with basic request and response logging.

**License**
- The SDK is distributed under the `Apache 2.0 License`

## 🔗 Links
[![portfolio](https://img.shields.io/badge/Devzery-000?style=for-the-badge&logo=ko-fi&logoColor=pink)](https://www.devzery.com)

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/devzery/)

[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/devzery)
