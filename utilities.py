from web3 import HTTPProvider
from ens import ENS
import config

provider = HTTPProvider(config.WEB3_PROVIDER)
ns = ENS(provider)

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
