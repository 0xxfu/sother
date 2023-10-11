## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Void function | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 2 |
| [N-2] | Unnecessary Public Function Modifier | 9 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 8 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-2] | Use `calldata` instead of `memory` for function parameters | 4 |
| [G-3] | Public function that could be declared external | 4 |
| [G-4] | Empty blocks should be removed or emit something | 12 |



## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There are `12` instances of this issue:**

- function:[Test.good(bytes)](solidity/tmp/test_external_function.sol#L10)is empty 

- function:[Test.good2()](solidity/tmp/test_external_function.sol#L11)is empty 

- function:[Test.good3(uint256,uint256)](solidity/tmp/test_external_function.sol#L12)is empty 

- function:[Test.good4(uint256[],string)](solidity/tmp/test_external_function.sol#L13)is empty 

- function:[Test.good5(Test.testStruct)](solidity/tmp/test_external_function.sol#L14)is empty 

- function:[Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15)is empty 

- function:[Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16)is empty 

- function:[Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17)is empty 

- function:[Test.bad4(string)](solidity/tmp/test_external_function.sol#L18)is empty 

- function:[ContractWithFunctionNotCalled.funcNotCalled3()](solidity/tmp/test_external_function.sol#L23-L25)is empty 

- function:[ContractWithFunctionNotCalled.funcNotCalled2()](solidity/tmp/test_external_function.sol#L27-L29)is empty 

- function:[ContractWithFunctionNotCalled.funcNotCalled()](solidity/tmp/test_external_function.sol#L31-L33)is empty 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Implement the function

### locations
- solidity/tmp/test_external_function.sol#L10
- solidity/tmp/test_external_function.sol#L11
- solidity/tmp/test_external_function.sol#L12
- solidity/tmp/test_external_function.sol#L13
- solidity/tmp/test_external_function.sol#L14
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18
- solidity/tmp/test_external_function.sol#L23-L25
- solidity/tmp/test_external_function.sol#L27-L29
- solidity/tmp/test_external_function.sol#L31-L33

### severity
Medium

### category
void-function

### confidence
High

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

**There are `2` instances of this issue:**

- Struct [Test.testStruct](solidity/tmp/test_external_function.sol#L5-L8) is not in CapWords

- Function [ContractWithFunctionNotCalled.my_func()](solidity/tmp/test_external_function.sol#L35-L37) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_external_function.sol#L5-L8
- solidity/tmp/test_external_function.sol#L35-L37

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `9` instances of this issue:**

- function:[Test.good2()](solidity/tmp/test_external_function.sol#L11)is public and can be replaced with external 

- function:[Test.good3(uint256,uint256)](solidity/tmp/test_external_function.sol#L12)is public and can be replaced with external 

- function:[Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15)is public and can be replaced with external 

- function:[Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16)is public and can be replaced with external 

- function:[Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17)is public and can be replaced with external 

- function:[Test.bad4(string)](solidity/tmp/test_external_function.sol#L18)is public and can be replaced with external 

- function:[ContractWithFunctionNotCalled.funcNotCalled3()](solidity/tmp/test_external_function.sol#L23-L25)is public and can be replaced with external 

- function:[ContractWithFunctionNotCalled.funcNotCalled2()](solidity/tmp/test_external_function.sol#L27-L29)is public and can be replaced with external 

- function:[ContractWithFunctionNotCalled.funcNotCalled()](solidity/tmp/test_external_function.sol#L31-L33)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/test_external_function.sol#L11
- solidity/tmp/test_external_function.sol#L12
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18
- solidity/tmp/test_external_function.sol#L23-L25
- solidity/tmp/test_external_function.sol#L27-L29
- solidity/tmp/test_external_function.sol#L31-L33

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `8` instances of this issue:**

- The param variables in [Test.good(bytes)](solidity/tmp/test_external_function.sol#L10) are unused.
	- [Test.good(bytes).x](solidity/tmp/test_external_function.sol#L10)

- The param variables in [Test.good3(uint256,uint256)](solidity/tmp/test_external_function.sol#L12) are unused.
	- [Test.good3(uint256,uint256).x](solidity/tmp/test_external_function.sol#L12)
	- [Test.good3(uint256,uint256).y](solidity/tmp/test_external_function.sol#L12)

- The param variables in [Test.good4(uint256[],string)](solidity/tmp/test_external_function.sol#L13) are unused.
	- [Test.good4(uint256[],string).x](solidity/tmp/test_external_function.sol#L13)
	- [Test.good4(uint256[],string).y](solidity/tmp/test_external_function.sol#L13)

- The param variables in [Test.good5(Test.testStruct)](solidity/tmp/test_external_function.sol#L14) are unused.
	- [Test.good5(Test.testStruct).x](solidity/tmp/test_external_function.sol#L14)

- The param variables in [Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15) are unused.
	- [Test.bad(bytes).x](solidity/tmp/test_external_function.sol#L15)

- The param variables in [Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16) are unused.
	- [Test.bad2(uint256[]).x](solidity/tmp/test_external_function.sol#L16)

- The param variables in [Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17) are unused.
	- [Test.bad3(Test.testStruct).x](solidity/tmp/test_external_function.sol#L17)

- The param variables in [Test.bad4(string)](solidity/tmp/test_external_function.sol#L18) are unused.
	- [Test.bad4(string).x](solidity/tmp/test_external_function.sol#L18)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_external_function.sol#L10
- solidity/tmp/test_external_function.sol#L12
- solidity/tmp/test_external_function.sol#L13
- solidity/tmp/test_external_function.sol#L14
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [ContractWithFunctionNotCalled.my_func()](solidity/tmp/test_external_function.sol#L35-L37) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/test_external_function.sol#L35-L37

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `4` instances of this issue:**

- [Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15) read-only `memory` parameters below should be changed to `calldata` :
	- [Test.bad(bytes).x](solidity/tmp/test_external_function.sol#L15)

- [Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16) read-only `memory` parameters below should be changed to `calldata` :
	- [Test.bad2(uint256[]).x](solidity/tmp/test_external_function.sol#L16)

- [Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17) read-only `memory` parameters below should be changed to `calldata` :
	- [Test.bad3(Test.testStruct).x](solidity/tmp/test_external_function.sol#L17)

- [Test.bad4(string)](solidity/tmp/test_external_function.sol#L18) read-only `memory` parameters below should be changed to `calldata` :
	- [Test.bad4(string).x](solidity/tmp/test_external_function.sol#L18)


### recommendation
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18

### severity
Optimization

### category
memory-in-parameters

### confidence
High

## [Optimization] Public function that could be declared external

### description
`public` functions that are never called by the contract should be declared `external`, and its immutable parameters should be located in `calldata` to save gas.

**There are `4` instances of this issue:**

- bad(bytes) should be declared external:
	- [Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad2(uint256[]) should be declared external:
	- [Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad3(Test.testStruct) should be declared external:
	- [Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17)
Moreover, the following function parameters should change its data location:
x location should be calldata

- bad4(string) should be declared external:
	- [Test.bad4(string)](solidity/tmp/test_external_function.sol#L18)
Moreover, the following function parameters should change its data location:
x location should be calldata


### recommendation
Use the `external` attribute for functions never called from the contract, and change the location of immutable parameters to `calldata` to save gas.

### locations
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18

### severity
Optimization

### category
external-function

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `12` instances of this issue:**

- [Test.good(bytes)](solidity/tmp/test_external_function.sol#L10) should removed or do something

- [Test.good2()](solidity/tmp/test_external_function.sol#L11) should removed or do something

- [Test.good3(uint256,uint256)](solidity/tmp/test_external_function.sol#L12) should removed or do something

- [Test.good4(uint256[],string)](solidity/tmp/test_external_function.sol#L13) should removed or do something

- [Test.good5(Test.testStruct)](solidity/tmp/test_external_function.sol#L14) should removed or do something

- [Test.bad(bytes)](solidity/tmp/test_external_function.sol#L15) should removed or do something

- [Test.bad2(uint256[])](solidity/tmp/test_external_function.sol#L16) should removed or do something

- [Test.bad3(Test.testStruct)](solidity/tmp/test_external_function.sol#L17) should removed or do something

- [Test.bad4(string)](solidity/tmp/test_external_function.sol#L18) should removed or do something

- [ContractWithFunctionNotCalled.funcNotCalled3()](solidity/tmp/test_external_function.sol#L23-L25) should removed or do something

- [ContractWithFunctionNotCalled.funcNotCalled2()](solidity/tmp/test_external_function.sol#L27-L29) should removed or do something

- [ContractWithFunctionNotCalled.funcNotCalled()](solidity/tmp/test_external_function.sol#L31-L33) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_external_function.sol#L10
- solidity/tmp/test_external_function.sol#L11
- solidity/tmp/test_external_function.sol#L12
- solidity/tmp/test_external_function.sol#L13
- solidity/tmp/test_external_function.sol#L14
- solidity/tmp/test_external_function.sol#L15
- solidity/tmp/test_external_function.sol#L16
- solidity/tmp/test_external_function.sol#L17
- solidity/tmp/test_external_function.sol#L18
- solidity/tmp/test_external_function.sol#L23-L25
- solidity/tmp/test_external_function.sol#L27-L29
- solidity/tmp/test_external_function.sol#L31-L33

### severity
Optimization

### category
empty-block

### confidence
High
