## Summary 

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
| [G-0] | Empty blocks should be removed or emit something | 1 |



## [Low] Missing `supportsInterface` functions

### description:

According to [EIP-165](https://eips.ethereum.org/EIPS/eip-165), 
a contract’s implementation of the supportsInterface function
should return true for the interfaces that the contract supports. 


**There is `1` instance of this issue:**

- [Bad721](solidity/test_missing_supports_interface.sol#L30) missing `supportsInterface()`.


### recommendation:

Short term, add supportsInterface functions to all contracts that implement a well-known interface. 
Doing so will help to ensure that contracts can interact with external contracts.

Long term, add tests to ensure that each contract’s supportsInterface function returns
true for the interfaces that the contract supports and false for some subset of the
interfaces that the contract does not support. Doing so will help to ensure that the
supportsInterface functions work correctly.


### locations:
- solidity/test_missing_supports_interface.sol#L30

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

## [Optimization] Empty blocks should be removed or emit something

### description:

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [Abstract721.safeTransferFrom(address,address,uint256)](solidity/test_missing_supports_interface.sol#L23-L27) should removed or do something


### recommendation:

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations:
- solidity/test_missing_supports_interface.sol#L23-L27

### severity:
Optimization

### category:
empty-block
