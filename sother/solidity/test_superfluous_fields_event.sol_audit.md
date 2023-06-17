## Summary 

### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Superfluous fields in event | 2 |



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
