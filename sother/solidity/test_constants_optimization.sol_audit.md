## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 6 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Do not calculate constants | 4 |
| [G-1] | Using `private` rather than `public` for constants, saves gas | 2 |
| [G-2] | `Bytes` constants are more efficient than `string` constants | 1 |



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

**There are `6` instances of this issue:**

- Constant `CalculateConstants.bad` (solidity/test_constants_optimization.sol#L7) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad2` (solidity/test_constants_optimization.sol#L8) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad3` (solidity/test_constants_optimization.sol#L9) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.bad4` (solidity/test_constants_optimization.sol#L10) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.notBad` (solidity/test_constants_optimization.sol#L11) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant `CalculateConstants.notBad2` (solidity/test_constants_optimization.sol#L12) is not in UPPER_CASE_WITH_UNDERSCORES


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_constants_optimization.sol#L7
- solidity/test_constants_optimization.sol#L8
- solidity/test_constants_optimization.sol#L9
- solidity/test_constants_optimization.sol#L10
- solidity/test_constants_optimization.sol#L11
- solidity/test_constants_optimization.sol#L12

### severity:
Informational

### category:
naming-convention

## [Optimization] Do not calculate constants

### description:

Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.


**There are `4` instances of this issue:**

- `CalculateConstants.bad` (solidity/test_constants_optimization.sol#L7) should use hardcode instead of calculation.

- `CalculateConstants.bad2` (solidity/test_constants_optimization.sol#L8) should use hardcode instead of calculation.

- `CalculateConstants.bad3` (solidity/test_constants_optimization.sol#L9) should use hardcode instead of calculation.

- `CalculateConstants.bad4` (solidity/test_constants_optimization.sol#L10) should use hardcode instead of calculation.


### recommendation:

Pre-calculate the results(hardcode) instead of runtime calculation.


### locations:
- solidity/test_constants_optimization.sol#L7
- solidity/test_constants_optimization.sol#L8
- solidity/test_constants_optimization.sol#L9
- solidity/test_constants_optimization.sol#L10

### severity:
Optimization

### category:
calculate-constants

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
