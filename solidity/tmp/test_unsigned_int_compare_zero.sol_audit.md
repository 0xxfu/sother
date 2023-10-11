## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 3 |
| [G-1] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 1 |
| [G-2] | `!= 0` is less gas than `> 0` for unsigned integers | 3 |



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

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `3` instances of this issue:**

- [require(bool,string)(a > 0,"err")](solidity/tmp/test_unsigned_int_compare_zero.sol#L9) should use custom error to save gas.

- [require(bool,string)(a > 0,"err")](solidity/tmp/test_unsigned_int_compare_zero.sol#L13) should use custom error to save gas.

- [require(bool,string)(a != 0,"err")](solidity/tmp/test_unsigned_int_compare_zero.sol#L23) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_unsigned_int_compare_zero.sol#L9
- solidity/tmp/test_unsigned_int_compare_zero.sol#L13
- solidity/tmp/test_unsigned_int_compare_zero.sol#L23

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There is `1` instance of this issue:**

- `uint32 `[UnsignedIntCompareZero.bad3(uint32).a](solidity/tmp/test_unsigned_int_compare_zero.sol#L12) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/test_unsigned_int_compare_zero.sol#L12

### severity
Optimization

### category
smaller-uint-int

### confidence
High

## [Optimization] `!= 0` is less gas than `> 0` for unsigned integers

### description

`!= 0` costs less gas compared to `> 0` for unsigned integers in require statements 
with the optimizer enabled (6 gas)

While it may seem that `> 0` is cheaper than `!=`, this is only true without the 
optimizer enabled and outside a require statement. 
If you enable the optimizer at 10k and you’re in a `require` statement, 
this will save gas.



**There are `3` instances of this issue:**

- [a > 0](solidity/tmp/test_unsigned_int_compare_zero.sol#L3) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(a > 0,"err")](solidity/tmp/test_unsigned_int_compare_zero.sol#L9) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(a > 0,"err")](solidity/tmp/test_unsigned_int_compare_zero.sol#L13) should use `!= 0` instead of `> 0` for unsigned integer comparison.


### recommendation

Use `!= 0` instead of `> 0` for unsigned integer comparison.


### locations
- solidity/tmp/test_unsigned_int_compare_zero.sol#L3
- solidity/tmp/test_unsigned_int_compare_zero.sol#L9
- solidity/tmp/test_unsigned_int_compare_zero.sol#L13

### severity
Optimization

### category
unsigned-int-compare-zero

### confidence
High
