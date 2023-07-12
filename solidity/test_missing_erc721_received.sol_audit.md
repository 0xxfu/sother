## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Incompatibility with transfer-on-fee or deflationary tokens | 2 |
| [M-1] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing `supportsInterface` functions | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Amounts should be checked for `0` before calling a `transfer` | 2 |



## [Medium] Incompatibility with transfer-on-fee or deflationary tokens

### description:

Some ERC20 tokens make modifications to the standard implementations of
their ERC20’s `transfer` or `balanceOf` functions.
One type of such token is deflationary tokens that charge a fee on every
`transfer()` and `transferFrom()`.
The protocol does not have incompatibility with fee-on-transfer tokens.

Note that there has been a real-world exploit related to this with 
[Balancer pool and STA deflationary tokens](https://medium.com/1inch-network/balancer-hack-2020-a8f7131c980e).


**There are `2` instances of this issue:**

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37) with fee on transfer are not supported.

- [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L56) with fee on transfer are not supported.

#### Exploit scenario

i.e. Fee-on-transfer scenario:
1. Contract calls transfer from contractA 100 tokens to current contract
2. Current contract thinks it received 100 tokens
3. It updates balances to increase +100 tokens
4. While actually contract received only 90 tokens
5. That breaks whole math for given token


### recommendation:

1. Consider comparing before and after balance to get the actual transferred amount.
2. Alternatively, disallow tokens with fee-on-transfer mechanics to be added as tokens.


### locations:
- solidity/test_missing_erc721_received.sol#L37
- solidity/test_missing_erc721_received.sol#L56

### severity:
Medium

### category:
fee-on-transfer

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

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description:

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `2` instances of this issue:**

- Adding a non-zero-value check for [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L37) at the beginning of [BadMissReceived.deposit3(IERC721,uint256)](solidity/test_missing_erc721_received.sol#L36-L38)

- Adding a non-zero-value check for [token.transferFrom(msg.sender,address(this),tokenId)](solidity/test_missing_erc721_received.sol#L56) at the beginning of [NotBad.deposit3(IERC721,uint256)](solidity/test_missing_erc721_received.sol#L55-L57)


### recommendation:

Consider adding a non-zero-value check at the beginning of function.


### locations:
- solidity/test_missing_erc721_received.sol#L37
- solidity/test_missing_erc721_received.sol#L56

### severity:
Optimization

### category:
zero-check-with-transfer
