## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `abi.encodePacked()` should not be used with dynamic types when passing the result to a hash function such as `keccak256()` | 5 |
| [L-1] | Local variable shadowing | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 5 |
| [N-2] | Unused state variable | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 3 |
| [G-1] | State variables that could be declared constant | 4 |



## [Low] `abi.encodePacked()` should not be used with dynamic types when passing the result to a hash function such as `keccak256()`

### description:

Use `abi.encode()` instead which will pad items to 32 bytes, which will 
[prevent hash collisions](https://docs.soliditylang.org/en/v0.8.13/abi-spec.html#non-standard-packed-mode) 
(e.g. `abi.encodePacked(0x123,0x456)` => `0x123456` => `abi.encodePacked(0x1,0x23456)`, 
but `abi.encode(0x123,0x456)` => `0x0...1230...456`). "Unless there is a compelling reason, 
`abi.encode` should be preferred". If there is only one argument to `abi.encodePacked()` 
it can often be cast to `bytes()` or `bytes32()` [instead](https://ethereum.stackexchange.com/questions/30912/how-to-compare-strings-in-solidity#answer-82739).

There is also discussion of [removing abi.encodePacked from future versions of Solidity](https://github.com/ethereum/solidity/issues/11593),
so using `abi.encode` now will ensure compatibility in the future.


**There are `5` instances of this issue:**

- [ABIencodePacked.bad0(string,string)](solidity/encode_packed_collision.sol#L14-L16) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,strb)](solidity/encode_packed_collision.sol#L15)

- [ABIencodePacked.bad1(string,bytes)](solidity/encode_packed_collision.sol#L19-L21) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,bytesa)](solidity/encode_packed_collision.sol#L20)

- [ABIencodePacked.bad2(string,uint256[])](solidity/encode_packed_collision.sol#L24-L26) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(stra,arra)](solidity/encode_packed_collision.sol#L25)

- [ABIencodePacked.bad3_get_hash_for_signature(string,string)](solidity/encode_packed_collision.sol#L29-L31) calls abi.encodePacked() with multiple dynamic arguments:
	- [keccak256(bytes)(abi.encodePacked(name,doc))](solidity/encode_packed_collision.sol#L30)

- [ABIencodePacked.bad4(bytes,bytes)](solidity/encode_packed_collision.sol#L34-L36) calls abi.encodePacked() with multiple dynamic arguments:
	- [packed = abi.encodePacked(a,a2,a3,a)](solidity/encode_packed_collision.sol#L35)

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


### recommendation:
Do not use more than one dynamic type in `abi.encodePacked()`
    (see the [Solidity documentation](https://docs.soliditylang.org/en/latest/abi-spec.html#non-standard-packed-mode)). 
    Use `abi.encode()`, preferably.

### locations:
- solidity/encode_packed_collision.sol#L14-L16
- solidity/encode_packed_collision.sol#L19-L21
- solidity/encode_packed_collision.sol#L24-L26
- solidity/encode_packed_collision.sol#L29-L31
- solidity/encode_packed_collision.sol#L34-L36

### severity:
Low

### category:
encode-packed-collision

## [Low] Local variable shadowing

### description:
Detection of shadowing using local variables.

**There is `1` instance of this issue:**

- [ABIencodePacked.good7(string,uint256,string).a](solidity/encode_packed_collision.sol#L74) shadows:
	- [ABIencodePacked.a](solidity/encode_packed_collision.sol#L3) (state variable)

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

### recommendation:
Rename the local variables that shadow another component.

### locations:
- solidity/encode_packed_collision.sol#L74

### severity:
Low

### category:
shadowing-local

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

**There are `5` instances of this issue:**

- Variable [ABIencodePacked._bytes](solidity/encode_packed_collision.sol#L6) is not in mixedCase

- Variable [ABIencodePacked.str_arr3](solidity/encode_packed_collision.sol#L9) is not in mixedCase

- Variable [ABIencodePacked.str_array](solidity/encode_packed_collision.sol#L10) is not in mixedCase

- Variable [ABIencodePacked.bytes_array](solidity/encode_packed_collision.sol#L11) is not in mixedCase

- Function [ABIencodePacked.bad3_get_hash_for_signature(string,string)](solidity/encode_packed_collision.sol#L29-L31) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/encode_packed_collision.sol#L6
- solidity/encode_packed_collision.sol#L9
- solidity/encode_packed_collision.sol#L10
- solidity/encode_packed_collision.sol#L11
- solidity/encode_packed_collision.sol#L29-L31

### severity:
Informational

### category:
naming-convention

## [Informational] Unused state variable

### description:
Unused state variable.

**There are `3` instances of this issue:**

- [ABIencodePacked.str_arr3](solidity/encode_packed_collision.sol#L9) is never used in [ABIencodePacked](solidity/encode_packed_collision.sol#L1-L77)

- [ABIencodePacked.str_array](solidity/encode_packed_collision.sol#L10) is never used in [ABIencodePacked](solidity/encode_packed_collision.sol#L1-L77)

- [ABIencodePacked.bytes_array](solidity/encode_packed_collision.sol#L11) is never used in [ABIencodePacked](solidity/encode_packed_collision.sol#L1-L77)


### recommendation:
Remove unused state variables.

### locations:
- solidity/encode_packed_collision.sol#L9
- solidity/encode_packed_collision.sol#L10
- solidity/encode_packed_collision.sol#L11

### severity:
Informational

### category:
unused-state

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There are `3` instances of this issue:**

- [ABIencodePacked.str_arr3](solidity/encode_packed_collision.sol#L9) is never used.
- [ABIencodePacked.str_array](solidity/encode_packed_collision.sol#L10) is never used.
- [ABIencodePacked.bytes_array](solidity/encode_packed_collision.sol#L11) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/encode_packed_collision.sol#L9
- solidity/encode_packed_collision.sol#L10
- solidity/encode_packed_collision.sol#L11

### severity:
Optimization

### category:
unused-state-variables

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `4` instances of this issue:**

- [ABIencodePacked.a](solidity/encode_packed_collision.sol#L3) should be constant 

- [ABIencodePacked.str1](solidity/encode_packed_collision.sol#L4) should be constant 

- [ABIencodePacked.str2](solidity/encode_packed_collision.sol#L5) should be constant 

- [ABIencodePacked._bytes](solidity/encode_packed_collision.sol#L6) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/encode_packed_collision.sol#L3
- solidity/encode_packed_collision.sol#L4
- solidity/encode_packed_collision.sol#L5
- solidity/encode_packed_collision.sol#L6

### severity:
Optimization

### category:
constable-states