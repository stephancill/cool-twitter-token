import base64
import config
from functools import wraps
import hashlib
import hmac
from itsdangerous import TimedJSONWebSignatureSerializer
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from models import Account
from requests_oauthlib import OAuth1Session
from sanic import response
import sanic
from session import Session
import utilities

app = sanic.Sanic(__name__)
app.update_config("./config.py")

env = Environment(
    loader=FileSystemLoader("templates/"),
    autoescape=select_autoescape(["html"])
)
app.ctx.env = env
serializer = TimedJSONWebSignatureSerializer(config.SECRET_KEY, expires_in=60*60)

@app.middleware('request')
async def add_session(request):
    request.ctx.db = Session()

@app.middleware("response")
async def close_session(request, response):
    if "db" in request.ctx.__dict__:
        try:
            request.ctx.db.commit()
        finally:
            db: Session = request.ctx.db
            db.close()

def inject_account():
    def decorator(f):
        @wraps(f)
        def decorated_function(request, *args, **kwargs):
            serialized_token = request.cookies.get("token")
            user_str = serializer.loads(serialized_token)
            user = json.loads(user_str)
                
            account = request.ctx.db.query(Account).filter(Account.twitter_id == user["id"]).first()
            if user and not account:
                account = Account(twitter_id=user["id"], balance=0)
                request.ctx.db.add(account)

            return f(request, account=account, user_name=user.get("name"), *args, **kwargs)
        return decorated_function
    return decorator


@app.get("/")
async def root(request):
    template = request.app.ctx.env.get_template("home.html")
    html = template.render(request=request)
    return response.html(html)

@app.get("/login")
async def login_redirect(request):
    callback_endpoint = request.app.url_for("login_callback")
    request_token_url = f"https://api.twitter.com/oauth/request_token"

    oauth = OAuth1Session(
        client_key=config.TWITTER_CONSUMER_KEY_AUTH,
        client_secret=config.TWITTER_CONSUMER_SECRET_AUTH,
        callback_uri=f"{config.SERVER_ENDPOINT}{callback_endpoint}"
    )
    fetch_response = oauth.fetch_request_token(request_token_url)

    if fetch_response:
        base_authorization_url = f"https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        return response.redirect(authorization_url)
    else:
        template = request.app.ctx.env.get_template("error.html")
        html = template.render(request=request)
        return response.html(html)
    

@app.get("/login-callback")
async def login_callback(request):
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    oauth = OAuth1Session(
        client_key=config.TWITTER_CONSUMER_KEY_AUTH, 
        client_secret=config.TWITTER_CONSUMER_SECRET_AUTH
    )
    oauth.parse_authorization_response(request.url)
    oauth.fetch_access_token(access_token_url)

    r = oauth.get(f"{config.TWITTER_API_ENDPOINT}/account/verify_credentials.json")
    res = response.redirect(request.app.url_for("claim_page"))
    if r.ok:
        r_json = r.json()
        twitter_id = str(r_json["id"])
        twitter_name = str(r_json["screen_name"])
        user = {
            "id": twitter_id,
            "name": twitter_name
        }
        user_str = json.dumps(user)
        res.cookies["token"] = serializer.dumps(user_str).decode()
    else:
        res = response.redirect(request.app.url_for("root"))

    return res

@app.get("/claim")
@inject_account()
async def claim_page(request, account: Account, user_name):
    template = request.app.ctx.env.get_template("claim.html")
    html = template.render(request=request, account=account, user_name=user_name)
    return response.html(html)

# Defines a route for the GET request
@app.get('/webhooks/twitter')
async def webhook_challenge(request):

    # creates HMAC SHA-256 hash from incomming token and your consumer secret
    sha256_hash_digest = hmac.new(config.TWITTER_CONSUMER_SECRET_WEBHOOKS.encode(), msg=request.args.get('crc_token').encode(), digestmod=hashlib.sha256).digest()

    # construct response data with base64 encoded hash
    response = {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode()
    }

    # returns properly formatted json response
    return sanic.response.json(response)

@app.post('/webhooks/twitter')
async def receive_webhook(request):
    for event in request.json.get("favorite_events", []):
        twitter_user = event["user"]
        print(json.dumps(event["user"]["name"]))
        ens_domain = utilities.get_ens_domain_in_user(twitter_user)
        if ens_domain:
            address = utilities.nslookup(ens_domain)
            # TODO: Send tokens
        else:
            twitter_id = str(twitter_user["id"])
            account = request.ctx.db.query(Account).filter(Account.twitter_id == twitter_id).first()
            if account:
                account.balance += 1
            else:
                account = Account(twitter_id=twitter_id, balance=1)
            request.ctx.db.add(account)
                
    return response.empty()


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, workers=1, debug=True)

