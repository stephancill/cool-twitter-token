// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.7.0;

import "hardhat/console.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/cryptography/ECDSA.sol";

contract Token is ERC20 {
    using ECDSA for bytes32;
    
    mapping(address => mapping(uint256 => bool)) _seenNonces;
    address _ownerAddress;

    constructor(uint256 initialSupply, address ownerAddress) ERC20("Stephan's Token", "STEPHAN") {
        _mint(ownerAddress, initialSupply);
        _ownerAddress = ownerAddress;
    }

    function externalMint(uint256 amount, uint256 nonce, address claimant, bytes memory sig) public {
        // This recreates the message hash that was signed on the client.
        bytes32 hash = keccak256(abi.encodePacked(amount, nonce, claimant));
        bytes32 messageHash = hash.toEthSignedMessageHash();

        address signer = messageHash.recover(sig);
        
        require(claimant == msg.sender, "Incorrect sender address");
        require(signer == _ownerAddress, "Invalid signature");
        require(!_seenNonces[msg.sender][nonce], "Mint already claimed");
        _seenNonces[msg.sender][nonce] = true;

        _mint(msg.sender, amount);

    }
    
    
}