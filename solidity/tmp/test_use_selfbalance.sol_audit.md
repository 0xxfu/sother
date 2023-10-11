## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 2 |
| [N-2] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 2 |
| [G-1] | Use `selfbalance()` instead of `address(this).balance` | 1 |
| [G-2] | Use `balance(address)` instead of address.balance() | 1 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `2` instances of this issue:**

- bad2(address) has possible integer overflow/underflow:
	- [bal ++](solidity/tmp/test_use_selfbalance.sol#L8)

- notBad2(address) has possible integer overflow/underflow:
	- [bal ++](solidity/tmp/test_use_selfbalance.sol#L24)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_use_selfbalance.sol#L8
- solidity/tmp/test_use_selfbalance.sol#L24

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

## [Informational] Assembly usage

### description
The use of assembly is error-prone and should be avoided.

**There are `2` instances of this issue:**

- [UseSelfbalance.notBad()](solidity/tmp/test_use_selfbalance.sol#L11-L17) uses assembly
	- [INLINE ASM](solidity/tmp/test_use_selfbalance.sol#L12-L16)

- [UseSelfbalance.notBad2(address)](solidity/tmp/test_use_selfbalance.sol#L19-L25) uses assembly
	- [INLINE ASM](solidity/tmp/test_use_selfbalance.sol#L21-L23)


### recommendation
Do not use `evm` assembly.

### locations
- solidity/tmp/test_use_selfbalance.sol#L11-L17
- solidity/tmp/test_use_selfbalance.sol#L19-L25

### severity
Informational

### category
assembly

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `4` instances of this issue:**

- function:[UseSelfbalance.bad()](solidity/tmp/test_use_selfbalance.sol#L2-L4)is public and can be replaced with external 

- function:[UseSelfbalance.bad2(address)](solidity/tmp/test_use_selfbalance.sol#L6-L9)is public and can be replaced with external 

- function:[UseSelfbalance.notBad()](solidity/tmp/test_use_selfbalance.sol#L11-L17)is public and can be replaced with external 

- function:[UseSelfbalance.notBad2(address)](solidity/tmp/test_use_selfbalance.sol#L19-L25)is public and can be replaced with external 

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
- solidity/tmp/test_use_selfbalance.sol#L2-L4
- solidity/tmp/test_use_selfbalance.sol#L6-L9
- solidity/tmp/test_use_selfbalance.sol#L11-L17
- solidity/tmp/test_use_selfbalance.sol#L19-L25

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)

### description

`++i` costs less gas compared to `i++` or `i += 1` for unsigned integer, as pre-increment is cheaper (about 5 gas per iteration). 
This statement is true even with the optimizer enabled.

`i++` increments i and returns the initial value of i. Which means:
```
uint i = 1;  
i++; // == 1 but i == 2  
```
But ++i returns the actual incremented value:
```
uint i = 1;  
++i; // == 2 and i == 2 too, so no need for a temporary variable  
```
In the first case, the compiler has to create a temporary variable (when used) 
for returning 1 instead of 2


**There are `2` instances of this issue:**

- [bal ++](solidity/tmp/test_use_selfbalance.sol#L8) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [bal ++](solidity/tmp/test_use_selfbalance.sol#L24) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.


### recommendation

Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.



### locations
- solidity/tmp/test_use_selfbalance.sol#L8
- solidity/tmp/test_use_selfbalance.sol#L24

### severity
Optimization

### category
pre-plus-plus

### confidence
High

## [Optimization] Use `selfbalance()` instead of `address(this).balance`

### description

You can use `selfbalance()` instead of `address(this).balance` when 
getting your contract’s balance of ETH to save gas. 
Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH.


**There is `1` instance of this issue:**

- Should use `selfbalance()` instead of [address(this).balance](solidity/tmp/test_use_selfbalance.sol#L3)


### recommendation

Using `selfbalance()` instead of `address(this).balance`, for example:

```
function assemblyInternalBalance() public returns (uint256) {
    assembly {
        let c := selfbalance()
        mstore(0x00, c)
        return(0x00, 0x20)
    }
}
```


### locations
- solidity/tmp/test_use_selfbalance.sol#L3

### severity
Optimization

### category
use-self-balance

### confidence
High

## [Optimization] Use `balance(address)` instead of address.balance()

### description

Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH to save gas.


**There is `1` instance of this issue:**

- Should use `balance(address)` instead of [bal = address(addr).balance](solidity/tmp/test_use_selfbalance.sol#L7)


### recommendation

Use `balance(address)` instead of address.balance(), for example:

```
function assemblyExternalBalance(address addr) public {
    uint256 bal;
    assembly {
        bal := balance(addr)
    }
}
```


### locations
- solidity/tmp/test_use_selfbalance.sol#L7

### severity
Optimization

### category
use-assembly-balance

### confidence
High
