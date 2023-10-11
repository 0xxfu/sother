## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Events are missing sender information | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unused events | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused struct declaration | 1 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 6 |



## [Low] Events are missing sender information

### description

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There are `12` instances of this issue:**

- [IntEvent(1)](solidity/tmp/test_indexed_event.sol#L45) should add `msg.sender` to event.

- [IndexedIntEvent(1)](solidity/tmp/test_indexed_event.sol#L50) should add `msg.sender` to event.

- [IntsEvent(1,1,1)](solidity/tmp/test_indexed_event.sol#L55) should add `msg.sender` to event.

- [IndexedIntsEvent(1,1,1)](solidity/tmp/test_indexed_event.sol#L60) should add `msg.sender` to event.

- [BoolEvent(true)](solidity/tmp/test_indexed_event.sol#L75) should add `msg.sender` to event.

- [IndexedBoolEvent(true)](solidity/tmp/test_indexed_event.sol#L80) should add `msg.sender` to event.

- [BytesEvent("hello")](solidity/tmp/test_indexed_event.sol#L85) should add `msg.sender` to event.

- [IndexedBytesEvent("hello")](solidity/tmp/test_indexed_event.sol#L90) should add `msg.sender` to event.

- [StrEvent("hello")](solidity/tmp/test_indexed_event.sol#L95) should add `msg.sender` to event.

- [IndexedStrEvent("hello")](solidity/tmp/test_indexed_event.sol#L100) should add `msg.sender` to event.

- [StructEvent(ABC({x:1}))](solidity/tmp/test_indexed_event.sol#L105) should add `msg.sender` to event.

- [IndexedStructEvent(ABC({x:1}))](solidity/tmp/test_indexed_event.sol#L110) should add `msg.sender` to event.


### recommendation

Adding `msg.sender` to event.


### locations
- solidity/tmp/test_indexed_event.sol#L45
- solidity/tmp/test_indexed_event.sol#L50
- solidity/tmp/test_indexed_event.sol#L55
- solidity/tmp/test_indexed_event.sol#L60
- solidity/tmp/test_indexed_event.sol#L75
- solidity/tmp/test_indexed_event.sol#L80
- solidity/tmp/test_indexed_event.sol#L85
- solidity/tmp/test_indexed_event.sol#L90
- solidity/tmp/test_indexed_event.sol#L95
- solidity/tmp/test_indexed_event.sol#L100
- solidity/tmp/test_indexed_event.sol#L105
- solidity/tmp/test_indexed_event.sol#L110

### severity
Low

### category
missing-sender-in-event

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

## [Informational] Unused events

### description
The event is declared but never emitted.

**There are `3` instances of this issue:**

- [IndexedEvent.IndexedMoreIntsEvent(uint256,uint256,uint256,uint256)](solidity/tmp/test_indexed_event.sol#L14-L19) is never emitted in [IndexedEvent](solidity/tmp/test_indexed_event.sol#L3-L112)

- [IndexedEvent.ArrayEvent(uint256[])](solidity/tmp/test_indexed_event.sol#L40) is never emitted in [IndexedEvent](solidity/tmp/test_indexed_event.sol#L3-L112)

- [IndexedEvent.IndexedArrayEvent(uint256[])](solidity/tmp/test_indexed_event.sol#L41) is never emitted in [IndexedEvent](solidity/tmp/test_indexed_event.sol#L3-L112)

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
- solidity/tmp/test_indexed_event.sol#L14-L19
- solidity/tmp/test_indexed_event.sol#L40
- solidity/tmp/test_indexed_event.sol#L41

### severity
Informational

### category
unused-event

### confidence
High

## [Optimization] Remove unused struct declaration

### description

Unused struct declaration are gas consuming. 
And are a bad code practice. 
Removing those structs can save deployment and improve code quality. 


**There is `1` instance of this issue:**

- The structs declaration in [IndexedEvent](solidity/tmp/test_indexed_event.sol#L3-L112) are unused.
	- [IndexedEvent.ABC](solidity/tmp/test_indexed_event.sol#L33-L35)


### recommendation

Remove unused struct declaration.


### locations
- solidity/tmp/test_indexed_event.sol#L3-L112

### severity
Optimization

### category
unused-struct

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `6` instances of this issue:**

- The following variables should be indexed in [IndexedEvent.IntEvent(uint256)](solidity/tmp/test_indexed_event.sol#L4):

	- [x](solidity/tmp/test_indexed_event.sol#L4)

- The following variables should be indexed in [IndexedEvent.IntsEvent(uint256,uint256,uint256)](solidity/tmp/test_indexed_event.sol#L7):

	- [y](solidity/tmp/test_indexed_event.sol#L7)

	- [z](solidity/tmp/test_indexed_event.sol#L7)

- The following variables should be indexed in [IndexedEvent.AddrEvent(address)](solidity/tmp/test_indexed_event.sol#L21):

	- [x](solidity/tmp/test_indexed_event.sol#L21)

- The following variables should be indexed in [IndexedEvent.BoolEvent(bool)](solidity/tmp/test_indexed_event.sol#L24):

	- [x](solidity/tmp/test_indexed_event.sol#L24)

- The following variables should be indexed in [IndexedEvent.BytesEvent(bytes)](solidity/tmp/test_indexed_event.sol#L27):

	- [x](solidity/tmp/test_indexed_event.sol#L27)

- The following variables should be indexed in [IndexedEvent.StrEvent(string)](solidity/tmp/test_indexed_event.sol#L30):

	- [x](solidity/tmp/test_indexed_event.sol#L30)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_indexed_event.sol#L4
- solidity/tmp/test_indexed_event.sol#L7
- solidity/tmp/test_indexed_event.sol#L21
- solidity/tmp/test_indexed_event.sol#L24
- solidity/tmp/test_indexed_event.sol#L27
- solidity/tmp/test_indexed_event.sol#L30

### severity
Optimization

### category
unindexed-event

### confidence
High
