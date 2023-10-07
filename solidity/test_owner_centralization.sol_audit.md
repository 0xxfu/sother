## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | The owner is a single point of failure and a centralization risk | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Functions guaranteed to revert when called by normal users can be marked `payable` | 4 |
| [G-1] | Empty blocks should be removed or emit something | 4 |
| [G-2] | State variables that could be declared constant | 2 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There are `2` instances of this issue:**

- [Centralization.owner](solidity/test_owner_centralization.sol#L2) is never initialized. It is used in:

- [Centralization.test](solidity/test_owner_centralization.sol#L3) is never initialized. It is used in:

#### Exploit scenario

```solidity
contract Uninitialized{
    address destination;

    function transfer() payable public{
        destination.transfer(msg.value);
    }
}
```
Bob calls `transfer`. As a result, the Ether are sent to the address `0x0` and are lost.


### recommendation

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### locations
- solidity/test_owner_centralization.sol#L2
- solidity/test_owner_centralization.sol#L3

### severity
High

### category
uninitialized-state

### confidence
High

## [Medium] The owner is a single point of failure and a centralization risk

### description

Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.


**There is `1` instance of this issue:**

- The role [Centralization.onlyOwner()](solidity/test_owner_centralization.sol#L9-L12) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [Centralization.bad()](solidity/test_owner_centralization.sol#L19)
	- [Centralization.bad0()](solidity/test_owner_centralization.sol#L21)


### recommendation

Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.


### locations
- solidity/test_owner_centralization.sol#L9-L12

### severity
Medium

### category
owner-centralization

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


**There are `4` instances of this issue:**

- [Centralization.bad()](solidity/test_owner_centralization.sol#L19) should be set to `payable` 

- [Centralization.bad0()](solidity/test_owner_centralization.sol#L21) should be set to `payable` 

- [Centralization.bad2()](solidity/test_owner_centralization.sol#L23) should be set to `payable` 

- [Centralization.notbad()](solidity/test_owner_centralization.sol#L25) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/test_owner_centralization.sol#L19
- solidity/test_owner_centralization.sol#L21
- solidity/test_owner_centralization.sol#L23
- solidity/test_owner_centralization.sol#L25

### severity
Optimization

### category
payable-function

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There are `4` instances of this issue:**

- [Centralization.bad()](solidity/test_owner_centralization.sol#L19) should removed or do something

- [Centralization.bad0()](solidity/test_owner_centralization.sol#L21) should removed or do something

- [Centralization.bad2()](solidity/test_owner_centralization.sol#L23) should removed or do something

- [Centralization.notbad()](solidity/test_owner_centralization.sol#L25) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/test_owner_centralization.sol#L19
- solidity/test_owner_centralization.sol#L21
- solidity/test_owner_centralization.sol#L23
- solidity/test_owner_centralization.sol#L25

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [Centralization.owner](solidity/test_owner_centralization.sol#L2) should be constant 

- [Centralization.test](solidity/test_owner_centralization.sol#L3) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/test_owner_centralization.sol#L2
- solidity/test_owner_centralization.sol#L3

### severity
Optimization

### category
constable-states

### confidence
High
