# $COOL

## Running
1. Copy env.template into `.env` and populate
2. `docker-compose up -d`
3. Server will be running on port 8080

## Deploy
1. `cd contracts`
2. `yarn hardhat node`
3. `yarn hardhat --network localhost run scripts/deploy.js`
4. Copy deployment address from output and enter it in `server/static/js/claim.js`

## TODO
[ ] Move contract dev environment to brownie
[ ] Bridge on different networks and L2s