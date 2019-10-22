from settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=workers,boards,stations,orders,presses,events,materials',
]

CRYPTO_KEY = b'sziAlG_7nlDASeKdYTGAU5jnh0xYHoI-F_OfnpX9XHo='

# token valid time in seconds
TOKEN_VALID_TIME = 8640
