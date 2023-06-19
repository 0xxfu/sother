## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 1 |
| [G-1] | State variables that could be declared constant | 2 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [Uninitialized.destination](solidity/test_unused_state.sol#L4) is never initialized. It is used in:
	- [Uninitialized.transfer()](solidity/test_unused_state.sol#L8-L10)

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


### recommendation:

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### location:
- solidity/test_unused_state.sol#L4

### severity:
High

### category:
uninitialized-state

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [Uninitialized.unusedState](solidity/test_unused_state.sol#L6) is never used.

### recommendation:

Remove or replace the unused state variables


### location:
- solidity/test_unused_state.sol#L6

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [Uninitialized.unusedState](solidity/test_unused_state.sol#L6) should be constant 

- [Uninitialized.destination](solidity/test_unused_state.sol#L4) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### location:
- solidity/test_unused_state.sol#L6
- solidity/test_unused_state.sol#L4

### severity:
Optimization

### category:
constable-states
