## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-1] | Using custom errors replace `require` or `assert` | 1 |
| [G-2] | Remove unused parameter variables | 2 |
| [G-3] | Use assembly to check for `address(0)` | 1 |



## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- Pragma version[0.8.17](solidity/tmp/unsafe_721_mint.sol#L2) allows old versions

- solc-0.8.17 is not recommended for deployment


### recommendation

Deploy with any of the following Solidity versions:
- 0.8.21

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations
- solidity/tmp/unsafe_721_mint.sol#L2
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [0.8.17](solidity/tmp/unsafe_721_mint.sol#L2) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/unsafe_721_mint.sol#L2

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(to != address(0),"ERC721: mint to the zero address")](solidity/tmp/unsafe_721_mint.sol#L32) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/unsafe_721_mint.sol#L32

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [ERC721._safeMint(address,uint256,bytes)](solidity/tmp/unsafe_721_mint.sol#L23-L29) are unused.
	- [ERC721._safeMint(address,uint256,bytes)._data](solidity/tmp/unsafe_721_mint.sol#L26)

- The param variables in [ERC721._mint(address,uint256)](solidity/tmp/unsafe_721_mint.sol#L31-L33) are unused.
	- [ERC721._mint(address,uint256).tokenId](solidity/tmp/unsafe_721_mint.sol#L31)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/unsafe_721_mint.sol#L23-L29
- solidity/tmp/unsafe_721_mint.sol#L31-L33

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There is `1` instance of this issue:**

- [require(bool,string)(to != address(0),"ERC721: mint to the zero address")](solidity/tmp/unsafe_721_mint.sol#L32) should use assembly to check for `address(0)`


### recommendation

Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```


### locations
- solidity/tmp/unsafe_721_mint.sol#L32

### severity
Optimization

### category
zero-address-optimization

### confidence
High
