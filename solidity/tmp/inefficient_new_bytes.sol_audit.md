## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 2 |
| [G-1] | Expression `""` is cheaper than `new bytes(0)` | 2 |



## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [InefficientNewBytes.bad(bytes)](solidity/tmp/inefficient_new_bytes.sol#L4-L7) does not emit an event

- Setter function [InefficientNewBytes.notBad(bytes)](solidity/tmp/inefficient_new_bytes.sol#L9-L12) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/inefficient_new_bytes.sol#L4-L7
- solidity/tmp/inefficient_new_bytes.sol#L9-L12

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

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [InefficientNewBytes.bad(bytes)](solidity/tmp/inefficient_new_bytes.sol#L4-L7) are unused.
	- [InefficientNewBytes.bad(bytes).a](solidity/tmp/inefficient_new_bytes.sol#L4)

- The param variables in [InefficientNewBytes.notBad(bytes)](solidity/tmp/inefficient_new_bytes.sol#L9-L12) are unused.
	- [InefficientNewBytes.notBad(bytes).a](solidity/tmp/inefficient_new_bytes.sol#L9)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/inefficient_new_bytes.sol#L4-L7
- solidity/tmp/inefficient_new_bytes.sol#L9-L12

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Expression `""` is cheaper than `new bytes(0)`

### description




**There are `2` instances of this issue:**

- Should use `""` instead of `new bytes(0)` on [a = new bytes(0)](solidity/tmp/inefficient_new_bytes.sol#L5)

- Should use `""` instead of `new bytes(0)` on [byt = new bytes(0)](solidity/tmp/inefficient_new_bytes.sol#L6)


### recommendation

Using empty string `""` instead of `new bytes(0)`.


### locations
- solidity/tmp/inefficient_new_bytes.sol#L5
- solidity/tmp/inefficient_new_bytes.sol#L6

### severity
Optimization

### category
inefficient-new-bytes

### confidence
High
