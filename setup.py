try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="utility_functions",
    packages=["utility_functions"],
    version="0.1",
    description="utility functions",
    long_description="utility functions",
    author="me",
    author_email="tony.barnett@cloudbuy.com",
    url="localhost",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ], requires=['regex']
)
