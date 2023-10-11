## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |
| [H-1] | State variable not initialized | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Uninitialized local variables | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Don't use `payable.transfer()`/`payable.send()` | 1 |
| [L-1] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | DoS With Block Gas Limit | 1 |
| [N-2] | Unnecessary Public Function Modifier | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}` | 2 |
| [G-1] | Remove unused local variables | 1 |
| [G-2] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 2 |
| [G-3] | Use `delete` to Clear Variables | 1 |
| [G-4] | State variables that could be declared constant | 6 |
| [G-5] | State variables that could be declared constant | 6 |



## [High] Uninitialized state variables

### description
Uninitialized state variables.

**There is `1` instance of this issue:**

- [A.readAddress](solidity/tmp/uninitialized_local_variable.sol#L30) is never initialized. It is used in:
	- [B.bad()](solidity/tmp/uninitialized_local_variable.sol#L36-L38)

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
- solidity/tmp/uninitialized_local_variable.sol#L30

### severity
High

### category
uninitialized-state

### confidence
High

## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There are `2` instances of this issue:**

- state variable: [A.readAddress](solidity/tmp/uninitialized_local_variable.sol#L30) not initialized and not written in contract but be used in contract

- state variable: [A.readInt](solidity/tmp/uninitialized_local_variable.sol#L31) not initialized and not written in contract but be used in contract

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
- solidity/tmp/uninitialized_local_variable.sol#L30
- solidity/tmp/uninitialized_local_variable.sol#L31

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Uninitialized local variables

### description
Uninitialized local variables.

**There is `1` instance of this issue:**

- [Uninitialized.withdraw().to](solidity/tmp/uninitialized_local_variable.sol#L19) is a local variable never initialized

#### Exploit scenario

```solidity
contract Uninitialized is Owner{
    function withdraw() payable public onlyOwner{
        address to;
        to.transfer(this.balance)
    }
}
```
Bob calls `transfer`. As a result, all Ether is sent to the address `0x0` and is lost.

### recommendation
Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.

### locations
- solidity/tmp/uninitialized_local_variable.sol#L19

### severity
Medium

### category
uninitialized-local

### confidence
Medium

## [Low] Don't use `payable.transfer()`/`payable.send()`

### description

The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. 


**There is `1` instance of this issue:**

- Payable calls in [Uninitialized.withdraw()](solidity/tmp/uninitialized_local_variable.sol#L18-L21):
	- [address(to).transfer(1)](solidity/tmp/uninitialized_local_variable.sol#L20)

#### Exploit scenario

The following cases can cause the transfer to fail:
* The contract does not have a `payable` callback
* The contract's `payable` callback spends more than 2300 gas (which is only enough to emit something)
* The contract is called through a proxy which itself uses up the 2300 gas

Any smart contract that uses `transfer()` or `send()` is taking a hard dependency on gas costs by forwarding a fixed amount of gas: `2300`.
```
contract Vulnerable {
    function withdraw(uint256 amount) external {
        // This forwards 2300 gas, which may not be enough if the recipient
        // is a contract and gas costs change.
        msg.sender.transfer(amount);
    }
}
```


### recommendation

Use OpenZeppelin's [Address.sendValue()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/2271e2c58d007894c5fe23c4f03a95f645ac9175/contracts/utils/Address.sol#L41-L50) instead of `payable.transfer()`/`payable.send()`


### locations
- solidity/tmp/uninitialized_local_variable.sol#L18-L21

### severity
Low

### category
payable-calls

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [B.good()](solidity/tmp/uninitialized_local_variable.sol#L44-L46) does not emit an event

- Setter function [B.fallback()](solidity/tmp/uninitialized_local_variable.sol#L48-L50) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/uninitialized_local_variable.sol#L44-L46
- solidity/tmp/uninitialized_local_variable.sol#L48-L50

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

## [Informational] DoS With Block Gas Limit

### description

    When smart contracts are deployed or functions inside them are called, the execution of these actions always requires a certain amount of gas, based of how much computation is needed to complete them. The Ethereum network specifies a block gas limit and the sum of all transactions included in a block can not exceed the threshold.
    Programming patterns that are harmless in centralized applications can lead to Denial of Service conditions in smart contracts when the cost of executing a function exceeds the block gas limit. Modifying an array of unknown size, that increases in size over time, can lead to such a Denial of Service condition.
    

**There is `1` instance of this issue:**

- Potential DoS Gas Limit Attack occur in[Uninitialized.noreportfor()](solidity/tmp/uninitialized_local_variable.sol#L8-L16)[BEGIN_LOOP](solidity/tmp/uninitialized_local_variable.sol#L9-L11)


### recommendation

    Caution is advised when you expect to have large arrays that grow over time. Actions that require looping across the entire data structure should be avoided.
    If you absolutely must loop over an array of unknown size, then you should plan for it to potentially take multiple blocks, and therefore require multiple transactions.
    

### locations
- solidity/tmp/uninitialized_local_variable.sol#L8-L16

### severity
Informational

### category
uncontrolled-resource-consumption

### confidence
Medium

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There is `1` instance of this issue:**

- function:[Uninitialized.noreportfor()](solidity/tmp/uninitialized_local_variable.sol#L8-L16)is public and can be replaced with external 

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
- solidity/tmp/uninitialized_local_variable.sol#L8-L16

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`

### description

The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)


**There are `2` instances of this issue:**

- [i ++](solidity/tmp/uninitialized_local_variable.sol#L9) should be used `unchecked{++i}/unchecked{i++}`.

- [j ++](solidity/tmp/uninitialized_local_variable.sol#L13) should be used `unchecked{++i}/unchecked{i++}`.


### recommendation

Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.


### locations
- solidity/tmp/uninitialized_local_variable.sol#L9
- solidity/tmp/uninitialized_local_variable.sol#L13

### severity
Optimization

### category
unchecked-in-loop

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There is `1` instance of this issue:**

- The local variables in [Uninitialized.noreportfor()](solidity/tmp/uninitialized_local_variable.sol#L8-L16) are unused.
	- [Uninitialized.noreportfor().a](solidity/tmp/uninitialized_local_variable.sol#L10)
	- [Uninitialized.noreportfor().b](solidity/tmp/uninitialized_local_variable.sol#L14)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/uninitialized_local_variable.sol#L8-L16

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)

### description

`++i` costs less gas compared to `i++` or `i += 1` for unsigned integer, as pre-increment is cheaper (about 5 gas per iteration). 
This statement is true even with the optimizer enabled.

`i++` increments i and returns the initial value of i. Which means:
```
uint i = 1;  
i++; // == 1 but i == 2  
```
But ++i returns the actual incremented value:
```
uint i = 1;  
++i; // == 2 and i == 2 too, so no need for a temporary variable  
```
In the first case, the compiler has to create a temporary variable (when used) 
for returning 1 instead of 2


**There are `2` instances of this issue:**

- [i ++](solidity/tmp/uninitialized_local_variable.sol#L9) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [j ++](solidity/tmp/uninitialized_local_variable.sol#L13) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.


### recommendation

Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.



### locations
- solidity/tmp/uninitialized_local_variable.sol#L9
- solidity/tmp/uninitialized_local_variable.sol#L13

### severity
Optimization

### category
pre-plus-plus

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There is `1` instance of this issue:**

- Should use `delete` statement instead of [used = address(0)](solidity/tmp/uninitialized_local_variable.sol#L49)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/uninitialized_local_variable.sol#L49

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `6` instances of this issue:**

- [A.unused](solidity/tmp/uninitialized_local_variable.sol#L25) should be constant 

- [A.unused2](solidity/tmp/uninitialized_local_variable.sol#L26) should be constant 

- [A.unused3](solidity/tmp/uninitialized_local_variable.sol#L27) should be constant 

- [A.unused4](solidity/tmp/uninitialized_local_variable.sol#L28) should be constant 

- [A.readAddress](solidity/tmp/uninitialized_local_variable.sol#L30) should be constant 

- [A.readInt](solidity/tmp/uninitialized_local_variable.sol#L31) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/uninitialized_local_variable.sol#L25
- solidity/tmp/uninitialized_local_variable.sol#L26
- solidity/tmp/uninitialized_local_variable.sol#L27
- solidity/tmp/uninitialized_local_variable.sol#L28
- solidity/tmp/uninitialized_local_variable.sol#L30
- solidity/tmp/uninitialized_local_variable.sol#L31

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `6` instances of this issue:**

- [A.unused](solidity/tmp/uninitialized_local_variable.sol#L25) should be constant

- [A.unused2](solidity/tmp/uninitialized_local_variable.sol#L26) should be constant

- [A.unused3](solidity/tmp/uninitialized_local_variable.sol#L27) should be constant

- [A.unused4](solidity/tmp/uninitialized_local_variable.sol#L28) should be constant

- [A.readAddress](solidity/tmp/uninitialized_local_variable.sol#L30) should be constant

- [A.readInt](solidity/tmp/uninitialized_local_variable.sol#L31) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/uninitialized_local_variable.sol#L25
- solidity/tmp/uninitialized_local_variable.sol#L26
- solidity/tmp/uninitialized_local_variable.sol#L27
- solidity/tmp/uninitialized_local_variable.sol#L28
- solidity/tmp/uninitialized_local_variable.sol#L30
- solidity/tmp/uninitialized_local_variable.sol#L31

### severity
Optimization

### category
state-should-be-constant

### confidence
High
