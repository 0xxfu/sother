## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 3 |
| [G-1] | Remove or replace unused state variables | 3 |
| [G-2] | It costs more gas to initialize state variables to zero than to let the default of zero be applied | 3 |



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

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description:

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `3` instances of this issue:**

- `uint32 ``SetVsDefault1.bad2` (solidity/zero_initialized_state_variable.sol#L3) should be used `uint256/int256`.

- `uint32 ``SetVsDefault1.notBad2` (solidity/zero_initialized_state_variable.sol#L5) should be used `uint256/int256`.

- `uint32 ``SetVsDefault1.good2` (solidity/zero_initialized_state_variable.sol#L9) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/zero_initialized_state_variable.sol#L3
- solidity/zero_initialized_state_variable.sol#L5
- solidity/zero_initialized_state_variable.sol#L9

### severity:
Optimization

### category:
smaller-uint-int

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There are `3` instances of this issue:**

- `SetVsDefault1.good` (solidity/zero_initialized_state_variable.sol#L8) is never used.
- `SetVsDefault1.good2` (solidity/zero_initialized_state_variable.sol#L9) is never used.
- `SetVsDefault1.good3` (solidity/zero_initialized_state_variable.sol#L10) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/zero_initialized_state_variable.sol#L8
- solidity/zero_initialized_state_variable.sol#L9
- solidity/zero_initialized_state_variable.sol#L10

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] It costs more gas to initialize state variables to zero than to let the default of zero be applied

### description:

If a state variable is not set/initialized, 
it is assumed to have the default value (0 for uint, false for bool, address(0) for address…). 
Explicitly initializing it with its default value is an anti-pattern and wastes gas.

More detail see [this.](https://gist.github.com/0xxfu/b111e822aa4ee2e0f6bbaf2658818520)



**There are `3` instances of this issue:**

- `SetVsDefault1.bad` (solidity/zero_initialized_state_variable.sol#L2) should not overwrite the default.

- `SetVsDefault1.bad2` (solidity/zero_initialized_state_variable.sol#L3) should not overwrite the default.

- `SetVsDefault1.bad3` (solidity/zero_initialized_state_variable.sol#L6) should not overwrite the default.


### recommendation:

Do not initialize state variables to zero.


### locations:
- solidity/zero_initialized_state_variable.sol#L2
- solidity/zero_initialized_state_variable.sol#L3
- solidity/zero_initialized_state_variable.sol#L6

### severity:
Optimization

### category:
zero-initialized-state-variable
