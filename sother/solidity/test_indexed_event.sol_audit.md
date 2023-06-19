## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use indexed events for value types as they are less costly compared to non-indexed ones | 1 |



## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There is `1` instance of this issue:**

- The following variables should be indexed in [IndexedEventIntsEvent(uint256,uint256,uint256)](solidity/test_indexed_event.sol#L7):

	- [z](solidity/test_indexed_event.sol#L7)

	- [y](solidity/test_indexed_event.sol#L7)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### location:
- solidity/test_indexed_event.sol#L7

### severity:
Optimization

### category:
unindexed-event
