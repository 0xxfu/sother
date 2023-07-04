## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Setting the constructor to `payable` | 2 |



## [Medium] Contracts that lock Ether

### description:
Contract with a `payable` function, but without a withdrawal capacity.

**There are `2` instances of this issue:**

- Contract locking ether found:
	Contract `NotBad` (solidity/test_payable_constructor.sol#L9-L11) has payable functions:
	 - `NotBad.constructor(address)` (solidity/test_payable_constructor.sol#L10)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract `NotBad2` (solidity/test_payable_constructor.sol#L13-L15) has payable functions:
	 - `NotBad2.constructor()` (solidity/test_payable_constructor.sol#L14)
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
- solidity/test_payable_constructor.sol#L9-L11
- solidity/test_payable_constructor.sol#L13-L15

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

## [Optimization] Setting the constructor to `payable`

### description:

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `2` instances of this issue:**

- `Bad.constructor(address)` (solidity/test_payable_constructor.sol#L2) should be set to `payable` 

- `Bad2.constructor()` (solidity/test_payable_constructor.sol#L6) should be set to `payable` 


### recommendation:

Set the constructor to `payable`.


### locations:
- solidity/test_payable_constructor.sol#L2
- solidity/test_payable_constructor.sol#L6

### severity:
Optimization

### category:
payable-constructor
