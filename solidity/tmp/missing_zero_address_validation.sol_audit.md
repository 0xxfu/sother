## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 2 |
| [L-1] | Missing zero address validation | 2 |
| [L-2] | Missing events access control | 3 |
| [L-3] | Missing Event Setter | 10 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 2 |
| [N-2] | Unnecessary Public Function Modifier | 1 |
| [N-3] | Unused events | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 1 |
| [G-1] | Using custom errors replace `require` or `assert` | 1 |
| [G-2] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-3] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-4] | Use assembly to check for `address(0)` | 1 |
| [G-5] | Functions guaranteed to revert when called by normal users can be marked `payable` | 8 |
| [G-6] | Use `assembly` to write address storage values | 7 |
| [G-7] | State variables that could be declared constant | 1 |
| [G-8] | State variables that could be declared constant | 1 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There is `1` instance of this issue:**

- good0(uint256) has possible integer overflow/underflow:
	- [totalSupply += a](solidity/tmp/missing_zero_address_validation.sol#L29)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/missing_zero_address_validation.sol#L29

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `2` instances of this issue:**

- [Bug.good0(uint256).a](solidity/tmp/missing_zero_address_validation.sol#L28) lacks an upper limit check on :
	- [totalSupply += a](solidity/tmp/missing_zero_address_validation.sol#L29)

- [Bug.good4(uint256).newPrice](solidity/tmp/missing_zero_address_validation.sol#L45) lacks an upper limit check on :
	- [price = newPrice](solidity/tmp/missing_zero_address_validation.sol#L46)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/missing_zero_address_validation.sol#L28
- solidity/tmp/missing_zero_address_validation.sol#L45

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Missing zero address validation

### description
Missing zero address validation.

**There are `2` instances of this issue:**

- [Bug.bad1(address).newOwner](solidity/tmp/missing_zero_address_validation.sol#L19) lacks a zero-check on :
		- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L20)

- [Bug.good5(address).newOwner](solidity/tmp/missing_zero_address_validation.sol#L49) lacks a zero-check on :
		- [operator = newOwner](solidity/tmp/missing_zero_address_validation.sol#L50)

#### Exploit scenario

```solidity
contract C {

  modifier onlyAdmin {
    if (msg.sender != owner) throw;
    _;
  }

  function updateOwner(address newOwner) onlyAdmin external {
    owner = newOwner;
  }
}
```
Bob calls `updateOwner` without specifying the `newOwner`, so Bob loses ownership of the contract.


### recommendation
Check that the address is not zero.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L19
- solidity/tmp/missing_zero_address_validation.sol#L49

### severity
Low

### category
missing-zero-check

### confidence
Medium

## [Low] Missing events access control

### description
Detect missing events for critical access control parameters

**There are `3` instances of this issue:**

- [Bug.bad0()](solidity/tmp/missing_zero_address_validation.sol#L15-L17) should emit an event for: 
	- [owner = msg.sender](solidity/tmp/missing_zero_address_validation.sol#L16) 

- [Bug.bad1(address)](solidity/tmp/missing_zero_address_validation.sol#L19-L21) should emit an event for: 
	- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L20) 

- [Bug.bad2(address)](solidity/tmp/missing_zero_address_validation.sol#L23-L26) should emit an event for: 
	- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L25) 

#### Exploit scenario

```solidity
contract C {

  modifier onlyAdmin {
    if (msg.sender != owner) throw;
    _;
  }

  function updateOwner(address newOwner) onlyAdmin external {
    owner = newOwner;
  }
}
```
`updateOwner()` has no event, so it is difficult to track off-chain owner changes.


### recommendation
Emit an event for critical parameter changes.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L15-L17
- solidity/tmp/missing_zero_address_validation.sol#L19-L21
- solidity/tmp/missing_zero_address_validation.sol#L23-L26

### severity
Low

### category
events-access

### confidence
Medium

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `10` instances of this issue:**

- Setter function [Bug.slitherConstructorVariables()](solidity/tmp/missing_zero_address_validation.sol#L1-L52) does not emit an event

- Setter function [Bug.onlyAdmin()](solidity/tmp/missing_zero_address_validation.sol#L10-L13) does not emit an event

- Setter function [Bug.bad0()](solidity/tmp/missing_zero_address_validation.sol#L15-L17) does not emit an event

- Setter function [Bug.bad1(address)](solidity/tmp/missing_zero_address_validation.sol#L19-L21) does not emit an event

- Setter function [Bug.bad2(address)](solidity/tmp/missing_zero_address_validation.sol#L23-L26) does not emit an event

- Setter function [Bug.good0(uint256)](solidity/tmp/missing_zero_address_validation.sol#L28-L30) does not emit an event

- Setter function [Bug.good2()](solidity/tmp/missing_zero_address_validation.sol#L37-L39) does not emit an event

- Setter function [Bug.good3(address)](solidity/tmp/missing_zero_address_validation.sol#L41-L43) does not emit an event

- Setter function [Bug.good4(uint256)](solidity/tmp/missing_zero_address_validation.sol#L45-L47) does not emit an event

- Setter function [Bug.good5(address)](solidity/tmp/missing_zero_address_validation.sol#L49-L51) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/missing_zero_address_validation.sol#L1-L52
- solidity/tmp/missing_zero_address_validation.sol#L10-L13
- solidity/tmp/missing_zero_address_validation.sol#L15-L17
- solidity/tmp/missing_zero_address_validation.sol#L19-L21
- solidity/tmp/missing_zero_address_validation.sol#L23-L26
- solidity/tmp/missing_zero_address_validation.sol#L28-L30
- solidity/tmp/missing_zero_address_validation.sol#L37-L39
- solidity/tmp/missing_zero_address_validation.sol#L41-L43
- solidity/tmp/missing_zero_address_validation.sol#L45-L47
- solidity/tmp/missing_zero_address_validation.sol#L49-L51

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

## [Informational] ..

### description
..

**There are `2` instances of this issue:**

- require() missing error messages
	 - [require(bool)(msg.sender != owner)](solidity/tmp/missing_zero_address_validation.sol#L11)

- require() missing error messages
	 - [require(bool)(newOwner != address(0))](solidity/tmp/missing_zero_address_validation.sol#L24)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/missing_zero_address_validation.sol#L11
- solidity/tmp/missing_zero_address_validation.sol#L24

### severity
Informational

### category
error-msg

### confidence
Medium

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There is `1` instance of this issue:**

- function:[Bug.good4(uint256)](solidity/tmp/missing_zero_address_validation.sol#L45-L47)is public and can be replaced with external 

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
- solidity/tmp/missing_zero_address_validation.sol#L45-L47

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Informational] Unused events

### description
The event is declared but never emitted.

**There is `1` instance of this issue:**

- [Bug.Supply(uint256)](solidity/tmp/missing_zero_address_validation.sol#L7) is never emitted in [Bug](solidity/tmp/missing_zero_address_validation.sol#L1-L52)

#### Exploit scenario

    // SPDX-License-Identifier: GPL-3.0
    pragma solidity ^0.8.4;

    contract Coin {
        
        address public minter;
        mapping (address => uint) public balances;

        event Sent(address from, address to, uint amount);

        constructor() {
            minter = msg.sender;
        }
        
        function mint(address receiver, uint amount) public {
            require(msg.sender == minter);
            balances[receiver] += amount;
        }
    
        error InsufficientBalance(uint requested, uint available);

        function send(address receiver, uint amount) public {
            if (amount > balances[msg.sender])
                revert InsufficientBalance({
                    requested: amount,
                    available: balances[msg.sender]
                });

            balances[msg.sender] -= amount;
            balances[receiver] += amount;
            //emit Sent(msg.sender, receiver, amount);
        }
    }
    

### recommendation
We recommend removing these events or emitting them in the right places.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L7

### severity
Informational

### category
unused-event

### confidence
High

## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There is `1` instance of this issue:**

- should use arithmetic operator `=` replace `+=` in [totalSupply += a](solidity/tmp/missing_zero_address_validation.sol#L29)

### recommendation
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### locations
- solidity/tmp/missing_zero_address_validation.sol#L29

### severity
Optimization

### category
assignment-left-operation

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool)(newOwner != address(0))](solidity/tmp/missing_zero_address_validation.sol#L24) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/missing_zero_address_validation.sol#L24

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [Bug.good3(address)](solidity/tmp/missing_zero_address_validation.sol#L41-L43) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L41-L43

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [Bug.Supply(uint256)](solidity/tmp/missing_zero_address_validation.sol#L7):

	- [totalSupply](solidity/tmp/missing_zero_address_validation.sol#L7)

- The following variables should be indexed in [Bug.Owner(address)](solidity/tmp/missing_zero_address_validation.sol#L8):

	- [owner](solidity/tmp/missing_zero_address_validation.sol#L8)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/missing_zero_address_validation.sol#L7
- solidity/tmp/missing_zero_address_validation.sol#L8

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There is `1` instance of this issue:**

- [require(bool)(newOwner != address(0))](solidity/tmp/missing_zero_address_validation.sol#L24) should use assembly to check for `address(0)`


### recommendation

Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```


### locations
- solidity/tmp/missing_zero_address_validation.sol#L24

### severity
Optimization

### category
zero-address-optimization

### confidence
High

## [Optimization] Functions guaranteed to revert when called by normal users can be marked `payable`

### description

If a function modifier such as `onlyOwner/onlyAdmin/only**` is used, 
the function will revert if a normal user tries to pay the function. 
Marking the function as payable will lower the gas cost for legitimate callers 
because the compiler will not include checks for whether a payment was provided. 

The extra opcodes avoided are `CALLVALUE(2)`,`DUP1(3)`,`ISZERO(3)`,`PUSH2(3)`,
`JUMPI(10)`,`PUSH1(3)`,`DUP1(3)`,`REVERT(0)`,`JUMPDEST(1)`,`POP(2)`, 
which costs an average of about `21 gas` per call to the function, 
in addition to the extra deployment cost


**There are `8` instances of this issue:**

- [Bug.bad0()](solidity/tmp/missing_zero_address_validation.sol#L15-L17) should be set to `payable` 

- [Bug.bad1(address)](solidity/tmp/missing_zero_address_validation.sol#L19-L21) should be set to `payable` 

- [Bug.bad2(address)](solidity/tmp/missing_zero_address_validation.sol#L23-L26) should be set to `payable` 

- [Bug.good1()](solidity/tmp/missing_zero_address_validation.sol#L32-L35) should be set to `payable` 

- [Bug.good2()](solidity/tmp/missing_zero_address_validation.sol#L37-L39) should be set to `payable` 

- [Bug.good3(address)](solidity/tmp/missing_zero_address_validation.sol#L41-L43) should be set to `payable` 

- [Bug.good4(uint256)](solidity/tmp/missing_zero_address_validation.sol#L45-L47) should be set to `payable` 

- [Bug.good5(address)](solidity/tmp/missing_zero_address_validation.sol#L49-L51) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/tmp/missing_zero_address_validation.sol#L15-L17
- solidity/tmp/missing_zero_address_validation.sol#L19-L21
- solidity/tmp/missing_zero_address_validation.sol#L23-L26
- solidity/tmp/missing_zero_address_validation.sol#L32-L35
- solidity/tmp/missing_zero_address_validation.sol#L37-L39
- solidity/tmp/missing_zero_address_validation.sol#L41-L43
- solidity/tmp/missing_zero_address_validation.sol#L45-L47
- solidity/tmp/missing_zero_address_validation.sol#L49-L51

### severity
Optimization

### category
payable-function

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There are `7` instances of this issue:**

- [owner = msg.sender](solidity/tmp/missing_zero_address_validation.sol#L16) should use `assembly` update address to save gas.

- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L20) should use `assembly` update address to save gas.

- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L25) should use `assembly` update address to save gas.

- [owner = msg.sender](solidity/tmp/missing_zero_address_validation.sol#L33) should use `assembly` update address to save gas.

- [owner = addr](solidity/tmp/missing_zero_address_validation.sol#L38) should use `assembly` update address to save gas.

- [owner = newOwner](solidity/tmp/missing_zero_address_validation.sol#L42) should use `assembly` update address to save gas.

- [operator = newOwner](solidity/tmp/missing_zero_address_validation.sol#L50) should use `assembly` update address to save gas.


### recommendation

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations
- solidity/tmp/missing_zero_address_validation.sol#L16
- solidity/tmp/missing_zero_address_validation.sol#L20
- solidity/tmp/missing_zero_address_validation.sol#L25
- solidity/tmp/missing_zero_address_validation.sol#L33
- solidity/tmp/missing_zero_address_validation.sol#L38
- solidity/tmp/missing_zero_address_validation.sol#L42
- solidity/tmp/missing_zero_address_validation.sol#L50

### severity
Optimization

### category
assembly-update-address

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [Bug.addr](solidity/tmp/missing_zero_address_validation.sol#L6) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L6

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [Bug.addr](solidity/tmp/missing_zero_address_validation.sol#L6) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/missing_zero_address_validation.sol#L6

### severity
Optimization

### category
state-should-be-constant

### confidence
High
