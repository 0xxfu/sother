## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe to use floating pragma | 1 |
| [L-1] | Missing Event Setter | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-1] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 2 |
| [G-2] | Remove unused local variables | 2 |
| [G-3] | Use `delete` to Clear Variables | 2 |



## [Low] Unsafe to use floating pragma

### description

Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).


**There is `1` instance of this issue:**

- Should lock the pragma version instead of floating pragma: [^0.8.17](solidity/tmp/test_assignment_operation.sol#L2). 


### recommendation

Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.


### locations
- solidity/tmp/test_assignment_operation.sol#L2

### severity
Low

### category
unsafe-floating-pragma

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `3` instances of this issue:**

- Setter function [StateVarPlusEqVsEqPlus.slitherConstructorVariables()](solidity/tmp/test_assignment_operation.sol#L8-L24) does not emit an event

- Setter function [StateVarPlusEqVsEqPlus.test()](solidity/tmp/test_assignment_operation.sol#L12-L16) does not emit an event

- Setter function [StateVarPlusEqVsEqPlus.test2()](solidity/tmp/test_assignment_operation.sol#L18-L23) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_assignment_operation.sol#L8-L24
- solidity/tmp/test_assignment_operation.sol#L12-L16
- solidity/tmp/test_assignment_operation.sol#L18-L23

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

**There are `2` instances of this issue:**

- Pragma version[^0.8.17](solidity/tmp/test_assignment_operation.sol#L2) allows old versions

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
- solidity/tmp/test_assignment_operation.sol#L2
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [^0.8.17](solidity/tmp/test_assignment_operation.sol#L2) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/test_assignment_operation.sol#L2

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There are `2` instances of this issue:**

- should use arithmetic operator `=` replace `+=` in [varr += block.number](solidity/tmp/test_assignment_operation.sol#L14)
- should use arithmetic operator `=` replace `-=` in [varr -= 0](solidity/tmp/test_assignment_operation.sol#L21)

### recommendation
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### locations
- solidity/tmp/test_assignment_operation.sol#L14
- solidity/tmp/test_assignment_operation.sol#L21

### severity
Optimization

### category
assignment-left-operation

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `2` instances of this issue:**

- The local variables in [StateVarPlusEqVsEqPlus.test()](solidity/tmp/test_assignment_operation.sol#L12-L16) are unused.
	- [StateVarPlusEqVsEqPlus.test().localUint](solidity/tmp/test_assignment_operation.sol#L13)

- The local variables in [StateVarPlusEqVsEqPlus.test2()](solidity/tmp/test_assignment_operation.sol#L18-L23) are unused.
	- [StateVarPlusEqVsEqPlus.test2().localUint2](solidity/tmp/test_assignment_operation.sol#L19)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_assignment_operation.sol#L12-L16
- solidity/tmp/test_assignment_operation.sol#L18-L23

### severity
Optimization

### category
unused-local-var

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

- Should use `delete` statement instead of [localUint = 0](solidity/tmp/test_assignment_operation.sol#L13)

- Should use `delete` statement instead of [localUint2 = 0](solidity/tmp/test_assignment_operation.sol#L19)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/test_assignment_operation.sol#L13
- solidity/tmp/test_assignment_operation.sol#L19

### severity
Optimization

### category
use-delete-statement

### confidence
High
