## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 3 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `abi.encodePacked()` should not be used with dynamic types when passing the result to a hash function such as `keccak256()` | 5 |
| [L-1] | Local variable shadowing | 1 |
| [L-2] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 5 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 3 |
| [G-1] | Remove unused local variables | 12 |
| [G-2] | Use `string.concat()` on string instead of `abi.encodePacked()` to save gas | 4 |
| [G-3] | Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas | 2 |
| [G-4] | State variables that could be declared constant | 4 |
| [G-5] | State variables that could be declared constant | 4 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There are `3` instances of this issue:**

- state variable: [ABIencodePacked.a](solidity/tmp/encode_packed_collision.sol#L3) not initialized and not written in contract but be used in contract

- state variable: [ABIencodePacked.arr](solidity/tmp/encode_packed_collision.sol#L7) not initialized and not written in contract but be used in contract

- state variable: [ABIencodePacked.arr2](solidity/tmp/encode_packed_collision.sol#L8) not initialized and not written in contract but be used in contract

#### Exploit scenario

```solidity
    struct BalancesStruct{
        address owner;
        array[]] balances;
    }
    array[] public stackBalance;

    function remove() internal{
         delete stackBalance[msg.sender];
    }
```
`remove` deletes an item of `stackBalance`.
The array `balances` is never deleted, so `remove` does not work as intended.

### recommendation
Use a lock mechanism instead of a deletion to disable structure containing a array.

### locations
- solidity/tmp/encode_packed_collision.sol#L3
- solidity/tmp/encode_packed_collision.sol#L7
- solidity/tmp/encode_packed_collision.sol#L8

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Low] `abi.encodePacked()` should not be used with dynamic types when passing the result to a hash function such as `keccak256()`

### description

Use `abi.encode()` instead which will pad items to 32 bytes, which will 
[prevent hash collisions](https://docs.soliditylang.org/en/v0.8.13/abi-spec.html#non-standard-packed-mode) 
(e.g. `abi.encodePacked(0x123,0x456)` => `0x123456` => `abi.encodePacked(0x1,0x23456)`, 
but `abi.encode(0x123,0x456)` => `0x0...1230...456`). "Unless there is a compelling reason, 
`abi.encode` should be preferred". If there is only one argument to `abi.encodePacked()` 
it can often be cast to `bytes()` or `bytes32()` [instead](https://ethereum.stackexchange.com/questions/30912/how-to-compare-strings-in-solidity#answer-82739).

There is also discussion of [removing abi.encodePacked from future versions of Solidity](https://github.com/ethereum/solidity/issues/11593),
so using `abi.encode` now will ensure compatibility in the future.


**There are `5` instances of this issue:**

- [ABIencodePacked.bad0(string,string)](solidity/tmp/encode_packed_collision.sol#L14-L16) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,strb)](solidity/tmp/encode_packed_collision.sol#L15)

- [ABIencodePacked.bad1(string,bytes)](solidity/tmp/encode_packed_collision.sol#L19-L21) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,bytesa)](solidity/tmp/encode_packed_collision.sol#L20)

- [ABIencodePacked.bad2(string,uint256[])](solidity/tmp/encode_packed_collision.sol#L24-L26) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,arra)](solidity/tmp/encode_packed_collision.sol#L25)

- [ABIencodePacked.bad3_get_hash_for_signature(string,string)](solidity/tmp/encode_packed_collision.sol#L29-L31) calls abi.encodePacked() with multiple dynamic arguments:
	- [keccak256(bytes)(abi.encodePacked(name,doc))](solidity/tmp/encode_packed_collision.sol#L30)

- [ABIencodePacked.bad4(bytes,bytes)](solidity/tmp/encode_packed_collision.sol#L34-L36) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(a,a2,a3,a)](solidity/tmp/encode_packed_collision.sol#L35)

#### Exploit scenario

```solidity
contract Sign {
    function get_hash_for_signature(string name, string doc) external returns(bytes32) {
        return keccak256(abi.encodePacked(name, doc));
    }
}
```
Bob calls `get_hash_for_signature` with (`bob`, `This is the content`). The hash returned is used as an ID.
Eve creates a collision with the ID using (`bo`, `bThis is the content`) and compromises the system.


### recommendation

Do not use more than one dynamic type in `abi.encodePacked()` 
(see the [Solidity documentation](https://docs.soliditylang.org/en/latest/abi-spec.html#non-standard-packed-mode)). 
Use `abi.encode()`, preferably.


### locations
- solidity/tmp/encode_packed_collision.sol#L14-L16
- solidity/tmp/encode_packed_collision.sol#L19-L21
- solidity/tmp/encode_packed_collision.sol#L24-L26
- solidity/tmp/encode_packed_collision.sol#L29-L31
- solidity/tmp/encode_packed_collision.sol#L34-L36

### severity
Low

### category
encode-packed-collision

### confidence
High

## [Low] Local variable shadowing

### description
Detection of shadowing using local variables.

**There is `1` instance of this issue:**

- [ABIencodePacked.good7(string,uint256,string).a](solidity/tmp/encode_packed_collision.sol#L74) shadows:
	- [ABIencodePacked.a](solidity/tmp/encode_packed_collision.sol#L3) (state variable)

#### Exploit scenario

```solidity
pragma solidity ^0.4.24;

contract Bug {
    uint owner;

    function sensitive_function(address owner) public {
        // ...
        require(owner == msg.sender);
    }

    function alternate_sensitive_function() public {
        address owner = msg.sender;
        // ...
        require(owner == msg.sender);
    }
}
```
`sensitive_function.owner` shadows `Bug.owner`. As a result, the use of `owner` in `sensitive_function` might be incorrect.

### recommendation
Rename the local variables that shadow another component.

### locations
- solidity/tmp/encode_packed_collision.sol#L74

### severity
Low

### category
shadowing-local

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [ABIencodePacked.slitherConstructorVariables()](solidity/tmp/encode_packed_collision.sol#L1-L77) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/encode_packed_collision.sol#L1-L77

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

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `5` instances of this issue:**

- Variable [ABIencodePacked._bytes](solidity/tmp/encode_packed_collision.sol#L6) is not in mixedCase

- Variable [ABIencodePacked.str_arr3](solidity/tmp/encode_packed_collision.sol#L9) is not in mixedCase

- Variable [ABIencodePacked.str_array](solidity/tmp/encode_packed_collision.sol#L10) is not in mixedCase

- Variable [ABIencodePacked.bytes_array](solidity/tmp/encode_packed_collision.sol#L11) is not in mixedCase

- Function [ABIencodePacked.bad3_get_hash_for_signature(string,string)](solidity/tmp/encode_packed_collision.sol#L29-L31) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/encode_packed_collision.sol#L6
- solidity/tmp/encode_packed_collision.sol#L9
- solidity/tmp/encode_packed_collision.sol#L10
- solidity/tmp/encode_packed_collision.sol#L11
- solidity/tmp/encode_packed_collision.sol#L29-L31

### severity
Informational

### category
naming-convention

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


**There are `3` instances of this issue:**

- [ABIencodePacked.str_arr3](solidity/tmp/encode_packed_collision.sol#L9) is never used.
- [ABIencodePacked.str_array](solidity/tmp/encode_packed_collision.sol#L10) is never used.
- [ABIencodePacked.bytes_array](solidity/tmp/encode_packed_collision.sol#L11) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/encode_packed_collision.sol#L9
- solidity/tmp/encode_packed_collision.sol#L10
- solidity/tmp/encode_packed_collision.sol#L11

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `12` instances of this issue:**

- The local variables in [ABIencodePacked.bad0(string,string)](solidity/tmp/encode_packed_collision.sol#L14-L16) are unused.
	- [ABIencodePacked.bad0(string,string).packed](solidity/tmp/encode_packed_collision.sol#L15)

- The local variables in [ABIencodePacked.bad1(string,bytes)](solidity/tmp/encode_packed_collision.sol#L19-L21) are unused.
	- [ABIencodePacked.bad1(string,bytes).packed](solidity/tmp/encode_packed_collision.sol#L20)

- The local variables in [ABIencodePacked.bad2(string,uint256[])](solidity/tmp/encode_packed_collision.sol#L24-L26) are unused.
	- [ABIencodePacked.bad2(string,uint256[]).packed](solidity/tmp/encode_packed_collision.sol#L25)

- The local variables in [ABIencodePacked.bad4(bytes,bytes)](solidity/tmp/encode_packed_collision.sol#L34-L36) are unused.
	- [ABIencodePacked.bad4(bytes,bytes).packed](solidity/tmp/encode_packed_collision.sol#L35)

- The local variables in [ABIencodePacked.good0()](solidity/tmp/encode_packed_collision.sol#L39-L41) are unused.
	- [ABIencodePacked.good0().packed](solidity/tmp/encode_packed_collision.sol#L40)

- The local variables in [ABIencodePacked.good1()](solidity/tmp/encode_packed_collision.sol#L44-L46) are unused.
	- [ABIencodePacked.good1().packed](solidity/tmp/encode_packed_collision.sol#L45)

- The local variables in [ABIencodePacked.good2()](solidity/tmp/encode_packed_collision.sol#L49-L51) are unused.
	- [ABIencodePacked.good2().packed](solidity/tmp/encode_packed_collision.sol#L50)

- The local variables in [ABIencodePacked.good3()](solidity/tmp/encode_packed_collision.sol#L54-L56) are unused.
	- [ABIencodePacked.good3().packed](solidity/tmp/encode_packed_collision.sol#L55)

- The local variables in [ABIencodePacked.good4()](solidity/tmp/encode_packed_collision.sol#L59-L61) are unused.
	- [ABIencodePacked.good4().packed](solidity/tmp/encode_packed_collision.sol#L60)

- The local variables in [ABIencodePacked.good5()](solidity/tmp/encode_packed_collision.sol#L64-L66) are unused.
	- [ABIencodePacked.good5().packed](solidity/tmp/encode_packed_collision.sol#L65)

- The local variables in [ABIencodePacked.good6()](solidity/tmp/encode_packed_collision.sol#L69-L71) are unused.
	- [ABIencodePacked.good6().packed](solidity/tmp/encode_packed_collision.sol#L70)

- The local variables in [ABIencodePacked.good7(string,uint256,string)](solidity/tmp/encode_packed_collision.sol#L74-L76) are unused.
	- [ABIencodePacked.good7(string,uint256,string).packed](solidity/tmp/encode_packed_collision.sol#L75)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/encode_packed_collision.sol#L14-L16
- solidity/tmp/encode_packed_collision.sol#L19-L21
- solidity/tmp/encode_packed_collision.sol#L24-L26
- solidity/tmp/encode_packed_collision.sol#L34-L36
- solidity/tmp/encode_packed_collision.sol#L39-L41
- solidity/tmp/encode_packed_collision.sol#L44-L46
- solidity/tmp/encode_packed_collision.sol#L49-L51
- solidity/tmp/encode_packed_collision.sol#L54-L56
- solidity/tmp/encode_packed_collision.sol#L59-L61
- solidity/tmp/encode_packed_collision.sol#L64-L66
- solidity/tmp/encode_packed_collision.sol#L69-L71
- solidity/tmp/encode_packed_collision.sol#L74-L76

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] Use `string.concat()` on string instead of `abi.encodePacked()` to save gas

### description

Starting with version 0.8.12, 
Solidity has the `string.concat()` function, 
which allows one to concatenate a list of strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.


**There are `4` instances of this issue:**

- should use `string.concat()` on string instead of [packed = abi.encodePacked(stra,strb)](solidity/tmp/encode_packed_collision.sol#L15)

- should use `string.concat()` on string instead of [keccak256(bytes)(abi.encodePacked(name,doc))](solidity/tmp/encode_packed_collision.sol#L30)

- should use `string.concat()` on string instead of [packed = abi.encodePacked(str1,str2)](solidity/tmp/encode_packed_collision.sol#L40)

- should use `string.concat()` on string instead of [packed = abi.encodePacked(str1)](solidity/tmp/encode_packed_collision.sol#L60)


### recommendation

Use `string.concat()` on string instead of `abi.encodePacked()`


### locations
- solidity/tmp/encode_packed_collision.sol#L15
- solidity/tmp/encode_packed_collision.sol#L30
- solidity/tmp/encode_packed_collision.sol#L40
- solidity/tmp/encode_packed_collision.sol#L60

### severity
Optimization

### category
use-concat-on-string

### confidence
High

## [Optimization] Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas

### description

Starting with version 0.8.4, 
Solidity has the `bytes.concat()` function, 
which allows one to concatenate a list of bytes/strings, without extra padding. 
Using this function rather than `abi.encodePacked()` makes the intended operation more clear, 
leading to less reviewer confusion and saving more gas.


**There are `2` instances of this issue:**

- should use `bytes.concat()` on mixing bytes and strings instead of  [packed = abi.encodePacked(stra,bytesa)](solidity/tmp/encode_packed_collision.sol#L20)

- should use `bytes.concat()` on mixing bytes and strings instead of  [packed = abi.encodePacked(str1,_bytes)](solidity/tmp/encode_packed_collision.sol#L45)


### recommendation

Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()`


### locations
- solidity/tmp/encode_packed_collision.sol#L20
- solidity/tmp/encode_packed_collision.sol#L45

### severity
Optimization

### category
use-concat-on-bytes

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `4` instances of this issue:**

- [ABIencodePacked.a](solidity/tmp/encode_packed_collision.sol#L3) should be constant 

- [ABIencodePacked.str1](solidity/tmp/encode_packed_collision.sol#L4) should be constant 

- [ABIencodePacked.str2](solidity/tmp/encode_packed_collision.sol#L5) should be constant 

- [ABIencodePacked._bytes](solidity/tmp/encode_packed_collision.sol#L6) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/encode_packed_collision.sol#L3
- solidity/tmp/encode_packed_collision.sol#L4
- solidity/tmp/encode_packed_collision.sol#L5
- solidity/tmp/encode_packed_collision.sol#L6

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `4` instances of this issue:**

- [ABIencodePacked.a](solidity/tmp/encode_packed_collision.sol#L3) should be constant

- [ABIencodePacked.str1](solidity/tmp/encode_packed_collision.sol#L4) should be constant

- [ABIencodePacked.str2](solidity/tmp/encode_packed_collision.sol#L5) should be constant

- [ABIencodePacked._bytes](solidity/tmp/encode_packed_collision.sol#L6) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/encode_packed_collision.sol#L3
- solidity/tmp/encode_packed_collision.sol#L4
- solidity/tmp/encode_packed_collision.sol#L5
- solidity/tmp/encode_packed_collision.sol#L6

### severity
Optimization

### category
state-should-be-constant

### confidence
High
