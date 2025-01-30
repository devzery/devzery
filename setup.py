from setuptools import setup, find_packages

setup(
    name="devzery",
    version="0.0.7",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'django': ['django>=3.0.0'],
        'flask': ['flask>=2.0.0'],
    },
    author="Devzery",
    author_email="nitish.varma@devzery.com",
    description="Request-Response logging middleware for Django and Flask",
    long_description_content_type="text/markdown",
    url="https://github.com/devzery/devzery",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Flask",
    ],
    python_requires=">=3.6",
)