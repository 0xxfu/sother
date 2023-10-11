## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |
| [H-1] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | The owner is a single point of failure and a centralization risk | 1 |
| [M-1] | Contracts that lock Ether | 3 |
| [M-2] | Void function | 4 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 6 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 4 |
| [G-1] | Setting the constructor to `payable` | 2 |
| [G-2] | Functions guaranteed to revert when called by normal users can be marked `payable` | 2 |
| [G-3] | Empty blocks should be removed or emit something | 4 |
| [G-4] | State variables that could be declared constant | 1 |
| [G-5] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There is `1` instance of this issue:**

- [PayableFunctions.owner](solidity/tmp/test_payable_functions.sol#L18) is never initialized. It is used in:

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
- solidity/tmp/test_payable_functions.sol#L18

### severity
High

### category
uninitialized-state

### confidence
High

## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [PayableFunctions.owner](solidity/tmp/test_payable_functions.sol#L18) not initialized and not written in contract but be used in contract

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
- solidity/tmp/test_payable_functions.sol#L18

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] The owner is a single point of failure and a centralization risk

### description

Having a single EOA as the only owner of contracts is a large centralization risk and a single point of failure. A single private key may be taken in a hack, or the sole holder of the key may become unable to retrieve the key when necessary.

There are several privileged entities that have access to sensitive operations as follows.


**There is `1` instance of this issue:**

- The role [PayableFunctions.onlyOwner()](solidity/tmp/test_payable_functions.sol#L19-L24) is a single point of failure and a centralization risk. and have access to sensitive operations as follows:
	- [PayableFunctions.bad()](solidity/tmp/test_payable_functions.sol#L32)
	- [PayableFunctions.notBad()](solidity/tmp/test_payable_functions.sol#L36)


### recommendation

Add a time lock to critical functions. Admin-only functions that change critical parameters should emit events and have timelocks.
Events allow capturing the changed parameters so that off-chain tools/interfaces can register such changes with timelocks that allow users to evaluate them and consider if they would like to engage/exit based on how they perceive the changes as affecting the trustworthiness of the protocol or profitability of the implemented financial services.

Allow only multi-signature wallets to call the function to reduce the likelihood of an attack.


### locations
- solidity/tmp/test_payable_functions.sol#L19-L24

### severity
Medium

### category
owner-centralization

### confidence
High

## [Medium] Contracts that lock Ether

### description
Contract with a `payable` function, but without a withdrawal capacity.

**There are `3` instances of this issue:**

- Contract locking ether found:
	Contract [NotBadConstructor](solidity/tmp/test_payable_functions.sol#L9-L11) has payable functions:
	 - [NotBadConstructor.constructor(address)](solidity/tmp/test_payable_functions.sol#L10)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract [NotBadConstructor2](solidity/tmp/test_payable_functions.sol#L13-L15) has payable functions:
	 - [NotBadConstructor2.constructor()](solidity/tmp/test_payable_functions.sol#L14)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract [PayableFunctions](solidity/tmp/test_payable_functions.sol#L17-L39) has payable functions:
	 - [PayableFunctions.notBad()](solidity/tmp/test_payable_functions.sol#L36)
	 - [PayableFunctions.notBad2(uint256)](solidity/tmp/test_payable_functions.sol#L38)
	But does not have a function to withdraw the ether

#### Exploit scenario

```solidity
pragma solidity 0.4.24;
contract Locked{
    function receive() payable public{
    }
}
```
Every Ether sent to `Locked` will be lost.

### recommendation
Remove the payable attribute or add a withdraw function.

### locations
- solidity/tmp/test_payable_functions.sol#L9-L11
- solidity/tmp/test_payable_functions.sol#L13-L15
- solidity/tmp/test_payable_functions.sol#L17-L39

### severity
Medium

### category
locked-ether

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There are `4` instances of this issue:**

- function:[PayableFunctions.bad()](solidity/tmp/test_payable_functions.sol#L32)is empty 

- function:[PayableFunctions.bad2(address)](solidity/tmp/test_payable_functions.sol#L34)is empty 

- function:[PayableFunctions.notBad()](solidity/tmp/test_payable_functions.sol#L36)is empty 

- function:[PayableFunctions.notBad2(uint256)](solidity/tmp/test_payable_functions.sol#L38)is empty 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Implement the function

### locations
- solidity/tmp/test_payable_functions.sol#L32
- solidity/tmp/test_payable_functions.sol#L34
- solidity/tmp/test_payable_functions.sol#L36
- solidity/tmp/test_payable_functions.sol#L38

### severity
Medium

### category
void-function

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `6` instances of this issue:**

- Setter function [PayableFunctions.onlyOwner()](solidity/tmp/test_payable_functions.sol#L19-L24) does not emit an event

- Setter function [PayableFunctions.onlyAdmin()](solidity/tmp/test_payable_functions.sol#L25-L30) does not emit an event

- Setter function [PayableFunctions.bad()](solidity/tmp/test_payable_functions.sol#L32) does not emit an event

- Setter function [PayableFunctions.bad2(address)](solidity/tmp/test_payable_functions.sol#L34) does not emit an event

- Setter function [PayableFunctions.notBad()](solidity/tmp/test_payable_functions.sol#L36) does not emit an event

- Setter function [PayableFunctions.notBad2(uint256)](solidity/tmp/test_payable_functions.sol#L38) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_payable_functions.sol#L19-L24
- solidity/tmp/test_payable_functions.sol#L25-L30
- solidity/tmp/test_payable_functions.sol#L32
- solidity/tmp/test_payable_functions.sol#L34
- solidity/tmp/test_payable_functions.sol#L36
- solidity/tmp/test_payable_functions.sol#L38

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

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `4` instances of this issue:**

- The param variables in [BadConstructor.constructor(address)](solidity/tmp/test_payable_functions.sol#L2) are unused.
	- [BadConstructor.constructor(address)._baseImpl](solidity/tmp/test_payable_functions.sol#L2)

- The param variables in [NotBadConstructor.constructor(address)](solidity/tmp/test_payable_functions.sol#L10) are unused.
	- [NotBadConstructor.constructor(address)._baseImpl](solidity/tmp/test_payable_functions.sol#L10)

- The param variables in [PayableFunctions.bad2(address)](solidity/tmp/test_payable_functions.sol#L34) are unused.
	- [PayableFunctions.bad2(address)._addr](solidity/tmp/test_payable_functions.sol#L34)

- The param variables in [PayableFunctions.notBad2(uint256)](solidity/tmp/test_payable_functions.sol#L38) are unused.
	- [PayableFunctions.notBad2(uint256).a](solidity/tmp/test_payable_functions.sol#L38)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_payable_functions.sol#L2
- solidity/tmp/test_payable_functions.sol#L10
- solidity/tmp/test_payable_functions.sol#L34
- solidity/tmp/test_payable_functions.sol#L38

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `2` instances of this issue:**

- [BadConstructor.constructor(address)](solidity/tmp/test_payable_functions.sol#L2) should be set to `payable` 

- [BadConstructor2.constructor()](solidity/tmp/test_payable_functions.sol#L6) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/test_payable_functions.sol#L2
- solidity/tmp/test_payable_functions.sol#L6

### severity
Optimization

### category
payable-constructor

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


**There are `2` instances of this issue:**

- [PayableFunctions.bad()](solidity/tmp/test_payable_functions.sol#L32) should be set to `payable` 

- [PayableFunctions.bad2(address)](solidity/tmp/test_payable_functions.sol#L34) should be set to `payable` 


### recommendation

Set the function to `payable`.


### locations
- solidity/tmp/test_payable_functions.sol#L32
- solidity/tmp/test_payable_functions.sol#L34

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

- [PayableFunctions.bad()](solidity/tmp/test_payable_functions.sol#L32) should removed or do something

- [PayableFunctions.bad2(address)](solidity/tmp/test_payable_functions.sol#L34) should removed or do something

- [PayableFunctions.notBad()](solidity/tmp/test_payable_functions.sol#L36) should removed or do something

- [PayableFunctions.notBad2(uint256)](solidity/tmp/test_payable_functions.sol#L38) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_payable_functions.sol#L32
- solidity/tmp/test_payable_functions.sol#L34
- solidity/tmp/test_payable_functions.sol#L36
- solidity/tmp/test_payable_functions.sol#L38

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [PayableFunctions.owner](solidity/tmp/test_payable_functions.sol#L18) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_payable_functions.sol#L18

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

- [PayableFunctions.owner](solidity/tmp/test_payable_functions.sol#L18) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_payable_functions.sol#L18

### severity
Optimization

### category
state-should-be-constant

### confidence
High
