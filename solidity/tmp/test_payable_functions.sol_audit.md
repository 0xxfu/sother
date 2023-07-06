## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Setting the constructor to `payable` | 2 |
| [G-1] | Functions guaranteed to revert when called by normal users can be marked `payable` | 2 |
| [G-2] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- `PayableFunctions.owner` (solidity/test_payable_functions.sol#L18) is never initialized. It is used in:

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


### recommendation:

Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.


### locations:
- solidity/test_payable_functions.sol#L18

### severity:
High

### category:
uninitialized-state

## [Medium] Contracts that lock Ether

### description:
Contract with a `payable` function, but without a withdrawal capacity.

**There are `3` instances of this issue:**

- Contract locking ether found:
	Contract `NotBadConstructor` (solidity/test_payable_functions.sol#L9-L11) has payable functions:
	 - `NotBadConstructor.constructor(address)` (solidity/test_payable_functions.sol#L10)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract `NotBadConstructor2` (solidity/test_payable_functions.sol#L13-L15) has payable functions:
	 - `NotBadConstructor2.constructor()` (solidity/test_payable_functions.sol#L14)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract `PayableFunctions` (solidity/test_payable_functions.sol#L17-L39) has payable functions:
	 - `PayableFunctions.notBad()` (solidity/test_payable_functions.sol#L36)
	 - `PayableFunctions.notBad2(uint256)` (solidity/test_payable_functions.sol#L38)
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

### recommendation:
Remove the payable attribute or add a withdraw function.

### locations:
- solidity/test_payable_functions.sol#L9-L11
- solidity/test_payable_functions.sol#L13-L15
- solidity/test_payable_functions.sol#L17-L39

### severity:
Medium

### category:
locked-ether

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

## [Optimization] Setting the constructor to `payable`

### description:

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `2` instances of this issue:**

- `BadConstructor.constructor(address)` (solidity/test_payable_functions.sol#L2) should be set to `payable` 

- `BadConstructor2.constructor()` (solidity/test_payable_functions.sol#L6) should be set to `payable` 


### recommendation:

Set the constructor to `payable`.


### locations:
- solidity/test_payable_functions.sol#L2
- solidity/test_payable_functions.sol#L6

### severity:
Optimization

### category:
payable-constructor

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


**There are `2` instances of this issue:**

- `PayableFunctions.bad()` (solidity/test_payable_functions.sol#L32) should be set to `payable` 

- `PayableFunctions.bad2(address)` (solidity/test_payable_functions.sol#L34) should be set to `payable` 


### recommendation:

Set the function to `payable`.


### locations:
- solidity/test_payable_functions.sol#L32
- solidity/test_payable_functions.sol#L34

### severity:
Optimization

### category:
payable-function

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- `PayableFunctions.owner` (solidity/test_payable_functions.sol#L18) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_payable_functions.sol#L18

### severity:
Optimization

### category:
constable-states
