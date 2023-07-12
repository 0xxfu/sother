## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `onERC721Received` not implemented in ERC721 received contract | 1 |
| [L-1] | Missing `supportsInterface` functions | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |



## [Medium] Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721

### description:

ERC721 NFTs may get locked forever if the recipient is not aware of ERC721 for some reason. 
While `safeTransferFrom()` is used for ERC1155 NFTs (which has the `_doSafeTransferAcceptanceCheck` 
check on recipient and does not have an option to avoid this), `transferFrom()` is used for 
ERC721 NFTs presumably for gas savings and reentrancy concerns over its `safeTransferFrom` 
variant (which has the `_checkOnERC721Received` check on the recipient).


**There are `2` instances of this issue:**

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37) should be replaced by `safeTransferFrom()`.

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L56) should be replaced by `safeTransferFrom()`.

#### Exploit scenario

if `_to` is a contract address that does not support ERC721, the NFT can be frozen in 
that contract.

As per the documentation of EIP-721:
> A wallet/broker/auction application MUST implement the wallet interface if it will 
accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721


### recommendation:

Evaluate using ERC721 `safeTransferFrom()` to avoid NFTs getting stuck vis-a-vis its 
reentrancy risk and gas costs.


### locations:
- solidity/test_missing_erc721_received.sol#L37
- solidity/test_missing_erc721_received.sol#L56

### severity:
Medium

### category:
unsafe-721-transfer

## [Low] `onERC721Received` not implemented in ERC721 received contract

### description:

The contract does not implement the `onERC721Received` function, 
which is considered a best practice to transfer ERC721 tokens from contracts to contracts. 
The absence of this function could prevent the contract from receiving ERC721 tokens 
from other contracts via `safeTransferFrom/transferFrom`.


**There is `1` instance of this issue:**

- [BadMissReceived](solidity/test_missing_erc721_received.sol#L22-L39) received NFT via following operations by is missing `onERC721Received` function: 
	- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37)
	- [token.safeTransferFrom(msg.sender,address(this),tokenId,new bytes(32))](solidity/test_missing_erc721_received.sol#L24-L29)
	- [token.safeTransferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L33)


### recommendation:

Consider adding an implementation of the `onERC721Received` function in the contract.


### locations:
- solidity/test_missing_erc721_received.sol#L22-L39

### severity:
Low

### category:
missing-erc721-received

## [Low] Missing `supportsInterface` functions

### description:

According to [EIP-165](https://eips.ethereum.org/EIPS/eip-165), 
a contract’s implementation of the supportsInterface function
should return true for the interfaces that the contract supports. 


**There is `1` instance of this issue:**

- [IERC721](solidity/test_missing_erc721_received.sol#L1-L20) missing `supportsInterface()`.


### recommendation:

Short term, add supportsInterface functions to all contracts that implement a well-known interface. 
Doing so will help to ensure that contracts can interact with external contracts.

Long term, add tests to ensure that each contract’s supportsInterface function returns
true for the interfaces that the contract supports and false for some subset of the
interfaces that the contract does not support. Doing so will help to ensure that the
supportsInterface functions work correctly.


### locations:
- solidity/test_missing_erc721_received.sol#L1-L20

### severity:
Low

### category:
missing-supports-interface

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.20

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations:
- 

### severity:
Informational

### category:
solc-version
