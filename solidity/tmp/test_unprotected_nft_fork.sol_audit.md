## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | NFT doesn't handle hard forks | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables should be cached in stack variables rather than re-reading them from storage | 2 |
| [G-1] | Using custom errors replace `require` or `assert` | 1 |
| [G-2] | State variables that could be declared constant | 2 |



## [Low] NFT doesn't handle hard forks

### description:

When there are hard forks, users often have to go through 
[many hoops](https://twitter.com/elerium115/status/1558471934924431363) to ensure that 
they control ownership on every fork. Consider adding `require(1 == chain.chainId)`, 
or the chain ID of whichever chain you prefer, to the functions below, 
or at least include the chain ID in the URI, 
so that there is no confusion about which chain is the owner of the NFT.



**There is `1` instance of this issue:**

- Protect NFT from copying in forks at the beginning of :
[UnprotectedNFTFork.tokenURI(uint256)](solidity/test_unprotected_nft_fork.sol#L11-L21)

### recommendation:

Add the following check:
```
if(block.chainid != 1) { 
    revert(); 
}
```


### locations:
- solidity/test_unprotected_nft_fork.sol#L11-L21

### severity:
Low

### category:
unprotected-nft-fork

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

## [Optimization] State variables should be cached in stack variables rather than re-reading them from storage

### description:

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `2` instances of this issue:**

- [UnprotectedNFTFork.baseURI](solidity/test_unprotected_nft_fork.sol#L9) should be cached with local memory-based variable in [UnprotectedNFTFork.tokenURI(uint256)](solidity/test_unprotected_nft_fork.sol#L11-L21), It is called more than once:
	- [bytes(baseURI).length > 0](solidity/test_unprotected_nft_fork.sol#L17-L20)
	- [string.concat(baseURI,tokenId.toString())](solidity/test_unprotected_nft_fork.sol#L17-L20)

- [ProtectedNFTFork.baseURI](solidity/test_unprotected_nft_fork.sol#L26) should be cached with local memory-based variable in [ProtectedNFTFork.tokenURI(uint256)](solidity/test_unprotected_nft_fork.sol#L28-L39), It is called more than once:
	- [bytes(baseURI).length > 0](solidity/test_unprotected_nft_fork.sol#L35-L38)
	- [string.concat(baseURI,tokenId.toString())](solidity/test_unprotected_nft_fork.sol#L35-L38)


### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations:
- solidity/test_unprotected_nft_fork.sol#L9
- solidity/test_unprotected_nft_fork.sol#L26

### severity:
Optimization

### category:
reread-state-variables

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool)(1 == block.chainid)](solidity/test_unprotected_nft_fork.sol#L34) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unprotected_nft_fork.sol#L34

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnprotectedNFTFork.baseURI](solidity/test_unprotected_nft_fork.sol#L9) should be constant 

- [ProtectedNFTFork.baseURI](solidity/test_unprotected_nft_fork.sol#L26) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unprotected_nft_fork.sol#L9
- solidity/test_unprotected_nft_fork.sol#L26

### severity:
Optimization

### category:
constable-states
