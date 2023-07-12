## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 4 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `onERC721Received` not implemented in ERC721 received contract | 1 |
| [L-1] | `onERC721Received` callback is never called when new tokens are minted or transferred | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 2 |
| [N-2] | Missing inheritance | 1 |



## [Medium] Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721

### description:

ERC721 NFTs may get locked forever if the recipient is not aware of ERC721 for some reason. 
While `safeTransferFrom()` is used for ERC1155 NFTs (which has the `_doSafeTransferAcceptanceCheck` 
check on recipient and does not have an option to avoid this), `transferFrom()` is used for 
ERC721 NFTs presumably for gas savings and reentrancy concerns over its `safeTransferFrom` 
variant (which has the `_checkOnERC721Received` check on the recipient).


**There are `4` instances of this issue:**

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37) should be replaced by `safeTransferFrom()`.

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L56) should be replaced by `safeTransferFrom()`.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/test_missing_erc721_received.sol#L84) should be replaced by `safeTransferFrom()`.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/test_missing_erc721_received.sol#L136) should be replaced by `safeTransferFrom()`.

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
- solidity/test_missing_erc721_received.sol#L84
- solidity/test_missing_erc721_received.sol#L136

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

- [BadMissReceived](solidity/test_missing_erc721_received.sol#L22-L39) received NFT via following operations is missing `onERC721Received` function: 
	- [token.safeTransferFrom(msg.sender,address(this),tokenId,new bytes(32))](solidity/test_missing_erc721_received.sol#L24-L29)
	- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37)
	- [token.safeTransferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L33)


### recommendation:

Consider adding an implementation of the `onERC721Received` function in the contract.


### locations:
- solidity/test_missing_erc721_received.sol#L22-L39

### severity:
Low

### category:
missing-erc721-received

## [Low] `onERC721Received` callback is never called when new tokens are minted or transferred

### description:

The ERC721 implementation used by the contract does not properly call the
corresponding callback when new tokens are minted or transferred.

The ERC721 standard states that the onERC721Received callback must be called when a
mint or transfer operation occurs.

However, the smart contracts interacting as users of the contracts will not be
notified with the `onERC721Received` callback, as expected according to the ERC721
standard.


**There are `3` instances of this issue:**

- [token.safeTransferFrom(address(this),msg.sender,tokenId,new bytes(32))](solidity/test_missing_erc721_received.sol#L71-L76) unchecked `onERC721Received` callback.

- [token.safeTransferFrom(address(this),msg.sender,tokenId)](solidity/test_missing_erc721_received.sol#L80) unchecked `onERC721Received` callback.

- [token.transferFrom(address(this),msg.sender,tokenId)](solidity/test_missing_erc721_received.sol#L84) unchecked `onERC721Received` callback.

#### Exploit scenario

Alice deploys a contract to interact with the Controller contract to send and receive
ERC721 tokens. Her contract correctly implements the `onERC71Received` callback, but this
is not called when tokens are minted or transferred back to her contract. As a result, the
tokens are trapped.


### recommendation:

Short term, ensure that the ERC721 implementations execute the standard callback when
they are required.

Example see OpenZeppelin implementation: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/8b72e20e326078029b92d526ff5a44add2671df1/contracts/token/ERC721/ERC721.sol#L425-L447


### locations:
- solidity/test_missing_erc721_received.sol#L71-L76
- solidity/test_missing_erc721_received.sol#L80
- solidity/test_missing_erc721_received.sol#L84

### severity:
Low

### category:
unchecked-erc721-received

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

## [Informational] Assembly usage

### description:
The use of assembly is error-prone and should be avoided.

**There are `2` instances of this issue:**

- [NotBadChecked.deposit(IERC721,uint256)](solidity/test_missing_erc721_received.sol#L98-L126) uses assembly
	- [INLINE ASM](solidity/test_missing_erc721_received.sol#L121-L123)

- [NotBadChecked._checkOnERC721Received(address,address,uint256,bytes)](solidity/test_missing_erc721_received.sol#L142-L170) uses assembly
	- [INLINE ASM](solidity/test_missing_erc721_received.sol#L162-L164)


### recommendation:
Do not use `evm` assembly.

### locations:
- solidity/test_missing_erc721_received.sol#L98-L126
- solidity/test_missing_erc721_received.sol#L142-L170

### severity:
Informational

### category:
assembly

## [Informational] Missing inheritance

### description:
Detect missing inheritance.

**There is `1` instance of this issue:**

- [NotBad](solidity/test_missing_erc721_received.sol#L41-L67) should inherit from [IERC721Receiver](solidity/test_missing_erc721_received.sol#L88-L95)

#### Exploit scenario

```solidity
interface ISomething {
    function f1() external returns(uint);
}

contract Something {
    function f1() external returns(uint){
        return 42;
    }
}
```
`Something` should inherit from `ISomething`. 


### recommendation:
Inherit from the missing interface or contract.

### locations:
- solidity/test_missing_erc721_received.sol#L41-L67

### severity:
Informational

### category:
missing-inheritance
