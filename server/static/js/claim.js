document.addEventListener('DOMContentLoaded', windowLoaded, false);

const ethEnabled = async () => {
  if (window.ethereum) {
    await window.ethereum.send("eth_requestAccounts")
    window.web3 = new Web3(window.ethereum)
    return true 
  }
  return false
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
  

  let claimTx = await fetch("/claim-tx").then(data => data.json())
  console.log(claimTx)
  
}

async function windowLoaded() {
  console.log("onload")
}