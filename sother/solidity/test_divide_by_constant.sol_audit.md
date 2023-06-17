## Summary 

### Medium Risk Issues

| |Issue|Instances|
|---|:---|:---:|
| [M-0] | Divide before multiply | 1 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 2 |



## [Medium] Divide before multiply

### description:
Solidity's integer division truncates. Thus, performing division before multiplication can lead to precision loss.

**There is `1` instance of this issue:**

- [DivVsShr.bad(uint256)](solidity/test_divide_by_constant.sol#L16-L26) performs a multiplication on the result of a division:
	- [result = a / result](solidity/test_divide_by_constant.sol#L22)
	- [result = result * 2](solidity/test_divide_by_constant.sol#L23)

#### Exploit scenario

```solidity
contract A {
	function f(uint n) public {
        coins = (oldSupply / n) * interest;
    }
}
```
If `n` is greater than `oldSupply`, `coins` will be zero. For example, with `oldSupply = 5; n = 10, interest = 2`, coins will be zero.  
If `(oldSupply * interest / n)` was used, `coins` would have been `1`.   
In general, it's usually a good idea to re-arrange arithmetic to perform multiplication before division, unless the limit of a smaller type makes this dangerous.

### recommendation:
Consider ordering multiplication before division.

### location:
- solidity/test_divide_by_constant.sol#L16-L26

### severity:
Medium

### category:
divide-before-multiply

## [Optimization] Using `x >> constant(uint)` with the right shift operator is a more gas-efficient

### description:

`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) due to `JUMP`s to and from a compiler utility function that introduces checks which can be avoided by using `unchecked {}` around the division by two



**There are `2` instances of this issue:**

- [a = result / 10](solidity/test_divide_by_constant.sol#L21) should use bit shifting `>>` operator to save gas.

- [result = x / 2](solidity/test_divide_by_constant.sol#L19) should use bit shifting `>>` operator to save gas.


### recommendation:

Using bit shifting (`>>` operator) replace division divided by constant.


### location:
- solidity/test_divide_by_constant.sol#L21
- solidity/test_divide_by_constant.sol#L19

### severity:
Optimization

### category:
divide-by-constant
