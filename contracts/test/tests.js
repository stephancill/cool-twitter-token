const { expect } = require("chai");
require("@nomiclabs/hardhat-waffle");
const ethereumjsABI = require("ethereumjs-abi")

async function createSignedMintOrder(account, amount, nonce, claimant) {
  var hash = ethereumjsABI.soliditySHA3(
    ["uint256", "uint256", "address"],
    [amount, nonce, claimant]
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
    var signature = await createSignedMintOrder(accounts[0], amount, nonce, accounts[1].address);

    await token.connect(accounts[1]).externalMint(amount, nonce, accounts[1].address, signature)

    expect(await token.balanceOf(accounts[1].address)).to.equal(amount);

  });

  it("Should handle replay attacks", async function() {
    const accounts = await ethers.getSigners();
    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy(100, accounts[0].address);
    
    await token.deployed();

    var amount = 5;
    var nonce = 1;
    var signature = await createSignedMintOrder(accounts[0], amount, nonce, accounts[1].address);

    await token.connect(accounts[1]).externalMint(amount, nonce, accounts[1].address, signature)

    await expect(token.connect(accounts[1]).externalMint(amount, nonce, accounts[1].address, signature)).to.be.revertedWith("Mint already claimed")
    // await expect(token.connect(accounts[2]).externalMint(amount, nonce, accounts[2].address, signature)).to.be.revertedWith("Mint already claimed")
  });
    
  it("Should handle mints with invalid signatures", async function() {
    const accounts = await ethers.getSigners();
    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy(100, accounts[0].address);
    
    await token.deployed();

    var amount = 5;
    var nonce = 2;
    var signature = await createSignedMintOrder(accounts[0], amount, nonce, accounts[2].address);

    await token.connect(accounts[2]).externalMint(amount, nonce, accounts[2].address, signature)
    expect(await token.balanceOf(accounts[2].address)).to.equal(amount);

    signature = await createSignedMintOrder(accounts[1], amount, nonce, accounts[1].address);
    await expect(token.connect(accounts[1]).externalMint(amount, nonce, accounts[1].address, signature)).to.be.revertedWith("Invalid signature")
  });
    
});
