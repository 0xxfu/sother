## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Uninitialized local variables | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Don't use `payable.transfer()`/`payable.send()` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unused state variable | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}` | 2 |
| [G-1] | State variables that could be declared constant | 6 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [A.readAddress](solidity/uninitialized_local_variable.sol#L30) is never initialized. It is used in:
	- [B.bad()](solidity/uninitialized_local_variable.sol#L36-L38)

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
- solidity/uninitialized_local_variable.sol#L30

### severity:
High

### category:
uninitialized-state

## [Medium] Uninitialized local variables

### description:
Uninitialized local variables.

**There is `1` instance of this issue:**

- [Uninitialized.withdraw().to](solidity/uninitialized_local_variable.sol#L19) is a local variable never initialized

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

### recommendation:
Initialize all the variables. If a variable is meant to be initialized to zero, explicitly set it to zero to improve code readability.

### locations:
- solidity/uninitialized_local_variable.sol#L19

### severity:
Medium

### category:
uninitialized-local

## [Low] Don't use `payable.transfer()`/`payable.send()`

### description:

The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. 


**There is `1` instance of this issue:**

- Payable calls in [Uninitialized.withdraw()](solidity/uninitialized_local_variable.sol#L18-L21):
	- [address(to).transfer(1)](solidity/uninitialized_local_variable.sol#L20)

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


### recommendation:

Use OpenZeppelin's [Address.sendValue()](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/2271e2c58d007894c5fe23c4f03a95f645ac9175/contracts/utils/Address.sol#L41-L50) instead of `payable.transfer()`/`payable.send()`


### locations:
- solidity/uninitialized_local_variable.sol#L18-L21

### severity:
Low

### category:
payable-calls

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

## [Informational] Unused state variable

### description:
Unused state variable.

**There are `4` instances of this issue:**

- [A.unused](solidity/uninitialized_local_variable.sol#L25) is never used in [B](solidity/uninitialized_local_variable.sol#L35-L51)

- [A.unused2](solidity/uninitialized_local_variable.sol#L26) is never used in [B](solidity/uninitialized_local_variable.sol#L35-L51)

- [A.unused3](solidity/uninitialized_local_variable.sol#L27) is never used in [B](solidity/uninitialized_local_variable.sol#L35-L51)

- [A.unused4](solidity/uninitialized_local_variable.sol#L28) is never used in [B](solidity/uninitialized_local_variable.sol#L35-L51)


### recommendation:
Remove unused state variables.

### locations:
- solidity/uninitialized_local_variable.sol#L25
- solidity/uninitialized_local_variable.sol#L26
- solidity/uninitialized_local_variable.sol#L27
- solidity/uninitialized_local_variable.sol#L28

### severity:
Informational

### category:
unused-state

## [Optimization] The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`

### description:

The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)


**There are `2` instances of this issue:**

- [i ++](solidity/uninitialized_local_variable.sol#L9) should be used `unchecked{++i}/unchecked{i++}`.

- [j ++](solidity/uninitialized_local_variable.sol#L13) should be used `unchecked{++i}/unchecked{i++}`.


### recommendation:

Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.


### locations:
- solidity/uninitialized_local_variable.sol#L9
- solidity/uninitialized_local_variable.sol#L13

### severity:
Optimization

### category:
unchecked-in-loop

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `6` instances of this issue:**

- [A.unused](solidity/uninitialized_local_variable.sol#L25) should be constant 

- [A.unused2](solidity/uninitialized_local_variable.sol#L26) should be constant 

- [A.unused3](solidity/uninitialized_local_variable.sol#L27) should be constant 

- [A.unused4](solidity/uninitialized_local_variable.sol#L28) should be constant 

- [A.readAddress](solidity/uninitialized_local_variable.sol#L30) should be constant 

- [A.readInt](solidity/uninitialized_local_variable.sol#L31) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/uninitialized_local_variable.sol#L25
- solidity/uninitialized_local_variable.sol#L26
- solidity/uninitialized_local_variable.sol#L27
- solidity/uninitialized_local_variable.sol#L28
- solidity/uninitialized_local_variable.sol#L30
- solidity/uninitialized_local_variable.sol#L31

### severity:
Optimization

### category:
constable-states
