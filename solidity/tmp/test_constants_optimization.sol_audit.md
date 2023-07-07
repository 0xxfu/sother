## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 7 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Do not calculate constants | 4 |
| [G-1] | Public function that could be declared external | 1 |
| [G-2] | Pre-calculate the results into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime.
 | 2 |
| [G-3] | Instead of calculating a state variable with `keccak256()`/`abi.encode**()` every time the contract is made pre calculate them before and only give the result to a constant | 2 |
| [G-4] | Use `calldata` instead of `memory` for function parameters | 2 |
| [G-5] | Using `private` rather than `public` for constants, saves gas | 2 |
| [G-6] | `Bytes` constants are more efficient than `string` constants | 1 |
| [G-7] | Using custom errors replace `require` or `assert` | 2 |
| [G-8] | State variables that could be declared constant | 1 |



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

**There are `7` instances of this issue:**

- Constant `CalculateConstants.bad` (solidity/test_constants_optimization.sol#L7) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad2` (solidity/test_constants_optimization.sol#L8) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad3` (solidity/test_constants_optimization.sol#L9) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad4` (solidity/test_constants_optimization.sol#L10) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.badKeccak` (solidity/test_constants_optimization.sol#L11) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.badEncode` (solidity/test_constants_optimization.sol#L12) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.notBad2` (solidity/test_constants_optimization.sol#L13) is not in UPPER_CASE_WITH_UNDERSCORES


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_constants_optimization.sol#L7
- solidity/test_constants_optimization.sol#L8
- solidity/test_constants_optimization.sol#L9
- solidity/test_constants_optimization.sol#L10
- solidity/test_constants_optimization.sol#L11
- solidity/test_constants_optimization.sol#L12
- solidity/test_constants_optimization.sol#L13

### severity:
Informational

### category:
naming-convention

## [Optimization] Do not calculate constants

### description:

Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.

See: [ethereum/solidity#9232](https://github.com/ethereum/solidity/issues/9232):
> each usage of a "constant" costs ~100gas more on each access (it is still a little better than storing the result in storage, but not much..)

> since these are not real constants, they can't be referenced from a real constant environment (e.g. from assembly, or from another library )



**There are `4` instances of this issue:**

- `CalculateConstants.bad` (solidity/test_constants_optimization.sol#L7) should use hardcode instead of calculation.

- `CalculateConstants.bad2` (solidity/test_constants_optimization.sol#L8) should use hardcode instead of calculation.

- `CalculateConstants.bad3` (solidity/test_constants_optimization.sol#L9) should use hardcode instead of calculation.

- `CalculateConstants.bad4` (solidity/test_constants_optimization.sol#L10) should use hardcode instead of calculation.


### recommendation:

Pre-calculate the results(hardcode) instead of calculation in runtime.


### locations:
- solidity/test_constants_optimization.sol#L7
- solidity/test_constants_optimization.sol#L8
- solidity/test_constants_optimization.sol#L9
- solidity/test_constants_optimization.sol#L10

### severity:
Optimization

### category:
calculate-constants

## [Optimization] Public function that could be declared external

### description:
`public` functions that are never called by the contract should be declared `external`, and its immutable parameters should be located in `calldata` to save gas.

**There is `1` instance of this issue:**

- notBad(string) should be declared external:
	- `ContstantInKeccak.notBad(string)` (solidity/test_constants_optimization.sol#L39-L41)
Moreover, the following function parameters should change its data location:
a location should be calldata


### recommendation:
Use the `external` attribute for functions never called from the contract, and change the location of immutable parameters to `calldata` to save gas.

### locations:
- solidity/test_constants_optimization.sol#L39-L41

### severity:
Optimization

### category:
external-function

## [Optimization] Pre-calculate the results into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime.


### description:

It should be saved to an `constant` variable, and the `constant` used instead. 
If the hash is being used as a part of a function selector, 
the cast to bytes4 should only be Pre-calculated


**There are `2` instances of this issue:**

- `abi.encode(a)` (solidity/test_constants_optimization.sol#L28) should use pre-calculate results instead of calculation in runtime.

- `require(bool,string)(checkRole.checkOnlyRole(keccak256(bytes)(TIMELOCK),msg.sender),not authorized)` (solidity/test_constants_optimization.sol#L32-L35) should use pre-calculate results instead of calculation in runtime.


### recommendation:

Pre-calculate the results(hardcode) into `constant` instead of calculate `keccak256`/`abi.encode**` in runtime.


### locations:
- solidity/test_constants_optimization.sol#L28
- solidity/test_constants_optimization.sol#L32-L35

### severity:
Optimization

### category:
keccak-constant-in-function

## [Optimization] Instead of calculating a state variable with `keccak256()`/`abi.encode**()` every time the contract is made pre calculate them before and only give the result to a constant

### description:

Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.

See: [ethereum/solidity#9232](https://github.com/ethereum/solidity/issues/9232):
> each usage of a "constant" costs ~100gas more on each access (it is still a little better than storing the result in storage, but not much..)

> since these are not real constants, they can't be referenced from a real constant environment (e.g. from assembly, or from another library )



**There are `2` instances of this issue:**

- `CalculateConstants.badKeccak` (solidity/test_constants_optimization.sol#L11) should use pre-calculate results instead of calculation in runtime.

- `CalculateConstants.badEncode` (solidity/test_constants_optimization.sol#L12) should use pre-calculate results instead of calculation in runtime.


### recommendation:

Pre-calculate the results(hardcode) instead of calculate `keccak256`/`abi.encode**` in runtime.


### locations:
- solidity/test_constants_optimization.sol#L11
- solidity/test_constants_optimization.sol#L12

### severity:
Optimization

### category:
keccak-constants

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `2` instances of this issue:**

- `ContstantInKeccak.notBad(string)` (solidity/test_constants_optimization.sol#L39-L41) read-only `memory` parameters below should be changed to `calldata` :
	- `ContstantInKeccak.notBad(string).a` (solidity/test_constants_optimization.sol#L39)

- `ContstantInKeccak.notBad2(bytes)` (solidity/test_constants_optimization.sol#L43-L49) read-only `memory` parameters below should be changed to `calldata` :
	- `ContstantInKeccak.notBad2(bytes).role` (solidity/test_constants_optimization.sol#L43)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_constants_optimization.sol#L39-L41
- solidity/test_constants_optimization.sol#L43-L49

### severity:
Optimization

### category:
memory-in-parameters

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description:

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There are `2` instances of this issue:**

- `BytesConstants.bad` (solidity/test_constants_optimization.sol#L2) should be used `private` visibility to save gas.

- `BytesConstants.notBad` (solidity/test_constants_optimization.sol#L3) should be used `private` visibility to save gas.


### recommendation:

Using `private` replace `public` with constant.


### locations:
- solidity/test_constants_optimization.sol#L2
- solidity/test_constants_optimization.sol#L3

### severity:
Optimization

### category:
public-to-private-constant

## [Optimization] `Bytes` constants are more efficient than `string` constants

### description:

From the [Solidity doc](https://docs.soliditylang.org/en/develop/types.html#arrays):
> If you can limit the length to a certain number of bytes, 
> always use one of the value types `bytes1` to `bytes32` because they are much cheaper.

[Why do Solidity examples use bytes32 type instead of string?](https://ethereum.stackexchange.com/questions/3795/why-do-solidity-examples-use-bytes32-type-instead-of-string)

`bytes32` uses less gas because it fits in a single word of the EVM, 
and `string` is a dynamically sized-type which has current limitations in Solidity 
(such as can’t be returned from a function to a contract).

If data can fit into 32 bytes, then you should use `bytes32` datatype rather than `bytes` or `strings`
 as it is cheaper in solidity. 
 Basically, any fixed size variable in solidity is cheaper than variable size. 
 That will save gas on the contract.


**There is `1` instance of this issue:**

- `BytesConstants.bad` (solidity/test_constants_optimization.sol#L2) should use `bytes(1..31)` instead of `string`.


### recommendation:

Replace `string` constant with `bytes(1..32)` constant.


### locations:
- solidity/test_constants_optimization.sol#L2

### severity:
Optimization

### category:
string-constants

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `2` instances of this issue:**

- `require(bool,string)(checkRole.checkOnlyRole(keccak256(bytes)(TIMELOCK),msg.sender),not authorized)` (solidity/test_constants_optimization.sol#L32-L35) should use custom error to save gas.

- `require(bool,string)(checkRole.checkOnlyRole(keccak256(bytes)(role),msg.sender),not authorized)` (solidity/test_constants_optimization.sol#L44-L47) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_constants_optimization.sol#L32-L35
- solidity/test_constants_optimization.sol#L44-L47

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- `ContstantInKeccak.checkRole` (solidity/test_constants_optimization.sol#L25) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_constants_optimization.sol#L25

### severity:
Optimization

### category:
constable-states
