from eth_account.messages import encode_defunct
from web3 import HTTPProvider, Web3
from ens import ENS
import config
from requests_oauthlib import OAuth1Session

provider = HTTPProvider(config.WEB3_PROVIDER)
ns = ENS(provider)
web3 = Web3(provider=provider)

webhooks_url = f"{config.TWITTER_API_ENDPOINT}/account_activity/all/{config.TWITTER_WEBHOOK_ENV}/webhooks.json"

def get_ens_domain_in_user(twitter_user):
    keys = ["name", "description", "screen_name"]
    potential_domains = [get_ens_domain_in_text(twitter_user[x]) for x in keys]
    potential_domains = [x for x in potential_domains if x]
    if len(potential_domains) > 0:
        return potential_domains[0]
    else:
        return None

def get_ens_domain_in_text(text):
    words = text.split(" ")
    ens = [word for word in words if ".eth" in word]
    if len(ens) > 0:
        return ens[0]
    else:
        return None

def nslookup(domain):
    return ns.address(domain) or ns.owner(domain)

def sign_mint_message(amount, nonce):
    pk = bytes.fromhex(config.CONTRACT_OWNER_PRIVATE_KEY[2:])
    hash = Web3.solidityKeccak(["uint256", "uint256"],[amount, nonce])
    message = encode_defunct(hexstr=hash.hex())
    signed_message = web3.eth.account.sign_message(message, private_key=pk)
    return signed_message

def register_webhook():
    oauth = OAuth1Session(
        client_key=config.TWITTER_CONSUMER_KEY_WEBHOOKS,
        client_secret=config.TWITTER_CONSUMER_SECRET_WEBHOOKS,
        resource_owner_key=config.TWITTER_ACCESS_TOKEN_WEBHOOKS,
        resource_owner_secret=config.TWITTER_ACCESS_TOKEN_SECRET_WEBHOOKS
    )
    r = oauth.post(
        webhooks_url,
        params={
            "url": f"{config.SERVER_ENDPOINT}/webhooks/twitter"
        }
    )

    print(r.json())

def delete_webhook():
    oauth = OAuth1Session(
        client_key=config.TWITTER_CONSUMER_KEY_WEBHOOKS,
        client_secret=config.TWITTER_CONSUMER_SECRET_WEBHOOKS,
        resource_owner_key=config.TWITTER_ACCESS_TOKEN_WEBHOOKS,
        resource_owner_secret=config.TWITTER_ACCESS_TOKEN_SECRET_WEBHOOKS
    )

    webhooks_r = oauth.get(webhooks_url)
    print(webhooks_r.json())
    if webhooks_r.ok and len(webhooks_r.json()) > 0:
        webhook_id = webhooks_r.json()[0]["id"]
    else:
        return

    webhook_delete_url = f"{config.TWITTER_API_ENDPOINT}/account_activity/all/{config.TWITTER_WEBHOOK_ENV}/webhooks/{webhook_id}.json"

    r = oauth.delete(webhook_delete_url)

    if r.ok:
        print("Webhook deleted")
    else:
        print("Failed deleting webhook")

def subscribe_to_owner():
    oauth = OAuth1Session(
        client_key=config.TWITTER_CONSUMER_KEY_WEBHOOKS,
        client_secret=config.TWITTER_CONSUMER_SECRET_WEBHOOKS,
        resource_owner_key=config.TWITTER_ACCESS_TOKEN_WEBHOOKS,
        resource_owner_secret=config.TWITTER_ACCESS_TOKEN_SECRET_WEBHOOKS
    )
    subscriptions_url = f"{config.TWITTER_API_ENDPOINT}/account_activity/all/{config.TWITTER_WEBHOOK_ENV}/subscriptions.json"
    r = oauth.post(subscriptions_url)

    if r.ok:
        print("Subscribed to user")
    else:
        print("Could not subscribe to user")

    
