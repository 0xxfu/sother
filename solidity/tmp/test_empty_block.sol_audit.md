## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Empty blocks should be removed or emit something | 6 |
| [G-1] | Setting the constructor to `payable` | 1 |



## [Medium] Contracts that lock Ether

### description:
Contract with a `payable` function, but without a withdrawal capacity.

**There is `1` instance of this issue:**

- Contract locking ether found:
	Contract `EmptyBlock` (solidity/test_empty_block.sol#L1-L19) has payable functions:
	 - `EmptyBlock.receive()` (solidity/test_empty_block.sol#L6)
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

### recommendation:
Remove the payable attribute or add a withdraw function.

### locations:
- solidity/test_empty_block.sol#L1-L19

### severity:
Medium

### category:
locked-ether

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


**There are `6` instances of this issue:**

- `EmptyBlock.constructor()` (solidity/test_empty_block.sol#L4) should removed or do something

- `EmptyBlock.receive()` (solidity/test_empty_block.sol#L6) should removed or do something

- `EmptyBlock.bad1()` (solidity/test_empty_block.sol#L8) should removed or do something

- `EmptyBlock.bad2()` (solidity/test_empty_block.sol#L10) should removed or do something

- `NotEmptyBlock.notBad1()` (solidity/test_empty_block.sol#L22) should removed or do something

- `NotEmptyBlock.notBad2()` (solidity/test_empty_block.sol#L24) should removed or do something


### recommendation:

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations:
- solidity/test_empty_block.sol#L4
- solidity/test_empty_block.sol#L6
- solidity/test_empty_block.sol#L8
- solidity/test_empty_block.sol#L10
- solidity/test_empty_block.sol#L22
- solidity/test_empty_block.sol#L24

### severity:
Optimization

### category:
empty-block

## [Optimization] Setting the constructor to `payable`

### description:

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- `EmptyBlock.constructor()` (solidity/test_empty_block.sol#L4) should be set to `payable` 


### recommendation:

Set the constructor to `payable`.


### locations:
- solidity/test_empty_block.sol#L4

### severity:
Optimization

### category:
payable-constructor
