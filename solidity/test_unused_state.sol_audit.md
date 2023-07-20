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
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused local variables | 1 |
| [G-1] | Not using the named return variables anywhere in the function is confusing | 3 |
| [G-2] | Remove unused parameter variables | 2 |
| [G-3] | Remove or replace unused state variables | 1 |
| [G-4] | Use `delete` to Clear Variables | 3 |
| [G-5] | State variables that could be declared constant | 2 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [UnUsedState.destination](solidity/test_unused_state.sol#L2) is never initialized. It is used in:
	- [UnUsedState.transfer()](solidity/test_unused_state.sol#L7-L9)

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
- solidity/test_unused_state.sol#L2

### severity:
High

### category:
uninitialized-state

## [Low] Don't use `payable.transfer()`/`payable.send()`

### description:

The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. 


**There is `1` instance of this issue:**

- Payable calls in [UnUsedState.transfer()](solidity/test_unused_state.sol#L7-L9):
	- [destination.transfer(msg.value)](solidity/test_unused_state.sol#L8)

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
- solidity/test_unused_state.sol#L7-L9

### severity:
Low

### category:
payable-calls

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

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Variable [UnUsedState.__gap](solidity/test_unused_state.sol#L5) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_unused_state.sol#L5

### severity:
Informational

### category:
naming-convention

## [Optimization] Remove unused local variables

### description:

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The local variables in [UnusedLocalVar.bad0()](solidity/test_unused_state.sol#L65-L70) are unused.
	- [UnusedLocalVar.bad0().b](solidity/test_unused_state.sol#L67)
	- [UnusedLocalVar.bad0().c](solidity/test_unused_state.sol#L68)


### recommendation:

Remove the unused local variables.


### locations:
- solidity/test_unused_state.sol#L65-L70

### severity:
Optimization

### category:
unused-local-var

## [Optimization] Not using the named return variables anywhere in the function is confusing

### description:

Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.


**There are `3` instances of this issue:**

- The named return variables in [UnusedReturnName.bad0()](solidity/test_unused_state.sol#L13-L15) are unused.
	- [UnusedReturnName.bad0().a](solidity/test_unused_state.sol#L13)

- The named return variables in [UnusedReturnName.bad1()](solidity/test_unused_state.sol#L17-L20) are unused.
	- [UnusedReturnName.bad1().b](solidity/test_unused_state.sol#L17)

- The named return variables in [UnusedReturnName.bad2()](solidity/test_unused_state.sol#L22-L25) are unused.
	- [UnusedReturnName.bad2().a](solidity/test_unused_state.sol#L22)


### recommendation:

Remove the unused named return variables.


### locations:
- solidity/test_unused_state.sol#L13-L15
- solidity/test_unused_state.sol#L17-L20
- solidity/test_unused_state.sol#L22-L25

### severity:
Optimization

### category:
unused-named-return-variables

## [Optimization] Remove unused parameter variables

### description:

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [UnusedParameter.bad0(uint256,uint256)](solidity/test_unused_state.sol#L45-L47) are unused.
	- [UnusedParameter.bad0(uint256,uint256).b](solidity/test_unused_state.sol#L45)

- The param variables in [UnusedParameter.bad1(uint256,uint256)](solidity/test_unused_state.sol#L49-L51) are unused.
	- [UnusedParameter.bad1(uint256,uint256).b](solidity/test_unused_state.sol#L49)


### recommendation:

Remove the unused parameter variables.


### locations:
- solidity/test_unused_state.sol#L45-L47
- solidity/test_unused_state.sol#L49-L51

### severity:
Optimization

### category:
unused-parameter

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, 
saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). 
If the variable remains unassigned, there is no gas savings unless the variable is public, 
in which case the compiler-generated non-payable getter deployment cost is saved. 
If the state variable is overriding an interface's public function, 
mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [UnUsedState.unusedState](solidity/test_unused_state.sol#L4) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/test_unused_state.sol#L4

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] Use `delete` to Clear Variables

### description:

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There are `3` instances of this issue:**

- Should use `delete` statement instead of [a = 0](solidity/test_unused_state.sol#L37)

- Should use `delete` statement instead of [a = 0](solidity/test_unused_state.sol#L66)

- Should use `delete` statement instead of [a = 0](solidity/test_unused_state.sol#L73)


### recommendation:

Replacing assignments of zero with delete statements.



### locations:
- solidity/test_unused_state.sol#L37
- solidity/test_unused_state.sol#L66
- solidity/test_unused_state.sol#L73

### severity:
Optimization

### category:
use-delete-statement

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnUsedState.destination](solidity/test_unused_state.sol#L2) should be constant 

- [UnUsedState.unusedState](solidity/test_unused_state.sol#L4) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unused_state.sol#L2
- solidity/test_unused_state.sol#L4

### severity:
Optimization

### category:
constable-states
