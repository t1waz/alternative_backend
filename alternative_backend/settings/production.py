import os
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

ACCESS_KEY = os.environ['PRODUCTION_ACCESS_TOKEN']
