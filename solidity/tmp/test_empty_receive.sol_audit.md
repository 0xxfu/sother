## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |
| [H-1] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 1 |
| [G-1] | Empty blocks should be removed or emit something | 1 |
| [G-2] | State variables that could be declared constant | 1 |
| [G-3] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There is `1` instance of this issue:**

- [NotBad.weth](solidity/tmp/test_empty_receive.sol#L6) is never initialized. It is used in:
	- [NotBad.receive()](solidity/tmp/test_empty_receive.sol#L8-L10)

#### Exploit scenario

```solidity
contract Uninitialized{
    address destination;

    function transfer() payable public{
        destination.transfer(msg.value);
    }
}
```
Bob calls `transfer`. As a result, the Ether are sent to the address `0x0` and are lost.


### recommendation

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### locations
- solidity/tmp/test_empty_receive.sol#L6

### severity
High

### category
uninitialized-state

### confidence
High

## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [NotBad.weth](solidity/tmp/test_empty_receive.sol#L6) not initialized and not written in contract but be used in contract

#### Exploit scenario

```solidity
    struct BalancesStruct{
        address owner;
        array[]] balances;
    }
    array[] public stackBalance;

    function remove() internal{
         delete stackBalance[msg.sender];
    }
```
`remove` deletes an item of `stackBalance`.
The array `balances` is never deleted, so `remove` does not work as intended.

### recommendation
Use a lock mechanism instead of a deletion to disable structure containing a array.

### locations
- solidity/tmp/test_empty_receive.sol#L6

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Contracts that lock Ether

### description
Contract with a `payable` function, but without a withdrawal capacity.

**There are `2` instances of this issue:**

- Contract locking ether found:
	Contract [Bad](solidity/tmp/test_empty_receive.sol#L1-L3) has payable functions:
	 - [Bad.receive()](solidity/tmp/test_empty_receive.sol#L2)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract [NotBad](solidity/tmp/test_empty_receive.sol#L5-L11) has payable functions:
	 - [NotBad.receive()](solidity/tmp/test_empty_receive.sol#L8-L10)
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
- solidity/tmp/test_empty_receive.sol#L1-L3
- solidity/tmp/test_empty_receive.sol#L5-L11

### severity
Medium

### category
locked-ether

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [NotBad.receive()](solidity/tmp/test_empty_receive.sol#L8-L10) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_empty_receive.sol#L8-L10

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

## [Informational] ..

### description
..

**There is `1` instance of this issue:**

- require() missing error messages
	 - [require(bool)(msg.sender == address(weth))](solidity/tmp/test_empty_receive.sol#L9)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_empty_receive.sol#L9

### severity
Informational

### category
error-msg

### confidence
Medium

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool)(msg.sender == address(weth))](solidity/tmp/test_empty_receive.sol#L9) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_empty_receive.sol#L9

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [Bad.receive()](solidity/tmp/test_empty_receive.sol#L2) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_empty_receive.sol#L2

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [NotBad.weth](solidity/tmp/test_empty_receive.sol#L6) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_empty_receive.sol#L6

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [NotBad.weth](solidity/tmp/test_empty_receive.sol#L6) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_empty_receive.sol#L6

### severity
Optimization

### category
state-should-be-constant

### confidence
High
