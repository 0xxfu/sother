## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | The owner is a single point of failure and a centralization risk | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Events are missing sender information | 2 |
| [L-1] | Missing Event Setter | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use indexed events for value types as they are less costly compared to non-indexed ones | 3 |
| [G-1] | Functions guaranteed to revert when called by normal users can be marked `payable` | 1 |



## [Medium] The owner is a single point of failure and a centralization risk

### description

Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.


**There is `1` instance of this issue:**

- The role [MissingSenderInEvents.onlyOwner()](solidity/tmp/test_missing_sender_in_events.sol#L5-L7) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [MissingSenderInEvents.notBad3(uint256,address)](solidity/tmp/test_missing_sender_in_events.sol#L29-L31)


### recommendation

Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.


### locations
- solidity/tmp/test_missing_sender_in_events.sol#L5-L7

### severity
Medium

### category
owner-centralization

### confidence
High

## [Low] Events are missing sender information

### description

When an action is triggered based on a user's action, not being able to filter based on 
who triggered the action makes event processing a lot more cumbersome. 
Including the `msg.sender` the events of these types of action will make events much more 
useful to end users.



**There are `2` instances of this issue:**

- [BadEvent(a)](solidity/tmp/test_missing_sender_in_events.sol#L14) should add `msg.sender` to event.

- [BadEvent(user,a)](solidity/tmp/test_missing_sender_in_events.sol#L18) should add `msg.sender` to event.


### recommendation

Adding `msg.sender` to event.


### locations
- solidity/tmp/test_missing_sender_in_events.sol#L14
- solidity/tmp/test_missing_sender_in_events.sol#L18

### severity
Low

### category
missing-sender-in-event

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There is `1` instance of this issue:**

- Setter function [MissingSenderInEvents._msgSender()](solidity/tmp/test_missing_sender_in_events.sol#L9-L11) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_missing_sender_in_events.sol#L9-L11

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

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `3` instances of this issue:**

- The following variables should be indexed in [MissingSenderInEvents.BadEvent(uint256)](solidity/tmp/test_missing_sender_in_events.sol#L2):

	- [x](solidity/tmp/test_missing_sender_in_events.sol#L2)

- The following variables should be indexed in [MissingSenderInEvents.BadEvent(address,uint256)](solidity/tmp/test_missing_sender_in_events.sol#L3):

	- [a](solidity/tmp/test_missing_sender_in_events.sol#L3)

	- [x](solidity/tmp/test_missing_sender_in_events.sol#L3)

- The following variables should be indexed in [MissingSenderInEvents.NotBadEvent(address,uint256)](solidity/tmp/test_missing_sender_in_events.sol#L4):

	- [x](solidity/tmp/test_missing_sender_in_events.sol#L4)

	- [sender](solidity/tmp/test_missing_sender_in_events.sol#L4)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_missing_sender_in_events.sol#L2
- solidity/tmp/test_missing_sender_in_events.sol#L3
- solidity/tmp/test_missing_sender_in_events.sol#L4

### severity
Optimization

### category
unindexed-event

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


**There is `1` instance of this issue:**

- [MissingSenderInEvents.notBad3(uint256,address)](solidity/tmp/test_missing_sender_in_events.sol#L29-L31) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/tmp/test_missing_sender_in_events.sol#L29-L31

### severity
Optimization

### category
payable-function

### confidence
High
