## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Use `_safeMint` instead of `_mint` for ERC721 | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Reduce gas usage by moving to Solidity 0.8.20 or later | 1 |
| [G-1] | use custom errors instead of revert strings | 1 |



## [Medium] Use `_safeMint` instead of `_mint` for ERC721

### description:

`_mint()` is [discouraged](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/d4d8d2ed9798cc3383912a23b5e8d5cb602f7d4b/contracts/token/ERC721/ERC721.sol#L271) in favor of `_safeMint()` 
which ensures that the recipient is either an EOA or implements `IERC721Receiver`. 
Both [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/d4d8d2ed9798cc3383912a23b5e8d5cb602f7d4b/contracts/token/ERC721/ERC721.sol#L238-L250) and [solmate](https://github.com/Rari-Capital/solmate/blob/4eaf6b68202e36f67cab379768ac6be304c8ebde/src/tokens/ERC721.sol#L180) 
have versions of this function


**There is `1` instance of this issue:**

- [_mint(to,tokenId)](solidity/unsafe_721_mint.sol#L38) should be replaced by `_safeMint()`.

#### Exploit scenario

if `to` is a contract address that does not support ERC721, the NFT can be frozen in the contract.

As per the documentation of EIP-721:

> A wallet/broker/auction application MUST implement the wallet interface if it will accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721

As per the documentation of ERC721.sol by Openzeppelin

Ref: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L260-L272

```
    /**
     * @dev Mints `tokenId` and transfers it to `to`.
     *
     * WARNING: Usage of this method is discouraged, use {_safeMint} whenever possible
     *
     * Requirements:
     *
     * - `tokenId` must not exist.
     * - `to` cannot be the zero address.
     *
     * Emits a {Transfer} event.
     */
    function _mint(address to, uint256 tokenId) internal virtual {
```



### recommendation:

Use `_safeMint` instead of `_mint` to check received address support for ERC721 implementation.

Ref: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol#L249-L258



### locations:
- solidity/unsafe_721_mint.sol#L38

### severity:
Medium

### category:
unsafe-721-mint

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- Pragma version[0.8.19](solidity/unsafe_721_mint.sol#L2) allows old versions

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
- solidity/unsafe_721_mint.sol#L2
- 

### severity:
Informational

### category:
solc-version

## [Optimization] Reduce gas usage by moving to Solidity 0.8.20 or later

### description:
See this [link](https://blog.soliditylang.org/2023/02/22/solidity-0.8.19-release-announcement/#preventing-dead-code-in-runtime-bytecode) for the full details

**There is `1` instance of this issue:**

- pragma solidity version [0.8.19](solidity/unsafe_721_mint.sol#L2) should upgrade to the latest version: 0.8.20

### recommendation:
Upgrade solidity version to the latest version: 0.8.20

### locations:
- solidity/unsafe_721_mint.sol#L2

### severity:
Optimization

### category:
upgrade-to-latest

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(to != address(0),ERC721: mint to the zero address)](solidity/unsafe_721_mint.sol#L32) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/unsafe_721_mint.sol#L32

### severity:
Optimization

### category:
use-custom-error
