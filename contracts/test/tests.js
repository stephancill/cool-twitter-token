const { expect } = require("chai");
require("@nomiclabs/hardhat-waffle");
const ethereumjsABI = require("ethereumjs-abi")
const Web3 = require("web3")

async function createSignedMintOrder(account, amount, nonce) {
  var hash = ethereumjsABI.soliditySHA3(
    ["uint256", "uint256"],
    [amount, nonce]
  );
  const signature = await account.signMessage(hash)
  return signature
}

describe("Token", function() {
  it("Should mint initial supply to correct user", async function() {
    const accounts = await ethers.getSigners();
    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy(100, accounts[0].address);
    
    await token.deployed();
    expect(await token.balanceOf(accounts[0].address)).to.equal(100);
    expect(await token.balanceOf(accounts[0].address)).to.not.equal(101);

  });

  it("Should handle external mints", async function() {
    const accounts = await ethers.getSigners();
    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy(100, accounts[0].address);
    
    await token.deployed();

    var amount = 5;
    var nonce = 1;
    var signature = await createSignedMintOrder(accounts[0], amount, nonce);

    await token.connect(accounts[1]).externalMint(amount, nonce, signature)

    expect(await token.balanceOf(accounts[1].address)).to.equal(amount);
    await expect(token.connect(accounts[1]).externalMint(amount, nonce, signature)).to.be.revertedWith("Mint already claimed")
    await expect(token.connect(accounts[2]).externalMint(amount, nonce, signature)).to.be.revertedWith("Mint already claimed")

    amount = 5;
    nonce = 2;
    signature = await createSignedMintOrder(accounts[0], amount, nonce);

    await token.connect(accounts[2]).externalMint(amount, nonce, signature)
    expect(await token.balanceOf(accounts[2].address)).to.equal(amount);

    signature = await createSignedMintOrder(accounts[1], amount, nonce);
    await expect(token.connect(accounts[1]).externalMint(amount, nonce, signature)).to.be.revertedWith("Signature not by owner address")
  });
});
