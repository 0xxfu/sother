## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Don't use `payable.transfer()`/`payable.send()` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 1 |
| [N-1] | Unused state variable | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 1 |
| [G-1] | State variables that could be declared constant | 2 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [UnUsedState.destination](solidity/test_unused_state.sol#L4) is never initialized. It is used in:
	- [UnUsedState.transfer()](solidity/test_unused_state.sol#L8-L10)

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


### locations:
- solidity/test_unused_state.sol#L4

### severity:
High

### category:
uninitialized-state

## [Low] Don't use `payable.transfer()`/`payable.send()`

### description:

The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. 


**There is `1` instance of this issue:**

- Payable calls in [UnUsedState.transfer()](solidity/test_unused_state.sol#L8-L10):
	- [destination.transfer(msg.value)](solidity/test_unused_state.sol#L9)

#### Exploit scenario

The following cases can cause the transfer to fail:
* The contract does not have a `payable` callback
* The contract's `payable` callback spends more than 2300 gas (which is only enough to emit something)
* The contract is called through a proxy which itself uses up the 2300 gas

Any smart contract that uses `transfer()` or `send()` is taking a hard dependency on gas costs by forwarding a fixed amount of gas: `2300`.
```
contract Vulnerable {
    function withdraw(uint256 amount) external {
        // This forwards 2300 gas, which may not be enough if the recipient
        // is a contract and gas costs change.
        msg.sender.transfer(amount);
    }
}
```


### recommendation:

Use OpenZeppelin's [Address.sendValue()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/2271e2c58d007894c5fe23c4f03a95f645ac9175/contracts/utils/Address.sol#L41-L50) instead of `payable.transfer()`/`payable.send()`


### locations:
- solidity/test_unused_state.sol#L8-L10

### severity:
Low

### category:
payable-calls

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Variable [UnUsedState.__gap](solidity/test_unused_state.sol#L7) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_unused_state.sol#L7

### severity:
Informational

### category:
naming-convention

## [Informational] Unused state variable

### description:
Unused state variable.

**There is `1` instance of this issue:**

- [UnUsedState.__gap](solidity/test_unused_state.sol#L7) is never used in [UnUsedState](solidity/test_unused_state.sol#L3-L11)


### recommendation:
Remove unused state variables.

### locations:
- solidity/test_unused_state.sol#L7

### severity:
Informational

### category:
unused-state

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [UnUsedState.unusedState](solidity/test_unused_state.sol#L6) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/test_unused_state.sol#L6

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnUsedState.unusedState](solidity/test_unused_state.sol#L6) should be constant 

- [UnUsedState.destination](solidity/test_unused_state.sol#L4) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unused_state.sol#L6
- solidity/test_unused_state.sol#L4

### severity:
Optimization

### category:
constable-states
