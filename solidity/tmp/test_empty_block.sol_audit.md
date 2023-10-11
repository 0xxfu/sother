## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 1 |
| [M-1] | Void function | 4 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Setting the constructor to `payable` | 1 |
| [G-1] | Empty blocks should be removed or emit something | 5 |



## [Medium] Contracts that lock Ether

### description
Contract with a `payable` function, but without a withdrawal capacity.

**There is `1` instance of this issue:**

- Contract locking ether found:
	Contract [EmptyBlock](solidity/tmp/test_empty_block.sol#L1-L19) has payable functions:
	 - [EmptyBlock.receive()](solidity/tmp/test_empty_block.sol#L6)
	But does not have a function to withdraw the ether

#### Exploit scenario

```solidity
pragma solidity 0.4.24;
contract Locked{
    function receive() payable public{
    }
}
```
Every Ether sent to `Locked` will be lost.

### recommendation
Remove the payable attribute or add a withdraw function.

### locations
- solidity/tmp/test_empty_block.sol#L1-L19

### severity
Medium

### category
locked-ether

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There are `4` instances of this issue:**

- function:[EmptyBlock.bad1()](solidity/tmp/test_empty_block.sol#L8)is empty 

- function:[EmptyBlock.bad2()](solidity/tmp/test_empty_block.sol#L10)is empty 

- function:[NotEmptyBlock.notBad1()](solidity/tmp/test_empty_block.sol#L22)is empty 

- function:[NotEmptyBlock.notBad2()](solidity/tmp/test_empty_block.sol#L24)is empty 

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
- solidity/tmp/test_empty_block.sol#L8
- solidity/tmp/test_empty_block.sol#L10
- solidity/tmp/test_empty_block.sol#L22
- solidity/tmp/test_empty_block.sol#L24

### severity
Medium

### category
void-function

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [EmptyBlock.notBad2()](solidity/tmp/test_empty_block.sol#L16-L18) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_empty_block.sol#L16-L18

### severity
Low

### category
pess-event-setter

### confidence
Medium

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

**There is `1` instance of this issue:**

- function:[ExplicitAbstract.f()](solidity/tmp/test_empty_block.sol#L28)is public and can be replaced with external 

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
- solidity/tmp/test_empty_block.sol#L28

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- [EmptyBlock.constructor()](solidity/tmp/test_empty_block.sol#L4) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/test_empty_block.sol#L4

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `5` instances of this issue:**

- [EmptyBlock.receive()](solidity/tmp/test_empty_block.sol#L6) should removed or do something

- [EmptyBlock.bad1()](solidity/tmp/test_empty_block.sol#L8) should removed or do something

- [EmptyBlock.bad2()](solidity/tmp/test_empty_block.sol#L10) should removed or do something

- [NotEmptyBlock.notBad1()](solidity/tmp/test_empty_block.sol#L22) should removed or do something

- [NotEmptyBlock.notBad2()](solidity/tmp/test_empty_block.sol#L24) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_empty_block.sol#L6
- solidity/tmp/test_empty_block.sol#L8
- solidity/tmp/test_empty_block.sol#L10
- solidity/tmp/test_empty_block.sol#L22
- solidity/tmp/test_empty_block.sol#L24

### severity
Optimization

### category
empty-block

### confidence
High
