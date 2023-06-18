## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Divide before multiply | 8 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 1 |
| [N-2] | Dead-code | 32 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 6 |
| [G-2] | Don't use `SafeMath` if use solidity version `>=0.8.0` | 1 |
| [G-3] | Remove or replace unused state variables | 1 |
| [G-4] | Reduce gas usage by moving to Solidity 0.8.19 or later | 1 |
| [G-5] | use custom errors instead of revert strings | 8 |
| [G-6] | State variables that could be declared constant | 1 |



## [Medium] Divide before multiply

### description:
Solidity's integer division truncates. Thus, performing division before multiplication can lead to precision loss.

**There are `8` instances of this issue:**

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [prod0 = prod0 / twos](solidity/test_safe_math_lib.sol#L196)
	- [result = prod0 * inverse](solidity/test_safe_math_lib.sol#L223)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L214)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse = (3 * denominator) ^ 2](solidity/test_safe_math_lib.sol#L208)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L213)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L217)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L212)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L216)

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) performs a multiplication on the result of a division:
	- [denominator = denominator / twos](solidity/test_safe_math_lib.sol#L193)
	- [inverse *= 2 - denominator * inverse](solidity/test_safe_math_lib.sol#L215)

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

### recommendation:
Consider ordering multiplication before division.

### location:
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L141-L226

### severity:
Medium

### category:
divide-before-multiply

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There is `1` instance of this issue:**

- Pragma version[^0.8.9](solidity/test_safe_math_lib.sol#L2) allows old versions


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.19

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### location:
- solidity/test_safe_math_lib.sol#L2

### severity:
Informational

### category:
solc-version

## [Informational] Assembly usage

### description:
The use of assembly is error-prone and should be avoided.

**There is `1` instance of this issue:**

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) uses assembly
	- [INLINE ASM](solidity/test_safe_math_lib.sol#L152-L156)
	- [INLINE ASM](solidity/test_safe_math_lib.sol#L177-L184)
	- [INLINE ASM](solidity/test_safe_math_lib.sol#L191-L200)


### recommendation:
Do not use `evm` assembly.

### location:
- solidity/test_safe_math_lib.sol#L141-L226

### severity:
Informational

### category:
assembly

## [Informational] Dead-code

### description:
Functions that are not sued.

**There are `32` instances of this issue:**

- [SafeMath.mul(uint256,uint256)](solidity/test_safe_math_lib.sol#L595-L600) is never used and should be removed

- [SafeMath.sub(uint256,uint256)](solidity/test_safe_math_lib.sol#L578-L583) is never used and should be removed

- [SafeMath.tryDiv(uint256,uint256)](solidity/test_safe_math_lib.sol#L522-L532) is never used and should be removed

- [Math.ceilDiv(uint256,uint256)](solidity/test_safe_math_lib.sol#L126-L134) is never used and should be removed

- [SafeMath.add(uint256,uint256)](solidity/test_safe_math_lib.sol#L561-L566) is never used and should be removed

- [Math.log10(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L397-L407) is never used and should be removed

- [SafeMath.tryMod(uint256,uint256)](solidity/test_safe_math_lib.sol#L539-L549) is never used and should be removed

- [Math.mulDiv(uint256,uint256,uint256)](solidity/test_safe_math_lib.sol#L141-L226) is never used and should be removed

- [SafeMath.sub(uint256,uint256,string)](solidity/test_safe_math_lib.sol#L651-L660) is never used and should be removed

- [Math.tryDiv(uint256,uint256)](solidity/test_safe_math_lib.sol#L72-L80) is never used and should be removed

- [Math.sqrt(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L285-L295) is never used and should be removed

- [Math.max(uint256,uint256)](solidity/test_safe_math_lib.sol#L100-L102) is never used and should be removed

- [Math.log2(uint256)](solidity/test_safe_math_lib.sol#L301-L337) is never used and should be removed

- [Math.average(uint256,uint256)](solidity/test_safe_math_lib.sol#L115-L118) is never used and should be removed

- [Math.log2(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L343-L353) is never used and should be removed

- [Math.log256(uint256)](solidity/test_safe_math_lib.sol#L415-L439) is never used and should be removed

- [SafeMath.tryAdd(uint256,uint256)](solidity/test_safe_math_lib.sol#L464-L473) is never used and should be removed

- [SafeMath.mod(uint256,uint256,string)](solidity/test_safe_math_lib.sol#L700-L709) is never used and should be removed

- [Math.log256(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L445-L455) is never used and should be removed

- [Math.sqrt(uint256)](solidity/test_safe_math_lib.sol#L249-L280) is never used and should be removed

- [SafeMath.div(uint256,uint256,string)](solidity/test_safe_math_lib.sol#L674-L683) is never used and should be removed

- [Math.tryAdd(uint256,uint256)](solidity/test_safe_math_lib.sol#L21-L30) is never used and should be removed

- [Math.mulDiv(uint256,uint256,uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L231-L242) is never used and should be removed

- [Math.log10(uint256)](solidity/test_safe_math_lib.sol#L359-L391) is never used and should be removed

- [SafeMath.mod(uint256,uint256)](solidity/test_safe_math_lib.sol#L631-L636) is never used and should be removed

- [SafeMath.div(uint256,uint256)](solidity/test_safe_math_lib.sol#L612-L617) is never used and should be removed

- [SafeMath.tryMul(uint256,uint256)](solidity/test_safe_math_lib.sol#L497-L515) is never used and should be removed

- [SafeMath.trySub(uint256,uint256)](solidity/test_safe_math_lib.sol#L480-L490) is never used and should be removed

- [Math.trySub(uint256,uint256)](solidity/test_safe_math_lib.sol#L37-L45) is never used and should be removed

- [Math.tryMul(uint256,uint256)](solidity/test_safe_math_lib.sol#L52-L65) is never used and should be removed

- [Math.tryMod(uint256,uint256)](solidity/test_safe_math_lib.sol#L87-L95) is never used and should be removed

- [Math.min(uint256,uint256)](solidity/test_safe_math_lib.sol#L107-L109) is never used and should be removed

#### Exploit scenario

```solidity
contract Contract{
    function dead_code() internal() {}
}
```
`dead_code` is not used in the contract, and make the code's review more difficult.

### recommendation:
Remove unused functions.

### location:
- solidity/test_safe_math_lib.sol#L595-L600
- solidity/test_safe_math_lib.sol#L578-L583
- solidity/test_safe_math_lib.sol#L522-L532
- solidity/test_safe_math_lib.sol#L126-L134
- solidity/test_safe_math_lib.sol#L561-L566
- solidity/test_safe_math_lib.sol#L397-L407
- solidity/test_safe_math_lib.sol#L539-L549
- solidity/test_safe_math_lib.sol#L141-L226
- solidity/test_safe_math_lib.sol#L651-L660
- solidity/test_safe_math_lib.sol#L72-L80
- solidity/test_safe_math_lib.sol#L285-L295
- solidity/test_safe_math_lib.sol#L100-L102
- solidity/test_safe_math_lib.sol#L301-L337
- solidity/test_safe_math_lib.sol#L115-L118
- solidity/test_safe_math_lib.sol#L343-L353
- solidity/test_safe_math_lib.sol#L415-L439
- solidity/test_safe_math_lib.sol#L464-L473
- solidity/test_safe_math_lib.sol#L700-L709
- solidity/test_safe_math_lib.sol#L445-L455
- solidity/test_safe_math_lib.sol#L249-L280
- solidity/test_safe_math_lib.sol#L674-L683
- solidity/test_safe_math_lib.sol#L21-L30
- solidity/test_safe_math_lib.sol#L231-L242
- solidity/test_safe_math_lib.sol#L359-L391
- solidity/test_safe_math_lib.sol#L631-L636
- solidity/test_safe_math_lib.sol#L612-L617
- solidity/test_safe_math_lib.sol#L497-L515
- solidity/test_safe_math_lib.sol#L480-L490
- solidity/test_safe_math_lib.sol#L37-L45
- solidity/test_safe_math_lib.sol#L52-L65
- solidity/test_safe_math_lib.sol#L87-L95
- solidity/test_safe_math_lib.sol#L107-L109

### severity:
Informational

### category:
dead-code

## [Optimization] Using `x >> constant(uint)` with the right shift operator is a more gas-efficient

### description:

`<x> / 2` is the same as `<x> >> 1`. While the compiler uses the `SHR` opcode to accomplish both, the version that uses division incurs an overhead of [**20 gas**](https://gist.github.com/0xxfu/84e3727f28e01f9b628836d5bf55d0cc) due to `JUMP`s to and from a compiler utility function that introduces checks which can be avoided by using `unchecked {}` around the division by two



**There is `1` instance of this issue:**

- [(a & b) + (a ^ b) / 2](solidity/test_safe_math_lib.sol#L117) should use right shift `>>` operator to save gas.


### recommendation:

Using bit shifting (`>>` operator) replace division divided by constant.


### location:
- solidity/test_safe_math_lib.sol#L117

### severity:
Optimization

### category:
divide-by-constant

## [Optimization] `internal` functions only called once can be inlined to save gas

### description:

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There are `6` instances of this issue:**

- [Math.mulDiv(uint256,uint256,uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L231-L242) could be inlined to save gas
- [Math.log2(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L343-L353) could be inlined to save gas
- [Math.log10(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L397-L407) could be inlined to save gas
- [Math.min(uint256,uint256)](solidity/test_safe_math_lib.sol#L107-L109) could be inlined to save gas
- [Math.sqrt(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L285-L295) could be inlined to save gas
- [Math.log256(uint256,Math.Rounding)](solidity/test_safe_math_lib.sol#L445-L455) could be inlined to save gas

### recommendation:
Using inlining replace `internal` function which only called once

### location:
- solidity/test_safe_math_lib.sol#L231-L242
- solidity/test_safe_math_lib.sol#L343-L353
- solidity/test_safe_math_lib.sol#L397-L407
- solidity/test_safe_math_lib.sol#L107-L109
- solidity/test_safe_math_lib.sol#L285-L295
- solidity/test_safe_math_lib.sol#L445-L455

### severity:
Optimization

### category:
internal-function-to-inline

## [Optimization] Don't use `SafeMath` if use solidity version `>=0.8.0`

### description:

Version `>=0.8.0` introduces internal overflow checks, using `SafeMath` function calls will be more expensive than just built in arithmetic, so using SafeMath is redundant and adds overhead.

More detail see [Solidity 0.8.0 Release Announcement][https://blog.soliditylang.org/2020/12/16/solidity-v0.8.0-release-announcement/#:~:text=the%20full%20list!-,Checked%20Arithmetic,-The%20%E2%80%9CChecked%20Arithmetic] and [OpenZeppelin discussion](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/2465)


**There is `1` instance of this issue:**

- `SafeMath` used in [SafeMathLib](solidity/test_safe_math_lib.sol#L712-L717) should be removed

### recommendation:

Remove `SafeMath` lib.


### location:
- solidity/test_safe_math_lib.sol#L712-L717

### severity:
Optimization

### category:
safe-math-lib

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [SafeMathLib.stateInt](solidity/test_safe_math_lib.sol#L716) is never used.

### recommendation:

Remove or replace the unused state variables


### location:
- solidity/test_safe_math_lib.sol#L716

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] Reduce gas usage by moving to Solidity 0.8.19 or later

### description:
See this [link](https://blog.soliditylang.org/2023/02/22/solidity-0.8.19-release-announcement/#preventing-dead-code-in-runtime-bytecode) for the full details

**There is `1` instance of this issue:**

- pragma solidity version [^0.8.9](solidity/test_safe_math_lib.sol#L2) should upgrade to the latest version: 0.8.19

### recommendation:
Upgrade solidity version to the latest version: 0.8.19

### location:
- solidity/test_safe_math_lib.sol#L2

### severity:
Optimization

### category:
upgrade-to-latest

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `8` instances of this issue:**

- [require(bool,string)(b <= a,errorMessage)](solidity/test_safe_math_lib.sol#L657) should use custom error to save gas.

- [require(bool,string)(c >= a,SafeMath: addition overflow)](solidity/test_safe_math_lib.sol#L564) should use custom error to save gas.

- [require(bool,string)(c / a == b,SafeMath: multiplication overflow)](solidity/test_safe_math_lib.sol#L598) should use custom error to save gas.

- [require(bool,string)(b <= a,SafeMath: subtraction overflow)](solidity/test_safe_math_lib.sol#L580) should use custom error to save gas.

- [require(bool,string)(b > 0,errorMessage)](solidity/test_safe_math_lib.sol#L680) should use custom error to save gas.

- [require(bool,string)(b > 0,SafeMath: modulo by zero)](solidity/test_safe_math_lib.sol#L633) should use custom error to save gas.

- [require(bool,string)(b > 0,errorMessage)](solidity/test_safe_math_lib.sol#L706) should use custom error to save gas.

- [require(bool,string)(b > 0,SafeMath: division by zero)](solidity/test_safe_math_lib.sol#L614) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### location:
- solidity/test_safe_math_lib.sol#L657
- solidity/test_safe_math_lib.sol#L564
- solidity/test_safe_math_lib.sol#L598
- solidity/test_safe_math_lib.sol#L580
- solidity/test_safe_math_lib.sol#L680
- solidity/test_safe_math_lib.sol#L633
- solidity/test_safe_math_lib.sol#L706
- solidity/test_safe_math_lib.sol#L614

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [SafeMathLib.stateInt](solidity/test_safe_math_lib.sol#L716) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### location:
- solidity/test_safe_math_lib.sol#L716

### severity:
Optimization

### category:
constable-states
