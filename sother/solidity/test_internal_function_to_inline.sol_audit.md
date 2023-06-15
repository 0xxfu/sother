## Summary 

### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 3 |



## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description:
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There is `1` instance of this issue:**

- should use arithmetic operator `=` replace `+=` in [state1 += internalFunction4(abc)](solidity/test_internal_function_to_inline.sol#L20)

### recommendation:
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### location:
- solidity/test_internal_function_to_inline.sol#L20

### severity:
Optimization

### category:
assignment-left-operation

## [Optimization] `internal` functions only called once can be inlined to save gas

### description:

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There are `3` instances of this issue:**

- [InternalFunctionToInline.internalFunction4(uint256)](solidity/test_internal_function_to_inline.sol#L35-L37) could be inlined to save gas
- [InternalFunctionToInline.internalFunction3(uint256)](solidity/test_internal_function_to_inline.sol#L31-L33) could be inlined to save gas
- [InternalFunctionToInline.internalFunction(uint256)](solidity/test_internal_function_to_inline.sol#L23-L25) could be inlined to save gas

### recommendation:
Using inlining replace `internal` function which only called once

### location:
- solidity/test_internal_function_to_inline.sol#L35-L37
- solidity/test_internal_function_to_inline.sol#L31-L33
- solidity/test_internal_function_to_inline.sol#L23-L25

### severity:
Optimization

### category:
internal-function-to-inline
