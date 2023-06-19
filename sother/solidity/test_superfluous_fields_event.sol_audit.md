## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Superfluous fields in event | 2 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 3 |



## [Optimization] Superfluous fields in event

### description:

`block.timestamp` and `block.number` are added to event information by default so adding them manually wastes gas


**There are `2` instances of this issue:**

- [BlockNumberEvent(block.number)](solidity/test_superfluous_fields_event.sol#L11) remove default fields(`block.timestamp` or `block.number`) in event to save gas.

- [BlockTimestampEvent(block.timestamp)](solidity/test_superfluous_fields_event.sol#L12) remove default fields(`block.timestamp` or `block.number`) in event to save gas.


### recommendation:

Remove default fields(`block.timestamp` or `block.number`) in event.


### location:
- solidity/test_superfluous_fields_event.sol#L11
- solidity/test_superfluous_fields_event.sol#L12

### severity:
Optimization

### category:
superfluous-fields-event

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `3` instances of this issue:**

- The following variables should be indexed in [SuperfluousFieldsEvent.BlockTimestampEvent(uint256)](solidity/test_superfluous_fields_event.sol#L4):

	- [blockTimestamp](solidity/test_superfluous_fields_event.sol#L4)

- The following variables should be indexed in [SuperfluousFieldsEvent.BlockNumberEvent(uint256)](solidity/test_superfluous_fields_event.sol#L5):

	- [blockNumber](solidity/test_superfluous_fields_event.sol#L5)

- The following variables should be indexed in [SuperfluousFieldsEvent.GoodEvent(uint256)](solidity/test_superfluous_fields_event.sol#L6):

	- [xyz](solidity/test_superfluous_fields_event.sol#L6)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### location:
- solidity/test_superfluous_fields_event.sol#L4
- solidity/test_superfluous_fields_event.sol#L5
- solidity/test_superfluous_fields_event.sol#L6

### severity:
Optimization

### category:
unindexed-event
