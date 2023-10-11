## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing `supportsInterface` functions | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 3 |
| [G-1] | Empty blocks should be removed or emit something | 1 |



## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There is `1` instance of this issue:**

- function:[Abstract721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_missing_supports_interface.sol#L23-L27)is empty 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Implement the function

### locations
- solidity/tmp/test_missing_supports_interface.sol#L23-L27

### severity
Medium

### category
void-function

### confidence
High

## [Low] Missing `supportsInterface` functions

### description

According to [EIP-165](https://eips.ethereum.org/EIPS/eip-165), 
a contract’s implementation of the supportsInterface function
should return true for the interfaces that the contract supports. 


**There is `1` instance of this issue:**

- [Bad721](solidity/tmp/test_missing_supports_interface.sol#L30) missing `supportsInterface()`.


### recommendation

Short term, add supportsInterface functions to all contracts that implement a well-known interface. 
Doing so will help to ensure that contracts can interact with external contracts.

Long term, add tests to ensure that each contract’s supportsInterface function returns
true for the interfaces that the contract supports and false for some subset of the
interfaces that the contract does not support. Doing so will help to ensure that the
supportsInterface functions work correctly.


### locations
- solidity/tmp/test_missing_supports_interface.sol#L30

### severity
Low

### category
missing-supports-interface

### confidence
High

## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

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
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `4` instances of this issue:**

- function:[ERC165.supportsInterface(bytes4)](solidity/tmp/test_missing_supports_interface.sol#L8-L15)is public and can be replaced with external 

- function:[Abstract721.ownerOf(uint256)](solidity/tmp/test_missing_supports_interface.sol#L19-L21)is public and can be replaced with external 

- function:[Abstract721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_missing_supports_interface.sol#L23-L27)is public and can be replaced with external 

- function:[NotBad721.supportsInterface(bytes4)](solidity/tmp/test_missing_supports_interface.sol#L33-L43)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/test_missing_supports_interface.sol#L8-L15
- solidity/tmp/test_missing_supports_interface.sol#L19-L21
- solidity/tmp/test_missing_supports_interface.sol#L23-L27
- solidity/tmp/test_missing_supports_interface.sol#L33-L43

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `3` instances of this issue:**

- The param variables in [Abstract721.ownerOf(uint256)](solidity/tmp/test_missing_supports_interface.sol#L19-L21) are unused.
	- [Abstract721.ownerOf(uint256).tokenId](solidity/tmp/test_missing_supports_interface.sol#L19)

- The param variables in [Abstract721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_missing_supports_interface.sol#L23-L27) are unused.
	- [Abstract721.safeTransferFrom(address,address,uint256).from](solidity/tmp/test_missing_supports_interface.sol#L24)
	- [Abstract721.safeTransferFrom(address,address,uint256).to](solidity/tmp/test_missing_supports_interface.sol#L25)
	- [Abstract721.safeTransferFrom(address,address,uint256).tokenId](solidity/tmp/test_missing_supports_interface.sol#L26)

- The param variables in [Abstract721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_missing_supports_interface.sol#L23-L27) are unused.
	- [Abstract721.safeTransferFrom(address,address,uint256).from](solidity/tmp/test_missing_supports_interface.sol#L24)
	- [Abstract721.safeTransferFrom(address,address,uint256).tokenId](solidity/tmp/test_missing_supports_interface.sol#L26)
	- [Abstract721.safeTransferFrom(address,address,uint256).to](solidity/tmp/test_missing_supports_interface.sol#L25)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_missing_supports_interface.sol#L19-L21
- solidity/tmp/test_missing_supports_interface.sol#L23-L27
- solidity/tmp/test_missing_supports_interface.sol#L23-L27

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [Abstract721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_missing_supports_interface.sol#L23-L27) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_missing_supports_interface.sol#L23-L27

### severity
Optimization

### category
empty-block

### confidence
High
