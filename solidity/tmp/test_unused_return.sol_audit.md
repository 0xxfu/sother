## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 3 |
| [M-1] | Integer Overflow and Underflow | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 5 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused local variables | 2 |



## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There are `3` instances of this issue:**

- [User.test(Target)](solidity/tmp/test_unused_return.sol#L17-L36) ignores return value by [t.f()](solidity/tmp/test_unused_return.sol#L18)

- [User.test(Target)](solidity/tmp/test_unused_return.sol#L17-L36) ignores return value by [t.g()](solidity/tmp/test_unused_return.sol#L30)

- [User.test(Target)](solidity/tmp/test_unused_return.sol#L17-L36) ignores return value by [a.add(0)](solidity/tmp/test_unused_return.sol#L22)

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

### recommendation
Ensure that all the return values of the function calls are used.

### locations
- solidity/tmp/test_unused_return.sol#L17-L36
- solidity/tmp/test_unused_return.sol#L17-L36
- solidity/tmp/test_unused_return.sol#L17-L36

### severity
Medium

### category
unused-return

### confidence
Medium

## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `2` instances of this issue:**

- add(uint256,uint256) has possible integer overflow/underflow:
	- [a + b](solidity/tmp/test_unused_return.sol#L4)

- good(Target) has possible integer overflow/underflow:
	- [c = a + 1](solidity/tmp/test_unused_return.sol#L40)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_unused_return.sol#L4
- solidity/tmp/test_unused_return.sol#L40

### severity
Medium

### category
integer-overflow

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

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `5` instances of this issue:**

- function:[SafeMath.add(uint256,uint256)](solidity/tmp/test_unused_return.sol#L3-L5)is public and can be replaced with external 

- function:[Target.f()](solidity/tmp/test_unused_return.sol#L9)is public and can be replaced with external 

- function:[Target.g()](solidity/tmp/test_unused_return.sol#L10)is public and can be replaced with external 

- function:[User.test(Target)](solidity/tmp/test_unused_return.sol#L17-L36)is public and can be replaced with external 

- function:[User.good(Target)](solidity/tmp/test_unused_return.sol#L38-L41)is public and can be replaced with external 

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
- solidity/tmp/test_unused_return.sol#L3-L5
- solidity/tmp/test_unused_return.sol#L9
- solidity/tmp/test_unused_return.sol#L10
- solidity/tmp/test_unused_return.sol#L17-L36
- solidity/tmp/test_unused_return.sol#L38-L41

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `2` instances of this issue:**

- The local variables in [User.test(Target)](solidity/tmp/test_unused_return.sol#L17-L36) are unused.
	- [User.test(Target).d](solidity/tmp/test_unused_return.sol#L32)
	- [User.test(Target).e](solidity/tmp/test_unused_return.sol#L35)
	- [User.test(Target).c](solidity/tmp/test_unused_return.sol#L32)
	- [User.test(Target).b](solidity/tmp/test_unused_return.sol#L28)

- The local variables in [User.good(Target)](solidity/tmp/test_unused_return.sol#L38-L41) are unused.
	- [User.good(Target).c](solidity/tmp/test_unused_return.sol#L40)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_unused_return.sol#L17-L36
- solidity/tmp/test_unused_return.sol#L38-L41

### severity
Optimization

### category
unused-local-var

### confidence
High
