## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Contracts that lock Ether | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 1 |
| [G-1] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- `NotBad.weth` (solidity/test_empty_receive.sol#L6) is never initialized. It is used in:
	- `NotBad.receive()` (solidity/test_empty_receive.sol#L8-L10)

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
- solidity/test_empty_receive.sol#L6

### severity:
High

### category:
uninitialized-state

## [Medium] Contracts that lock Ether

### description:
Contract with a `payable` function, but without a withdrawal capacity.

**There are `2` instances of this issue:**

- Contract locking ether found:
	Contract `Bad` (solidity/test_empty_receive.sol#L1-L3) has payable functions:
	 - `Bad.receive()` (solidity/test_empty_receive.sol#L2)
	But does not have a function to withdraw the ether

- Contract locking ether found:
	Contract `NotBad` (solidity/test_empty_receive.sol#L5-L11) has payable functions:
	 - `NotBad.receive()` (solidity/test_empty_receive.sol#L8-L10)
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
- solidity/test_empty_receive.sol#L1-L3
- solidity/test_empty_receive.sol#L5-L11

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

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- `require(bool)(msg.sender == address(weth))` (solidity/test_empty_receive.sol#L9) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_empty_receive.sol#L9

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- `NotBad.weth` (solidity/test_empty_receive.sol#L6) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_empty_receive.sol#L6

### severity:
Optimization

### category:
constable-states
