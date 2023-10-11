## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Write after write | 1 |
| [M-1] | Integer Overflow and Underflow | 11 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 7 |
| [L-1] | Events are missing sender information | 1 |
| [L-2] | Missing Event Setter | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache state variables instead of rereading | 2 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 1 |



## [Medium] Write after write

### description
Detects variables that are written but never read and written again.

**There is `1` instance of this issue:**

- [RereadStateVariables.stateUint256](solidity/tmp/test_reread_state_variables.sol#L4) is written in both
	[stateUint256 = x + 1](solidity/tmp/test_reread_state_variables.sol#L21)
	[stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L23)

#### Exploit scenario

    ```solidity
    contract Buggy{
        function my_func() external initializer{
            // ...
            a = b;
            a = c;
            // ..
        }
    }
    ```
    `a` is first asigned to `b`, and then to `c`. As a result the first write does nothing.

### recommendation
Fix or remove the writes.

### locations
- solidity/tmp/test_reread_state_variables.sol#L4

### severity
Medium

### category
write-after-write

### confidence
High

## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `11` instances of this issue:**

- bad(uint256) has possible integer overflow/underflow:
	- [a = stateUint256 + 1](solidity/tmp/test_reread_state_variables.sol#L9)

- bad(uint256) has possible integer overflow/underflow:
	- [b = stateUint256 + x](solidity/tmp/test_reread_state_variables.sol#L10)

- bad(uint256) has possible integer overflow/underflow:
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L11)

- bad2(uint256) has possible integer overflow/underflow:
	- [a = stateUint256 + x](solidity/tmp/test_reread_state_variables.sol#L15)

- notBad(uint256) has possible integer overflow/underflow:
	- [a = stateUint256 + 1](solidity/tmp/test_reread_state_variables.sol#L20)

- notBad(uint256) has possible integer overflow/underflow:
	- [stateUint256 = x + 1](solidity/tmp/test_reread_state_variables.sol#L21)

- notBad(uint256) has possible integer overflow/underflow:
	- [b = stateUint256 + x](solidity/tmp/test_reread_state_variables.sol#L22)

- notBad(uint256) has possible integer overflow/underflow:
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L23)

- good(uint256) has possible integer overflow/underflow:
	- [a = tmpState + 1](solidity/tmp/test_reread_state_variables.sol#L28)

- good(uint256) has possible integer overflow/underflow:
	- [b = tmpState + x](solidity/tmp/test_reread_state_variables.sol#L29)

- good(uint256) has possible integer overflow/underflow:
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L30)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_reread_state_variables.sol#L9
- solidity/tmp/test_reread_state_variables.sol#L10
- solidity/tmp/test_reread_state_variables.sol#L11
- solidity/tmp/test_reread_state_variables.sol#L15
- solidity/tmp/test_reread_state_variables.sol#L20
- solidity/tmp/test_reread_state_variables.sol#L21
- solidity/tmp/test_reread_state_variables.sol#L22
- solidity/tmp/test_reread_state_variables.sol#L23
- solidity/tmp/test_reread_state_variables.sol#L28
- solidity/tmp/test_reread_state_variables.sol#L29
- solidity/tmp/test_reread_state_variables.sol#L30

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `7` instances of this issue:**

- [RereadStateVariables.bad(uint256).a](solidity/tmp/test_reread_state_variables.sol#L9) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L11)

- [RereadStateVariables.bad(uint256).b](solidity/tmp/test_reread_state_variables.sol#L10) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L11)

- [RereadStateVariables.notBad(uint256).x](solidity/tmp/test_reread_state_variables.sol#L19) lacks an upper limit check on :
	- [stateUint256 = x + 1](solidity/tmp/test_reread_state_variables.sol#L21)

- [RereadStateVariables.notBad(uint256).a](solidity/tmp/test_reread_state_variables.sol#L20) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L23)

- [RereadStateVariables.notBad(uint256).b](solidity/tmp/test_reread_state_variables.sol#L22) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L23)

- [RereadStateVariables.good(uint256).a](solidity/tmp/test_reread_state_variables.sol#L28) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L30)

- [RereadStateVariables.good(uint256).b](solidity/tmp/test_reread_state_variables.sol#L29) lacks an upper limit check on :
	- [stateUint256 = a + b](solidity/tmp/test_reread_state_variables.sol#L30)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_reread_state_variables.sol#L9
- solidity/tmp/test_reread_state_variables.sol#L10
- solidity/tmp/test_reread_state_variables.sol#L19
- solidity/tmp/test_reread_state_variables.sol#L20
- solidity/tmp/test_reread_state_variables.sol#L22
- solidity/tmp/test_reread_state_variables.sol#L28
- solidity/tmp/test_reread_state_variables.sol#L29

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Events are missing sender information

### description

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There is `1` instance of this issue:**

- [StateEvent(stateUint256,a)](solidity/tmp/test_reread_state_variables.sol#L16) should add `msg.sender` to event.


### recommendation

Adding `msg.sender` to event.


### locations
- solidity/tmp/test_reread_state_variables.sol#L16

### severity
Low

### category
missing-sender-in-event

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `3` instances of this issue:**

- Setter function [RereadStateVariables.bad(uint256)](solidity/tmp/test_reread_state_variables.sol#L8-L12) does not emit an event

- Setter function [RereadStateVariables.notBad(uint256)](solidity/tmp/test_reread_state_variables.sol#L19-L24) does not emit an event

- Setter function [RereadStateVariables.good(uint256)](solidity/tmp/test_reread_state_variables.sol#L26-L31) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_reread_state_variables.sol#L8-L12
- solidity/tmp/test_reread_state_variables.sol#L19-L24
- solidity/tmp/test_reread_state_variables.sol#L26-L31

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

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `2` instances of this issue:**

- [RereadStateVariables.stateUint256](solidity/tmp/test_reread_state_variables.sol#L4) should be cached with local memory-based variable in [RereadStateVariables.bad2(uint256)](solidity/tmp/test_reread_state_variables.sol#L14-L17), It is called more than once:
	- [StateEvent(stateUint256,a)](solidity/tmp/test_reread_state_variables.sol#L16)
	- [a = stateUint256 + x](solidity/tmp/test_reread_state_variables.sol#L15)

- [RereadStateVariables.stateUint256](solidity/tmp/test_reread_state_variables.sol#L4) should be cached with local memory-based variable in [RereadStateVariables.bad(uint256)](solidity/tmp/test_reread_state_variables.sol#L8-L12), It is called more than once:
	- [b = stateUint256 + x](solidity/tmp/test_reread_state_variables.sol#L10)
	- [a = stateUint256 + 1](solidity/tmp/test_reread_state_variables.sol#L9)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_reread_state_variables.sol#L4
- solidity/tmp/test_reread_state_variables.sol#L4

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There is `1` instance of this issue:**

- The following variables should be indexed in [RereadStateVariables.StateEvent(uint256,uint256)](solidity/tmp/test_reread_state_variables.sol#L6):

	- [state](solidity/tmp/test_reread_state_variables.sol#L6)

	- [a](solidity/tmp/test_reread_state_variables.sol#L6)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_reread_state_variables.sol#L6

### severity
Optimization

### category
unindexed-event

### confidence
High
