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

WEB3_PROVIDER = get_env_value("WEB3_PROVIDER")
CONTRACT_OWNER_PRIVATE_KEY = get_env_value("CONTRACT_OWNER_PRIVATE_KEY")

SERVER_ENDPOINT = get_env_value("SERVER_ENDPOINT")
SECRET_KEY = get_env_value("SECRET_KEY")

TWITTER_API_ENDPOINT = get_env_value("TWITTER_API_ENDPOINT")
TWITTER_CONSUMER_KEY_WEBHOOKS = get_env_value("TWITTER_CONSUMER_KEY_WEBHOOKS")
TWITTER_CONSUMER_SECRET_WEBHOOKS = get_env_value("TWITTER_CONSUMER_SECRET_WEBHOOKS")
TWITTER_ACCESS_TOKEN_WEBHOOKS = get_env_value("TWITTER_ACCESS_TOKEN_WEBHOOKS")
TWITTER_ACCESS_TOKEN_SECRET_WEBHOOKS = get_env_value("TWITTER_ACCESS_TOKEN_SECRET_WEBHOOKS")

TWITTER_CONSUMER_KEY_AUTH = get_env_value("TWITTER_CONSUMER_KEY_AUTH")
TWITTER_CONSUMER_SECRET_AUTH = get_env_value("TWITTER_CONSUMER_SECRET_AUTH")
TWITTER_WEBHOOK_ENV = get_env_value("TWITTER_WEBHOOK_ENV")