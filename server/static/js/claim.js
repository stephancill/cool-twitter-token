document.addEventListener('DOMContentLoaded', windowLoaded, false);

let _contract
const contractAddress = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
let BN

const ethEnabled = async () => {
  if (window.ethereum) {
    await window.ethereum.send("eth_requestAccounts")
    window.web3 = new Web3(window.ethereum)
    var accounts = await window.web3.eth.getAccounts()
    window.web3.eth.defaultAccount = accounts[0]
    BN = window.web3.utils.BN;
    return true 
  }
  return false
}

async function getContract() {
  // Contract ABI
  if (_contract) {
    return _contract.clone()
  }
  let contractJSON = await fetch("/static/artifacts/Token.sol/Token.json")
  if (contractJSON.ok) {
    contractJSON = await contractJSON.json()
  } else {
    alert("Something went wrong fetching contract ABI")
  }
  _contract = new window.web3.eth.Contract(contractJSON.abi, contractAddress)
  return _contract
}

async function claimButtonClicked() {
  try {
    var connected = await ethEnabled()
    if (!connected) {
      alert("Metamask not connected")
      return
    }
  } catch (error) {
    alert(error.message)
    return
  }
  
  // Claim signature
  let claimAddress = window.web3.eth.defaultAccount
  let claimTx = await fetch(`/claim-tx?address=${claimAddress}`)
  if (claimTx.ok) {
    claimTx = await claimTx.json()
  } else {
    alert("Something went wrong fetching claim signature")
  }

  let contract = await getContract()
  
  const tx = await contract.methods.externalMint(new BN(claimTx.amount), claimTx.nonce, claimAddress, claimTx.signature).send({from: window.web3.eth.defaultAccount}, )

  if (tx.status) {
    let r = await fetch("/expire-nonce", {
      method: "POST"
    })

    if (r.ok) {
      location.reload()
    } else {
      alert("Something went wrong updating your balance. Please try again later")
    } 
  }

}

async function addToWalletClicked() {
  if (!(await ethEnabled())) {
    return
  }

  let contract = await getContract()
  if (!contract) {
    return
  }

  var decimals = await contract.methods.decimals().call()
  var tokenImage = `${window.location.origin}/favicon.ico`
  var tokenSymbol = await contract.methods.symbol().call()

  try {
    await ethereum.request({
      method: 'wallet_watchAsset',
      params: {
        type: 'ERC20', // Initially only supports ERC20, but eventually more!
        options: {
          address: contractAddress, // The address that the token is at.
          symbol: tokenSymbol, // A ticker symbol or shorthand, up to 5 chars.
          decimals: decimals, // The number of decimals in the token
          image: tokenImage, // A string url of the token logo
        },
      },
    });
  } catch (e) {
    console.error(e)
  }
  
}

async function windowLoaded() {
  console.log("onload")
}