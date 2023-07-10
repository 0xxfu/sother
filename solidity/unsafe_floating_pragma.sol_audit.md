## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe to use floating pragma | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 3 |
| [N-1] | Different pragma directives are used | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.20` for gas reduction and improved security. | 2 |



## [Low] Unsafe to use floating pragma

### description:

Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).


**There is `1` instance of this issue:**

- Should lock the pragma version instead of floating pragma: [^0.8.19](solidity/unsafe_floating_pragma.sol#L1). 


### recommendation:

Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.


### locations:
- solidity/unsafe_floating_pragma.sol#L1

### severity:
Low

### category:
unsafe-floating-pragma

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `3` instances of this issue:**

- Pragma version[^0.8.19](solidity/unsafe_floating_pragma.sol#L1) allows old versions

- Pragma version[0.8.19](solidity/unsafe_floating_pragma.sol#L5) allows old versions

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
- solidity/unsafe_floating_pragma.sol#L1
- solidity/unsafe_floating_pragma.sol#L5
- 

### severity:
Informational

### category:
solc-version

## [Informational] Different pragma directives are used

### description:
Detect whether different Solidity versions are used.

**There is `1` instance of this issue:**

- Different versions of Solidity are used:
	- Version used: ['0.8.19', '^0.8.19']
	- [0.8.19](solidity/unsafe_floating_pragma.sol#L5)
	- [^0.8.19](solidity/unsafe_floating_pragma.sol#L1)


### recommendation:
Use one Solidity version.

### locations:
- solidity/unsafe_floating_pragma.sol#L5

### severity:
Informational

### category:
pragma

## [Optimization] Should use latest solidity version `0.8.20` for gas reduction and improved security.

### description:

[Solidity v0.8.20](https://blog.soliditylang.org/2023/05/10/solidity-0.8.20-release-announcement/) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(0.8.20) for gas reduction and improved security.


**There are `2` instances of this issue:**

- pragma solidity version [^0.8.19](solidity/unsafe_floating_pragma.sol#L1) should upgrade to the latest version: 0.8.20
- pragma solidity version [0.8.19](solidity/unsafe_floating_pragma.sol#L5) should upgrade to the latest version: 0.8.20

### recommendation:
Upgrade solidity version to the latest version: 0.8.20

### locations:
- solidity/unsafe_floating_pragma.sol#L1
- solidity/unsafe_floating_pragma.sol#L5

### severity:
Optimization

### category:
upgrade-to-latest
