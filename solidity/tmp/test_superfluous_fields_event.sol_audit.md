## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 4 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Events are missing sender information | 6 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Superfluous fields in event | 2 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 3 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `4` instances of this issue:**

- bad(uint256) has possible integer overflow/underflow:
	- [abc = abc + 1](solidity/tmp/test_superfluous_fields_event.sol#L9)

- good(uint256) has possible integer overflow/underflow:
	- [abc = abc + 1](solidity/tmp/test_superfluous_fields_event.sol#L16)

- good(uint256) has possible integer overflow/underflow:
	- [BlockNumberEvent(abc + 1)](solidity/tmp/test_superfluous_fields_event.sol#L18)

- good(uint256) has possible integer overflow/underflow:
	- [BlockTimestampEvent(abc + 1)](solidity/tmp/test_superfluous_fields_event.sol#L19)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_superfluous_fields_event.sol#L9
- solidity/tmp/test_superfluous_fields_event.sol#L16
- solidity/tmp/test_superfluous_fields_event.sol#L18
- solidity/tmp/test_superfluous_fields_event.sol#L19

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Events are missing sender information

### description

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There are `6` instances of this issue:**

- [GoodEvent(abc)](solidity/tmp/test_superfluous_fields_event.sol#L10) should add `msg.sender` to event.

- [BlockNumberEvent(block.number)](solidity/tmp/test_superfluous_fields_event.sol#L11) should add `msg.sender` to event.

- [BlockTimestampEvent(block.timestamp)](solidity/tmp/test_superfluous_fields_event.sol#L12) should add `msg.sender` to event.

- [GoodEvent(abc)](solidity/tmp/test_superfluous_fields_event.sol#L17) should add `msg.sender` to event.

- [BlockNumberEvent(abc + 1)](solidity/tmp/test_superfluous_fields_event.sol#L18) should add `msg.sender` to event.

- [BlockTimestampEvent(abc + 1)](solidity/tmp/test_superfluous_fields_event.sol#L19) should add `msg.sender` to event.


### recommendation

Adding `msg.sender` to event.


### locations
- solidity/tmp/test_superfluous_fields_event.sol#L10
- solidity/tmp/test_superfluous_fields_event.sol#L11
- solidity/tmp/test_superfluous_fields_event.sol#L12
- solidity/tmp/test_superfluous_fields_event.sol#L17
- solidity/tmp/test_superfluous_fields_event.sol#L18
- solidity/tmp/test_superfluous_fields_event.sol#L19

### severity
Low

### category
missing-sender-in-event

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

## [Optimization] Superfluous fields in event

### description

`block.timestamp` and `block.number` are added to event information by default so adding them manually wastes gas


**There are `2` instances of this issue:**

- [BlockNumberEvent(block.number)](solidity/tmp/test_superfluous_fields_event.sol#L11) remove default fields(`block.timestamp` or `block.number`) in event to save gas.

- [BlockTimestampEvent(block.timestamp)](solidity/tmp/test_superfluous_fields_event.sol#L12) remove default fields(`block.timestamp` or `block.number`) in event to save gas.


### recommendation

Remove default fields(`block.timestamp` or `block.number`) in event.


### locations
- solidity/tmp/test_superfluous_fields_event.sol#L11
- solidity/tmp/test_superfluous_fields_event.sol#L12

### severity
Optimization

### category
superfluous-fields-event

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `3` instances of this issue:**

- The following variables should be indexed in [SuperfluousFieldsEvent.BlockTimestampEvent(uint256)](solidity/tmp/test_superfluous_fields_event.sol#L4):

	- [blockTimestamp](solidity/tmp/test_superfluous_fields_event.sol#L4)

- The following variables should be indexed in [SuperfluousFieldsEvent.BlockNumberEvent(uint256)](solidity/tmp/test_superfluous_fields_event.sol#L5):

	- [blockNumber](solidity/tmp/test_superfluous_fields_event.sol#L5)

- The following variables should be indexed in [SuperfluousFieldsEvent.GoodEvent(uint256)](solidity/tmp/test_superfluous_fields_event.sol#L6):

	- [xyz](solidity/tmp/test_superfluous_fields_event.sol#L6)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_superfluous_fields_event.sol#L4
- solidity/tmp/test_superfluous_fields_event.sol#L5
- solidity/tmp/test_superfluous_fields_event.sol#L6

### severity
Optimization

### category
unindexed-event

### confidence
High
