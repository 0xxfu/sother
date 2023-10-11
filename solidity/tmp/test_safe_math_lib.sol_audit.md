## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Divide before multiply | 8 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe to use floating pragma | 1 |
| [L-1] | Division by zero not prevented | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | Assembly usage | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 6 |
| [G-2] | Using custom errors replace `require` or `assert` | 8 |
| [G-3] | Remove or replace unused state variables | 1 |
| [G-4] | Not using the named return variables anywhere in the function is confusing | 1 |
| [G-5] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 1 |
| [G-6] | Don't use `SafeMath` if use solidity version `>=0.8.0` | 1 |
| [G-7] | Dead-code: functions not used should be removed to save deployment gas | 32 |
| [G-8] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 4 |
| [G-9] | `!= 0` is less gas than `> 0` for unsigned integers | 6 |
| [G-10] | Shortening revert strings to fit in 32 `bytes` | 1 |
| [G-11] | Use `delete` to Clear Variables | 5 |
| [G-12] | State variables that could be declared constant | 1 |



## [Medium] Divide before multiply

### description
Solidity's integer division truncates. Thus, performing division before multiplication can lead to precision loss.

**There are `8` instances of this issue:**

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse = (3 * denominator) ^ 2](solidity/tmp/test_safe_math_lib.sol#L208)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L212)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [prod0 = prod0 / twos](solidity/tmp/test_safe_math_lib.sol#L196)
	- [result = prod0 * inverse](solidity/tmp/test_safe_math_lib.sol#L223)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L213)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L215)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L214)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L216)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/tmp/test_safe_math_lib.sol#L217)

#### Exploit scenario

```solidity
contract A {
	function f(uint n) public {
        coins = (oldSupply / n) * interest;
    }
}
```
If `n` is greater than `oldSupply`, `coins` will be zero. For example, with `oldSupply = 5; n = 10, interest = 2`, coins will be zero.  
If `(oldSupply * interest / n)` was used, `coins` would have been `1`.   
In general, it's usually a good idea to re-arrange arithmetic to perform multiplication before division, unless the limit of a smaller type makes this dangerous.

### recommendation
Consider ordering multiplication before division.

### locations
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L141-L226

### severity
Medium

### category
divide-before-multiply

### confidence
Medium

## [Low] Unsafe to use floating pragma

### description

Contracts should be deployed with the same compiler version and flags that 
they have been tested with thoroughly. 
Locking the pragma helps to ensure that contracts do not accidentally get deployed using, 
for example, an outdated compiler version that might introduce bugs that affect the 
contract system negatively.

More detail see [SWC-103](https://swcregistry.io/docs/SWC-103).


**There is `1` instance of this issue:**

- Should lock the pragma version instead of floating pragma: [^0.8.9](solidity/tmp/test_safe_math_lib.sol#L2). 


### recommendation

Lock the pragma version and also consider known bugs (https://github.com/ethereum/solidity/releases) 
for the compiler version that is chosen.


### locations
- solidity/tmp/test_safe_math_lib.sol#L2

### severity
Low

### category
unsafe-floating-pragma

### confidence
High

## [Low] Division by zero not prevented

### description

In Solidity, transactions are reverted with the "division by zero" error
message when a division by zero is attempted.
Although divisions by zero will result in reversions, 
they will not have error messages, 
making failed transaction more difficult to debug by users.

Consider actively preventing divisions by zero with appropriate `revert` statements that 
have informative and user-friendly error messages.


**There are `12` instances of this issue:**

- [prod0 / denominator](solidity/tmp/test_safe_math_lib.sol#L163) possible divisions by `0` can be performed.

- [denominator = denominator / twos](solidity/tmp/test_safe_math_lib.sol#L193) possible divisions by `0` can be performed.

- [prod0 = prod0 / twos](solidity/tmp/test_safe_math_lib.sol#L196) possible divisions by `0` can be performed.

- [twos = 0 - twos / twos + 1](solidity/tmp/test_safe_math_lib.sol#L199) possible divisions by `0` can be performed.

- [value /= 10 ** 64](solidity/tmp/test_safe_math_lib.sol#L363) possible divisions by `0` can be performed.

- [value /= 10 ** 32](solidity/tmp/test_safe_math_lib.sol#L367) possible divisions by `0` can be performed.

- [value /= 10 ** 16](solidity/tmp/test_safe_math_lib.sol#L371) possible divisions by `0` can be performed.

- [value /= 10 ** 8](solidity/tmp/test_safe_math_lib.sol#L375) possible divisions by `0` can be performed.

- [value /= 10 ** 4](solidity/tmp/test_safe_math_lib.sol#L379) possible divisions by `0` can be performed.

- [value /= 10 ** 2](solidity/tmp/test_safe_math_lib.sol#L383) possible divisions by `0` can be performed.

- [c = a / b](solidity/tmp/test_safe_math_lib.sol#L528) possible divisions by `0` can be performed.

- [require(bool,string)(c / a == b,"SafeMath: multiplication overflow")](solidity/tmp/test_safe_math_lib.sol#L598) possible divisions by `0` can be performed.


### recommendation

It is recommended to add a sanity check to control whether the borrowed
amount is zero or not.


### locations
- solidity/tmp/test_safe_math_lib.sol#L163
- solidity/tmp/test_safe_math_lib.sol#L193
- solidity/tmp/test_safe_math_lib.sol#L196
- solidity/tmp/test_safe_math_lib.sol#L199
- solidity/tmp/test_safe_math_lib.sol#L363
- solidity/tmp/test_safe_math_lib.sol#L367
- solidity/tmp/test_safe_math_lib.sol#L371
- solidity/tmp/test_safe_math_lib.sol#L375
- solidity/tmp/test_safe_math_lib.sol#L379
- solidity/tmp/test_safe_math_lib.sol#L383
- solidity/tmp/test_safe_math_lib.sol#L528
- solidity/tmp/test_safe_math_lib.sol#L598

### severity
Low

### category
division-by-zero

### confidence
High

## [Informational] Incorrect versions of Solidity

### description

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- Pragma version[^0.8.9](solidity/tmp/test_safe_math_lib.sol#L2) allows old versions

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
- solidity/tmp/test_safe_math_lib.sol#L2
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

**There is `1` instance of this issue:**

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) uses assembly
	- [INLINE ASM](solidity/tmp/test_safe_math_lib.sol#L152-L156)
	- [INLINE ASM](solidity/tmp/test_safe_math_lib.sol#L177-L184)
	- [INLINE ASM](solidity/tmp/test_safe_math_lib.sol#L191-L200)


### recommendation
Do not use `evm` assembly.

### locations
- solidity/tmp/test_safe_math_lib.sol#L141-L226

### severity
Informational

### category
assembly

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [^0.8.9](solidity/tmp/test_safe_math_lib.sol#L2) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/test_safe_math_lib.sol#L2

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There are `6` instances of this issue:**

- [Math.min(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L107-L109) could be inlined to save gas.

- [Math.mulDiv(uint256,uint256,uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L231-L242) could be inlined to save gas.

- [Math.sqrt(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L285-L295) could be inlined to save gas.

- [Math.log2(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L343-L353) could be inlined to save gas.

- [Math.log10(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L397-L407) could be inlined to save gas.

- [Math.log256(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L445-L455) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/tmp/test_safe_math_lib.sol#L107-L109
- solidity/tmp/test_safe_math_lib.sol#L231-L242
- solidity/tmp/test_safe_math_lib.sol#L285-L295
- solidity/tmp/test_safe_math_lib.sol#L343-L353
- solidity/tmp/test_safe_math_lib.sol#L397-L407
- solidity/tmp/test_safe_math_lib.sol#L445-L455

### severity
Optimization

### category
internal-function-to-inline

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `8` instances of this issue:**

- [require(bool,string)(c >= a,"SafeMath: addition overflow")](solidity/tmp/test_safe_math_lib.sol#L564) should use custom error to save gas.

- [require(bool,string)(b <= a,"SafeMath: subtraction overflow")](solidity/tmp/test_safe_math_lib.sol#L580) should use custom error to save gas.

- [require(bool,string)(c / a == b,"SafeMath: multiplication overflow")](solidity/tmp/test_safe_math_lib.sol#L598) should use custom error to save gas.

- [require(bool,string)(b > 0,"SafeMath: division by zero")](solidity/tmp/test_safe_math_lib.sol#L614) should use custom error to save gas.

- [require(bool,string)(b > 0,"SafeMath: modulo by zero")](solidity/tmp/test_safe_math_lib.sol#L633) should use custom error to save gas.

- [require(bool,string)(b <= a,errorMessage)](solidity/tmp/test_safe_math_lib.sol#L657) should use custom error to save gas.

- [require(bool,string)(b > 0,errorMessage)](solidity/tmp/test_safe_math_lib.sol#L680) should use custom error to save gas.

- [require(bool,string)(b > 0,errorMessage)](solidity/tmp/test_safe_math_lib.sol#L706) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_safe_math_lib.sol#L564
- solidity/tmp/test_safe_math_lib.sol#L580
- solidity/tmp/test_safe_math_lib.sol#L598
- solidity/tmp/test_safe_math_lib.sol#L614
- solidity/tmp/test_safe_math_lib.sol#L633
- solidity/tmp/test_safe_math_lib.sol#L657
- solidity/tmp/test_safe_math_lib.sol#L680
- solidity/tmp/test_safe_math_lib.sol#L706

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Remove or replace unused state variables

### description

Saves a storage slot. If the variable is assigned a non-zero value, 
saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). 
If the variable remains unassigned, there is no gas savings unless the variable is public, 
in which case the compiler-generated non-payable getter deployment cost is saved. 
If the state variable is overriding an interface's public function, 
mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [SafeMathLib.stateInt](solidity/tmp/test_safe_math_lib.sol#L716) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/test_safe_math_lib.sol#L716

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Not using the named return variables anywhere in the function is confusing

### description

Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.


**There is `1` instance of this issue:**

- The named return variables in [SafeMath.mod(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L631-L636) are unused.
	- [SafeMath.mod(uint256,uint256).c](solidity/tmp/test_safe_math_lib.sol#L631)


### recommendation

Remove the unused named return variables.


### locations
- solidity/tmp/test_safe_math_lib.sol#L631-L636

### severity
Optimization

### category
unused-named-return-variables

### confidence
High

## [Optimization] Using `x >> constant(uint)` with the right shift operator is a more gas-efficient

### description

`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, 
the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) 
due to `JUMP`s to and from a compiler utility function that introduces checks which can 
be avoided by using `unchecked {}` around the division by two



**There is `1` instance of this issue:**

- [(a & b) + (a ^ b) / 2](solidity/tmp/test_safe_math_lib.sol#L117) should use right shift `>>` operator to save gas.


### recommendation

Using bit shifting (`>>` operator) replace division divided by constant.


### locations
- solidity/tmp/test_safe_math_lib.sol#L117

### severity
Optimization

### category
divide-by-constant

### confidence
High

## [Optimization] Don't use `SafeMath` if use solidity version `>=0.8.0`

### description

Version `>=0.8.0` introduces internal overflow checks, using `SafeMath` function calls will be more expensive than just built in arithmetic, so using SafeMath is redundant and adds overhead.

More detail see [Solidity 0.8.0 Release Announcement](https://blog.soliditylang.org/2020/12/16/solidity-v0.8.0-release-announcement/#:~:text=the%20full%20list!-,Checked%20Arithmetic,-The%20%E2%80%9CChecked%20Arithmetic) and [OpenZeppelin discussion](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2465)


**There is `1` instance of this issue:**

- `SafeMath` used in [SafeMathLib](solidity/tmp/test_safe_math_lib.sol#L712-L717) should be removed

### recommendation

Remove `SafeMath` lib.


### locations
- solidity/tmp/test_safe_math_lib.sol#L712-L717

### severity
Optimization

### category
safe-math-lib

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There are `32` instances of this issue:**

- [Math.tryAdd(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L21-L30) is never used and should be removed

- [Math.trySub(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L37-L45) is never used and should be removed

- [Math.tryMul(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L52-L65) is never used and should be removed

- [Math.tryDiv(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L72-L80) is never used and should be removed

- [Math.tryMod(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L87-L95) is never used and should be removed

- [Math.max(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L100-L102) is never used and should be removed

- [Math.min(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L107-L109) is never used and should be removed

- [Math.average(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L115-L118) is never used and should be removed

- [Math.ceilDiv(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L126-L134) is never used and should be removed

- [Math.mulDiv(uint256,uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L141-L226) is never used and should be removed

- [Math.mulDiv(uint256,uint256,uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L231-L242) is never used and should be removed

- [Math.sqrt(uint256)](solidity/tmp/test_safe_math_lib.sol#L249-L280) is never used and should be removed

- [Math.sqrt(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L285-L295) is never used and should be removed

- [Math.log2(uint256)](solidity/tmp/test_safe_math_lib.sol#L301-L337) is never used and should be removed

- [Math.log2(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L343-L353) is never used and should be removed

- [Math.log10(uint256)](solidity/tmp/test_safe_math_lib.sol#L359-L391) is never used and should be removed

- [Math.log10(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L397-L407) is never used and should be removed

- [Math.log256(uint256)](solidity/tmp/test_safe_math_lib.sol#L415-L439) is never used and should be removed

- [Math.log256(uint256,Math.Rounding)](solidity/tmp/test_safe_math_lib.sol#L445-L455) is never used and should be removed

- [SafeMath.tryAdd(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L464-L473) is never used and should be removed

- [SafeMath.trySub(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L480-L490) is never used and should be removed

- [SafeMath.tryMul(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L497-L515) is never used and should be removed

- [SafeMath.tryDiv(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L522-L532) is never used and should be removed

- [SafeMath.tryMod(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L539-L549) is never used and should be removed

- [SafeMath.add(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L561-L566) is never used and should be removed

- [SafeMath.sub(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L578-L583) is never used and should be removed

- [SafeMath.mul(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L595-L600) is never used and should be removed

- [SafeMath.div(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L612-L617) is never used and should be removed

- [SafeMath.mod(uint256,uint256)](solidity/tmp/test_safe_math_lib.sol#L631-L636) is never used and should be removed

- [SafeMath.sub(uint256,uint256,string)](solidity/tmp/test_safe_math_lib.sol#L651-L660) is never used and should be removed

- [SafeMath.div(uint256,uint256,string)](solidity/tmp/test_safe_math_lib.sol#L674-L683) is never used and should be removed

- [SafeMath.mod(uint256,uint256,string)](solidity/tmp/test_safe_math_lib.sol#L700-L709) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/test_safe_math_lib.sol#L21-L30
- solidity/tmp/test_safe_math_lib.sol#L37-L45
- solidity/tmp/test_safe_math_lib.sol#L52-L65
- solidity/tmp/test_safe_math_lib.sol#L72-L80
- solidity/tmp/test_safe_math_lib.sol#L87-L95
- solidity/tmp/test_safe_math_lib.sol#L100-L102
- solidity/tmp/test_safe_math_lib.sol#L107-L109
- solidity/tmp/test_safe_math_lib.sol#L115-L118
- solidity/tmp/test_safe_math_lib.sol#L126-L134
- solidity/tmp/test_safe_math_lib.sol#L141-L226
- solidity/tmp/test_safe_math_lib.sol#L231-L242
- solidity/tmp/test_safe_math_lib.sol#L249-L280
- solidity/tmp/test_safe_math_lib.sol#L285-L295
- solidity/tmp/test_safe_math_lib.sol#L301-L337
- solidity/tmp/test_safe_math_lib.sol#L343-L353
- solidity/tmp/test_safe_math_lib.sol#L359-L391
- solidity/tmp/test_safe_math_lib.sol#L397-L407
- solidity/tmp/test_safe_math_lib.sol#L415-L439
- solidity/tmp/test_safe_math_lib.sol#L445-L455
- solidity/tmp/test_safe_math_lib.sol#L464-L473
- solidity/tmp/test_safe_math_lib.sol#L480-L490
- solidity/tmp/test_safe_math_lib.sol#L497-L515
- solidity/tmp/test_safe_math_lib.sol#L522-L532
- solidity/tmp/test_safe_math_lib.sol#L539-L549
- solidity/tmp/test_safe_math_lib.sol#L561-L566
- solidity/tmp/test_safe_math_lib.sol#L578-L583
- solidity/tmp/test_safe_math_lib.sol#L595-L600
- solidity/tmp/test_safe_math_lib.sol#L612-L617
- solidity/tmp/test_safe_math_lib.sol#L631-L636
- solidity/tmp/test_safe_math_lib.sol#L651-L660
- solidity/tmp/test_safe_math_lib.sol#L674-L683
- solidity/tmp/test_safe_math_lib.sol#L700-L709

### severity
Optimization

### category
dead-code

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


**There are `4` instances of this issue:**

- [result += 1](solidity/tmp/test_safe_math_lib.sol#L239) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [result += 1](solidity/tmp/test_safe_math_lib.sol#L333) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [result += 1](solidity/tmp/test_safe_math_lib.sol#L387) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [result += 1](solidity/tmp/test_safe_math_lib.sol#L435) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.


### recommendation

Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.



### locations
- solidity/tmp/test_safe_math_lib.sol#L239
- solidity/tmp/test_safe_math_lib.sol#L333
- solidity/tmp/test_safe_math_lib.sol#L387
- solidity/tmp/test_safe_math_lib.sol#L435

### severity
Optimization

### category
pre-plus-plus

### confidence
High

## [Optimization] `!= 0` is less gas than `> 0` for unsigned integers

### description

`!= 0` costs less gas compared to `> 0` for unsigned integers in require statements 
with the optimizer enabled (6 gas)

While it may seem that `> 0` is cheaper than `!=`, this is only true without the 
optimizer enabled and outside a require statement. 
If you enable the optimizer at 10k and you’re in a `require` statement, 
this will save gas.



**There are `6` instances of this issue:**

- [b > 0](solidity/tmp/test_safe_math_lib.sol#L527) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [b > 0](solidity/tmp/test_safe_math_lib.sol#L544) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(b > 0,"SafeMath: division by zero")](solidity/tmp/test_safe_math_lib.sol#L614) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(b > 0,"SafeMath: modulo by zero")](solidity/tmp/test_safe_math_lib.sol#L633) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(b > 0,errorMessage)](solidity/tmp/test_safe_math_lib.sol#L680) should use `!= 0` instead of `> 0` for unsigned integer comparison.

- [require(bool,string)(b > 0,errorMessage)](solidity/tmp/test_safe_math_lib.sol#L706) should use `!= 0` instead of `> 0` for unsigned integer comparison.


### recommendation

Use `!= 0` instead of `> 0` for unsigned integer comparison.


### locations
- solidity/tmp/test_safe_math_lib.sol#L527
- solidity/tmp/test_safe_math_lib.sol#L544
- solidity/tmp/test_safe_math_lib.sol#L614
- solidity/tmp/test_safe_math_lib.sol#L633
- solidity/tmp/test_safe_math_lib.sol#L680
- solidity/tmp/test_safe_math_lib.sol#L706

### severity
Optimization

### category
unsigned-int-compare-zero

### confidence
High

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There is `1` instance of this issue:**

- [require(bool,string)(c / a == b,"SafeMath: multiplication overflow")](solidity/tmp/test_safe_math_lib.sol#L598) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation

Shortening revert strings to fit in 32 `bytes`


### locations
- solidity/tmp/test_safe_math_lib.sol#L598

### severity
Optimization

### category
revert-long-strings

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


**There are `5` instances of this issue:**

- Should use `delete` statement instead of [result = 0](solidity/tmp/test_safe_math_lib.sol#L302)

- Should use `delete` statement instead of [result = 0](solidity/tmp/test_safe_math_lib.sol#L360)

- Should use `delete` statement instead of [result = 0](solidity/tmp/test_safe_math_lib.sol#L416)

- Should use `delete` statement instead of [c = 0](solidity/tmp/test_safe_math_lib.sol#L470)

- Should use `delete` statement instead of [c = 0](solidity/tmp/test_safe_math_lib.sol#L509)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/test_safe_math_lib.sol#L302
- solidity/tmp/test_safe_math_lib.sol#L360
- solidity/tmp/test_safe_math_lib.sol#L416
- solidity/tmp/test_safe_math_lib.sol#L470
- solidity/tmp/test_safe_math_lib.sol#L509

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [SafeMathLib.stateInt](solidity/tmp/test_safe_math_lib.sol#L716) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_safe_math_lib.sol#L716

### severity
Optimization

### category
state-should-be-constant

### confidence
High
