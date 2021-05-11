import base64
from contextvars import ContextVar 
import hashlib
import hmac
import json
import sanic
from session import bind
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


app = sanic.Sanic(__name__)
app.update_config("./config.py")

_base_model_session_ctx = ContextVar("session")

@app.middleware("request")
async def inject_session(request):
    request.ctx.session = sessionmaker(bind, AsyncSession, expire_on_commit=False)()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


# Defines a route for the GET request
@app.get('/webhooks/twitter')
async def webhook_challenge(request):

    # creates HMAC SHA-256 hash from incomming token and your consumer secret
    sha256_hash_digest = hmac.new(request.app.config.TWITTER_CONSUMER_SECRET.encode(), msg=request.args.get('crc_token').encode(), digestmod=hashlib.sha256).digest()

    # construct response data with base64 encoded hash
    response = {
        'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode()
    }

    # returns properly formatted json response
    return sanic.response.json(response)

@app.post('/webhooks/twitter')
async def receive_webhook(request):
    for event in request.json.get("favorite_events"):
        print(json.dumps(event["user"]["name"]))
    return sanic.response.empty()


if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, workers=1, debug=True)

