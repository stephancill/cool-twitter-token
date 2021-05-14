require("@nomiclabs/hardhat-waffle");

async function main() {
  // We get the contract to deploy
  const accounts = await ethers.getSigners();
  
  const Token = await ethers.getContractFactory("Token");
  const token = await Token.deploy(100, accounts[0].address);
  console.log(accounts[0].privateKey)
  
  await token.deployed();

  console.log("Token deployed to:", token.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
