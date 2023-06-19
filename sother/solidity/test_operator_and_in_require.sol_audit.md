## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Splitting `&&` in `require()` statements to saves gas | 1 |
| [G-1] | use custom errors instead of revert strings | 3 |



## [Optimization] Splitting `&&` in `require()` statements to saves gas

### description:

Instead of using the `&&` operator in a single require statement to check multiple conditions,using multiple require statements with 1 condition per require statement will save 3 GAS per `&&`

More detail see [this.](https://gist.github.com/0xxfu/478b64036c4cdc45d3d278cd5bd8eb9b)


**There is `1` instance of this issue:**

- [require(bool,string)(a >= 100 && a <= 1000,err)](solidity/test_operator_and_in_require.sol#L18) contain `&&` operator should be split into multiple `require()` statements.


### recommendation:

Splitting `&&` operator in `require()` into multiple `require()` statements.

```
// Before
require(result >= a && result <= b);

// After
require(result >= a);
require(result <= b);
```


### location:
- solidity/test_operator_and_in_require.sol#L18

### severity:
Optimization

### category:
operator-and-in-require

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `3` instances of this issue:**

- [require(bool,string)(a >= 100,err)](solidity/test_operator_and_in_require.sol#L8) should use custom error to save gas.

- [require(bool,string)(a >= 100 && a <= 1000,err)](solidity/test_operator_and_in_require.sol#L18) should use custom error to save gas.

- [require(bool,string)(a <= 1000,err)](solidity/test_operator_and_in_require.sol#L10) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### location:
- solidity/test_operator_and_in_require.sol#L8
- solidity/test_operator_and_in_require.sol#L18
- solidity/test_operator_and_in_require.sol#L10

### severity:
Optimization

### category:
use-custom-error
