## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache the `<array>.length` for the loop condition | 2 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |



## [Optimization] Cache the `<array>.length` for the loop condition

### description:

The overheads outlined below are _PER LOOP_, excluding the first loop
* storage arrays incur a Gwarmaccess (**100 gas**)
* memory arrays use `MLOAD` (**3 gas**)
* calldata arrays use `CALLDATALOAD` (**3 gas**)

Caching the length changes each of these to a `DUP<N>` (**3 gas**), and gets rid of the extra `DUP<N>` needed to store the stack offset.
More detail optimization see [this](https://gist.github.com/0xxfu/80fcbc39d2d38d85ae61b4b8838ef30b)


**There are `2` instances of this issue:**

- [i < ns.length](solidity/test_array_length_in_loop.sol#L41) `<array>.length` should be cached.

- [i < ns.length](solidity/test_array_length_in_loop.sol#L8) `<array>.length` should be cached.


### recommendation:

Caching the `<array>.length` for the loop condition, for example:
```solidity
// gas save (-230)
function loopArray_cached(uint256[] calldata ns) public returns (uint256 sum) {
    uint256 length = ns.length;
    for(uint256 i = 0; i < length;) {
        sum += ns[i];
        unchecked {
            i++;
        }
    }
}
```


### location:
- solidity/test_array_length_in_loop.sol#L41
- solidity/test_array_length_in_loop.sol#L8

### severity:
Optimization

### category:
array-length-in-loop

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [LoopArrayLength.internalView(uint256[])](solidity/test_array_length_in_loop.sol#L39-L48) is never used and should be removed


### recommendation:
Remove unused functions.

### location:
- solidity/test_array_length_in_loop.sol#L39-L48

### severity:
Optimization

### category:
dead-code
