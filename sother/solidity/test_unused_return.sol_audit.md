## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The result of function calls should be cached rather than re-calling the function | 1 |
| [G-1] | Use `calldata` instead of `memory` for function parameters | 2 |



## [Medium] Unused return

### description:
The return value of an external call is not stored in a local or state variable.

**There are `3` instances of this issue:**

- [User.test(Target)](solidity/test_unused_return.sol#L17-L36) ignores return value by [a.add(0)](solidity/test_unused_return.sol#L22)

- [User.test(Target)](solidity/test_unused_return.sol#L17-L36) ignores return value by [t.f()](solidity/test_unused_return.sol#L18)

- [User.test(Target)](solidity/test_unused_return.sol#L17-L36) ignores return value by [t.g()](solidity/test_unused_return.sol#L30)

#### Exploit scenario

```solidity
contract MyConc{
    using SafeMath for uint;   
    function my_func(uint a, uint b) public{
        a.add(b);
    }
}
```
`MyConc` calls `add` of `SafeMath`, but does not store the result in `a`. As a result, the computation has no effect.

### recommendation:
Ensure that all the return values of the function calls are used.

### locations:
- solidity/test_unused_return.sol#L17-L36
- solidity/test_unused_return.sol#L17-L36
- solidity/test_unused_return.sol#L17-L36

### severity:
Medium

### category:
unused-return

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

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description:

The instances below point to the second+ call of the function within a single function


**There is `1` instance of this issue:**

- `Target.g()` called result should be cached with local variable in [User.test(Target)](solidity/test_unused_return.sol#L17-L36), It is called more than once:
	- [(e) = t.g()](solidity/test_unused_return.sol#L35)
	- [(c,d) = t.g()](solidity/test_unused_return.sol#L32)
	- [t.g()](solidity/test_unused_return.sol#L30)


### recommendation:

Using local variable to cache function called result if the same function called more than once.


### locations:
- solidity/test_unused_return.sol#L17-L36

### severity:
Optimization

### category:
cache-call-function-result

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `2` instances of this issue:**

- [User.test(Target)](solidity/test_unused_return.sol#L17-L36) read-only `memory` parameters below should be changed to `calldata` :
	- [User.test(Target).t](solidity/test_unused_return.sol#L17)

- [User.good(Target)](solidity/test_unused_return.sol#L38-L41) read-only `memory` parameters below should be changed to `calldata` :
	- [User.good(Target).t](solidity/test_unused_return.sol#L38)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_unused_return.sol#L17-L36
- solidity/test_unused_return.sol#L38-L41

### severity:
Optimization

### category:
memory-in-parameters
