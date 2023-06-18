## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Dead-code | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache the `<array>.length` for the loop condition | 3 |
| [G-1] | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}` | 2 |



## [Informational] Dead-code

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- [UncheckedInLoop.internalView(uint256[])](solidity/test_unchecked_in_loop.sol#L40-L49) is never used and should be removed

#### Exploit scenario

```solidity
contract Contract{
    function dead_code() internal() {}
}
```
`dead_code` is not used in the contract, and make the code's review more difficult.

### recommendation:
Remove unused functions.

### location:
- solidity/test_unchecked_in_loop.sol#L40-L49

### severity:
Informational

### category:
dead-code

## [Optimization] Cache the `<array>.length` for the loop condition

### description:

The overheads outlined below are _PER LOOP_, excluding the first loop
* storage arrays incur a Gwarmaccess (**100 gas**)
* memory arrays use `MLOAD` (**3 gas**)
* calldata arrays use `CALLDATALOAD` (**3 gas**)

Caching the length changes each of these to a `DUP<N>` (**3 gas**), and gets rid of the extra `DUP<N>` needed to store the stack offset.
More detail optimization see [this](https://gist.github.com/0xxfu/80fcbc39d2d38d85ae61b4b8838ef30b)


**There are `3` instances of this issue:**

- [j < ns.length](solidity/test_unchecked_in_loop.sol#L15) `<array>.length` should be cached.

- [i_scope_0 < ns.length](solidity/test_unchecked_in_loop.sol#L11) `<array>.length` should be cached.

- [i < ns.length](solidity/test_unchecked_in_loop.sol#L8) `<array>.length` should be cached.


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
- solidity/test_unchecked_in_loop.sol#L15
- solidity/test_unchecked_in_loop.sol#L11
- solidity/test_unchecked_in_loop.sol#L8

### severity:
Optimization

### category:
array-length-in-loop

## [Optimization] The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`

### description:

The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)


**There are `2` instances of this issue:**

- [++ i_scope_0](solidity/test_unchecked_in_loop.sol#L11) should be used `unchecked{++i}/unchecked{i++}`.

- [i ++](solidity/test_unchecked_in_loop.sol#L8) should be used `unchecked{++i}/unchecked{i++}`.


### recommendation:

Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.


### location:
- solidity/test_unchecked_in_loop.sol#L11
- solidity/test_unchecked_in_loop.sol#L8

### severity:
Optimization

### category:
unchecked-in-loop
