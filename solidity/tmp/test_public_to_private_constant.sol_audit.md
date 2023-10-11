## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using `private` rather than `public` for constants, saves gas | 3 |
| [G-1] | It costs more gas to initialize state variables to zero than to let the default of zero be applied | 2 |
| [G-2] | Use `delete` to Clear Variables | 2 |



## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [PublicToPrivateConstant.slitherConstructorConstantVariables()](solidity/tmp/test_public_to_private_constant.sol#L3-L10) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_public_to_private_constant.sol#L3-L10

### severity
Low

### category
pess-event-setter

### confidence
Medium

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

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `3` instances of this issue:**

- Constant [PublicToPrivateConstant.priUint256](solidity/tmp/test_public_to_private_constant.sol#L7) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [PublicToPrivateConstant.priAddress](solidity/tmp/test_public_to_private_constant.sol#L8) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [PublicToPrivateConstant.priBytes](solidity/tmp/test_public_to_private_constant.sol#L9) is not in UPPER_CASE_WITH_UNDERSCORES


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_public_to_private_constant.sol#L7
- solidity/tmp/test_public_to_private_constant.sol#L8
- solidity/tmp/test_public_to_private_constant.sol#L9

### severity
Informational

### category
naming-convention

### confidence
High

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There are `3` instances of this issue:**

- [PublicToPrivateConstant.pUint256](solidity/tmp/test_public_to_private_constant.sol#L4) should be used `private` visibility to save gas.

- [PublicToPrivateConstant.pAddress](solidity/tmp/test_public_to_private_constant.sol#L5) should be used `private` visibility to save gas.

- [PublicToPrivateConstant.pBytes](solidity/tmp/test_public_to_private_constant.sol#L6) should be used `private` visibility to save gas.


### recommendation

Using `private` replace `public` with constant.


### locations
- solidity/tmp/test_public_to_private_constant.sol#L4
- solidity/tmp/test_public_to_private_constant.sol#L5
- solidity/tmp/test_public_to_private_constant.sol#L6

### severity
Optimization

### category
public-to-private-constant

### confidence
High

## [Optimization] It costs more gas to initialize state variables to zero than to let the default of zero be applied

### description

If a state variable is not set/initialized, 
it is assumed to have the default value (0 for uint, false for bool, address(0) for address…). 
Explicitly initializing it with its default value is an anti-pattern and wastes gas.

More detail see [this.](https://gist.github.com/0xxfu/b111e822aa4ee2e0f6bbaf2658818520)



**There are `2` instances of this issue:**

- [PublicToPrivateConstant.pAddress](solidity/tmp/test_public_to_private_constant.sol#L5) should not overwrite the default.

- [PublicToPrivateConstant.priAddress](solidity/tmp/test_public_to_private_constant.sol#L8) should not overwrite the default.


### recommendation

Do not initialize state variables to zero.


### locations
- solidity/tmp/test_public_to_private_constant.sol#L5
- solidity/tmp/test_public_to_private_constant.sol#L8

### severity
Optimization

### category
zero-initialized-state-variable

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There are `2` instances of this issue:**

- Should use `delete` statement instead of [pAddress = address(0)](solidity/tmp/test_public_to_private_constant.sol#L5)

- Should use `delete` statement instead of [priAddress = address(0)](solidity/tmp/test_public_to_private_constant.sol#L8)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/test_public_to_private_constant.sol#L5
- solidity/tmp/test_public_to_private_constant.sol#L8

### severity
Optimization

### category
use-delete-statement

### confidence
High
