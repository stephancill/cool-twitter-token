import os

class ImproperlyConfigured(Exception):
    pass

def get_env_value(env_variable, default=None):
    try:
      	return os.environ[env_variable]
    except KeyError:
        if default != None:
            return default
        error_msg = 'Set the {} environment variable'.format(env_variable)
        raise ImproperlyConfigured(error_msg)

DATABASE_URI = get_env_value("DATABASE_URI")
TWITTER_CONSUMER_KEY = get_env_value("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = get_env_value("TWITTER_CONSUMER_SECRET")