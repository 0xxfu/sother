## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-1] | Empty blocks should be removed or emit something | 12 |
| [G-2] | Public function that could be declared external | 4 |
| [G-3] | Use `calldata` instead of `memory` for function parameters | 4 |



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

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `2` instances of this issue:**

- Struct `Test.testStruct` (solidity/test_external_function.sol#L5-L8) is not in CapWords

- Function `ContractWithFunctionNotCalled.my_func()` (solidity/test_external_function.sol#L35-L37) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_external_function.sol#L5-L8
- solidity/test_external_function.sol#L35-L37

### severity:
Informational

### category:
naming-convention

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description:
Functions that are not sued.

**There is `1` instance of this issue:**

- `ContractWithFunctionNotCalled.my_func()` (solidity/test_external_function.sol#L35-L37) is never used and should be removed


### recommendation:
Remove unused functions.

### locations:
- solidity/test_external_function.sol#L35-L37

### severity:
Optimization

### category:
dead-code

## [Optimization] Empty blocks should be removed or emit something

### description:

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `12` instances of this issue:**

- `Test.good(bytes)` (solidity/test_external_function.sol#L10) should removed or do something

- `Test.good2()` (solidity/test_external_function.sol#L11) should removed or do something

- `Test.good3(uint256,uint256)` (solidity/test_external_function.sol#L12) should removed or do something

- `Test.good4(uint256[] ,string)` (solidity/test_external_function.sol#L13) should removed or do something

- `Test.good5(Test.testStruct)` (solidity/test_external_function.sol#L14) should removed or do something

- `Test.bad(bytes)` (solidity/test_external_function.sol#L15) should removed or do something

- `Test.bad2(uint256[] )` (solidity/test_external_function.sol#L16) should removed or do something

- `Test.bad3(Test.testStruct)` (solidity/test_external_function.sol#L17) should removed or do something

- `Test.bad4(string)` (solidity/test_external_function.sol#L18) should removed or do something

- `ContractWithFunctionNotCalled.funcNotCalled3()` (solidity/test_external_function.sol#L23-L25) should removed or do something

- `ContractWithFunctionNotCalled.funcNotCalled2()` (solidity/test_external_function.sol#L27-L29) should removed or do something

- `ContractWithFunctionNotCalled.funcNotCalled()` (solidity/test_external_function.sol#L31-L33) should removed or do something


### recommendation:

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations:
- solidity/test_external_function.sol#L10
- solidity/test_external_function.sol#L11
- solidity/test_external_function.sol#L12
- solidity/test_external_function.sol#L13
- solidity/test_external_function.sol#L14
- solidity/test_external_function.sol#L15
- solidity/test_external_function.sol#L16
- solidity/test_external_function.sol#L17
- solidity/test_external_function.sol#L18
- solidity/test_external_function.sol#L23-L25
- solidity/test_external_function.sol#L27-L29
- solidity/test_external_function.sol#L31-L33

### severity:
Optimization

### category:
empty-block

## [Optimization] Public function that could be declared external

### description:
`public` functions that are never called by the contract should be declared `external`, and its immutable parameters should be located in `calldata` to save gas.

**There are `4` instances of this issue:**

- bad(bytes) should be declared external:
	- `Test.bad(bytes)` (solidity/test_external_function.sol#L15)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad2(uint256[] ) should be declared external:
	- `Test.bad2(uint256[] )` (solidity/test_external_function.sol#L16)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad3(Test.testStruct) should be declared external:
	- `Test.bad3(Test.testStruct)` (solidity/test_external_function.sol#L17)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad4(string) should be declared external:
	- `Test.bad4(string)` (solidity/test_external_function.sol#L18)
Moreover, the following function parameters should change its data location:
x location should be calldata


### recommendation:
Use the `external` attribute for functions never called from the contract, and change the location of immutable parameters to `calldata` to save gas.

### locations:
- solidity/test_external_function.sol#L15
- solidity/test_external_function.sol#L16
- solidity/test_external_function.sol#L17
- solidity/test_external_function.sol#L18

### severity:
Optimization

### category:
external-function

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `4` instances of this issue:**

- `Test.bad(bytes)` (solidity/test_external_function.sol#L15) read-only `memory` parameters below should be changed to `calldata` :
	- `Test.bad(bytes).x` (solidity/test_external_function.sol#L15)

- `Test.bad2(uint256[] )` (solidity/test_external_function.sol#L16) read-only `memory` parameters below should be changed to `calldata` :
	- `Test.bad2(uint256[] ).x` (solidity/test_external_function.sol#L16)

- `Test.bad3(Test.testStruct)` (solidity/test_external_function.sol#L17) read-only `memory` parameters below should be changed to `calldata` :
	- `Test.bad3(Test.testStruct).x` (solidity/test_external_function.sol#L17)

- `Test.bad4(string)` (solidity/test_external_function.sol#L18) read-only `memory` parameters below should be changed to `calldata` :
	- `Test.bad4(string).x` (solidity/test_external_function.sol#L18)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_external_function.sol#L15
- solidity/test_external_function.sol#L16
- solidity/test_external_function.sol#L17
- solidity/test_external_function.sol#L18

### severity:
Optimization

### category:
memory-in-parameters
