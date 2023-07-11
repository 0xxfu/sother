## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Events are missing sender information | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Functions guaranteed to revert when called by normal users can be marked `payable` | 1 |
| [G-1] | Use indexed events for value types as they are less costly compared to non-indexed ones | 3 |



## [Low] Events are missing sender information

### description:

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There are `2` instances of this issue:**

- [BadEvent(a)](solidity/test_missing_sender_in_events.sol#L14) should add `msg.sender` to event.

- [BadEvent(user,a)](solidity/test_missing_sender_in_events.sol#L18) should add `msg.sender` to event.


### recommendation:

Adding `msg.sender` to event.


### locations:
- solidity/test_missing_sender_in_events.sol#L14
- solidity/test_missing_sender_in_events.sol#L18

### severity:
Low

### category:
missing-sender-in-event

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

## [Optimization] Functions guaranteed to revert when called by normal users can be marked `payable`

### description:

If a function modifier such as `onlyOwner/onlyAdmin/only**` is used, 
the function will revert if a normal user tries to pay the function. 
Marking the function as payable will lower the gas cost for legitimate callers 
because the compiler will not include checks for whether a payment was provided. 

The extra opcodes avoided are `CALLVALUE(2)`,`DUP1(3)`,`ISZERO(3)`,`PUSH2(3)`,
`JUMPI(10)`,`PUSH1(3)`,`DUP1(3)`,`REVERT(0)`,`JUMPDEST(1)`,`POP(2)`, 
which costs an average of about `21 gas` per call to the function, 
in addition to the extra deployment cost


**There is `1` instance of this issue:**

- [MissingSenderInEvents.notBad3(uint256,address)](solidity/test_missing_sender_in_events.sol#L29-L31) should be set to `payable` 


### recommendation:

Set the function to `payable`.


### locations:
- solidity/test_missing_sender_in_events.sol#L29-L31

### severity:
Optimization

### category:
payable-function

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description:

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `3` instances of this issue:**

- The following variables should be indexed in [MissingSenderInEvents.BadEvent(uint256)](solidity/test_missing_sender_in_events.sol#L2):

	- [x](solidity/test_missing_sender_in_events.sol#L2)

- The following variables should be indexed in [MissingSenderInEvents.BadEvent(address,uint256)](solidity/test_missing_sender_in_events.sol#L3):

	- [a](solidity/test_missing_sender_in_events.sol#L3)

	- [x](solidity/test_missing_sender_in_events.sol#L3)

- The following variables should be indexed in [MissingSenderInEvents.NotBadEvent(address,uint256)](solidity/test_missing_sender_in_events.sol#L4):

	- [x](solidity/test_missing_sender_in_events.sol#L4)

	- [sender](solidity/test_missing_sender_in_events.sol#L4)


### recommendation:

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations:
- solidity/test_missing_sender_in_events.sol#L2
- solidity/test_missing_sender_in_events.sol#L3
- solidity/test_missing_sender_in_events.sol#L4

### severity:
Optimization

### category:
unindexed-event
