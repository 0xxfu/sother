## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 3 |
| [L-1] | Unsafe downcasting arithmetic operation | 1 |
| [L-2] | Missing zero address validation | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `assembly` to write address storage values | 1 |
| [G-1] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 1 |



## [Low] Setters should check the input value

### description:

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `3` instances of this issue:**

- [UncheckedSetters.bad(uint256).a](solidity/test_unchecked_setters.sol#L7) lacks an upper limit check on :
	- [x = a](solidity/test_unchecked_setters.sol#L8)

- [UncheckedSetters.bad3(uint256).a](solidity/test_unchecked_setters.sol#L15) lacks an upper limit check on :
	- [x = a](solidity/test_unchecked_setters.sol#L16)
	- [y = a](solidity/test_unchecked_setters.sol#L17)

- [UncheckedSetters.bad4(uint256).a](solidity/test_unchecked_setters.sol#L20) lacks an upper limit check on :
	- [z = uint8(a)](solidity/test_unchecked_setters.sol#L21)


### recommendation:

Add an upper limit check to the setters function.


### locations:
- solidity/test_unchecked_setters.sol#L7
- solidity/test_unchecked_setters.sol#L15
- solidity/test_unchecked_setters.sol#L20

### severity:
Low

### category:
unchecked-setters

## [Low] Unsafe downcasting arithmetic operation

### description:

Downcasting from uint256/int256 in Solidity does not revert on overflow.
When a type is downcast to a smaller type, the higher order bits are truncated, 
effectively applying a modulo to the original value. 
Without any other checks, this wrapping will lead to unexpected behavior and bugs.


**There is `1` instance of this issue:**

- [z = uint8(a)](solidity/test_unchecked_setters.sol#L21) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.

### recommendation:

Just use `uint256/int256`, or use [OpenZeppelin SafeCast lib](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#).


### locations:
- solidity/test_unchecked_setters.sol#L21

### severity:
Low

### category:
unsafe-downcast

## [Low] Missing zero address validation

### description:
Detect missing zero address validation.

**There is `1` instance of this issue:**

- [UncheckedSetters.bad2(address).newOwner](solidity/test_unchecked_setters.sol#L11) lacks a zero-check on :
		- [owner = newOwner](solidity/test_unchecked_setters.sol#L12)

#### Exploit scenario

```solidity
contract C {

  modifier onlyAdmin {
    if (msg.sender != owner) throw;
    _;
  }

  function updateOwner(address newOwner) onlyAdmin external {
    owner = newOwner;
  }
}
```
Bob calls `updateOwner` without specifying the `newOwner`, so Bob loses ownership of the contract.


### recommendation:
Check that the address is not zero.

### locations:
- solidity/test_unchecked_setters.sol#L11

### severity:
Low

### category:
missing-zero-check

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.20

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### locations:
- 

### severity:
Informational

### category:
solc-version

## [Optimization] Use `assembly` to write address storage values

### description:

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There is `1` instance of this issue:**

- [owner = newOwner](solidity/test_unchecked_setters.sol#L12) should use `assembly` update address to save gas.


### recommendation:

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations:
- solidity/test_unchecked_setters.sol#L12

### severity:
Optimization

### category:
assembly-update-address

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description:

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There is `1` instance of this issue:**

- `uint8 `[UncheckedSetters.z](solidity/test_unchecked_setters.sol#L4) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/test_unchecked_setters.sol#L4

### severity:
Optimization

### category:
smaller-uint-int
