## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Functions that send Ether to arbitrary destinations | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unchecked Send | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Don't use `payable.transfer()`/`payable.send()` | 2 |
| [L-1] | Missing zero address validation | 2 |



## [High] Functions that send Ether to arbitrary destinations

### description:
Unprotected call to a function sending Ether to an arbitrary address.

**There are `2` instances of this issue:**

- [PayableCalls.transfer(address)](solidity/test_payable_calls.sol#L3-L5) sends eth to arbitrary user
	Dangerous calls:
	- [address(to).transfer(1)](solidity/test_payable_calls.sol#L4)

- [PayableCalls.send(address)](solidity/test_payable_calls.sol#L7-L10) sends eth to arbitrary user
	Dangerous calls:
	- [address(to).send(1)](solidity/test_payable_calls.sol#L8)

#### Exploit scenario

```solidity
contract ArbitrarySendEth{
    address destination;
    function setDestination(){
        destination = msg.sender;
    }

    function withdraw() public{
        destination.transfer(this.balance);
    }
}
```
Bob calls `setDestination` and `withdraw`. As a result he withdraws the contract's balance.

### recommendation:
Ensure that an arbitrary user cannot withdraw unauthorized funds.

### locations:
- solidity/test_payable_calls.sol#L3-L5
- solidity/test_payable_calls.sol#L7-L10

### severity:
High

### category:
arbitrary-send-eth

## [Medium] Unchecked Send

### description:
The return value of a `send` is not checked.

**There is `1` instance of this issue:**

- [PayableCalls.send(address)](solidity/test_payable_calls.sol#L7-L10) ignores return value by [address(to).send(1)](solidity/test_payable_calls.sol#L8)

#### Exploit scenario

```solidity
contract MyConc{
    function my_func(address payable dst) public payable{
        dst.send(msg.value);
    }
}
```
The return value of `send` is not checked, so if the send fails, the Ether will be locked in the contract.
If `send` is used to prevent blocking operations, consider logging the failed `send`.
    

### recommendation:
Ensure that the return value of `send` is checked or logged.

### locations:
- solidity/test_payable_calls.sol#L7-L10

### severity:
Medium

### category:
unchecked-send

## [Low] Don't use `payable.transfer()`/`payable.send()`

### description:

The use of `payable.transfer()` is [heavily frowned upon](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/) because it can lead to the locking of funds. The `transfer()` call requires that the recipient is either an EOA account, or is a contract that has a `payable` callback. For the contract case, the `transfer()` call only provides 2300 gas for the contract to complete its operations. This means the following cases can cause the transfer to fail:
* The contract does not have a `payable` callback
* The contract's `payable` callback spends more than 2300 gas (which is only enough to emit something)
* The contract is called through a proxy which itself uses up the 2300 gas

Use OpenZeppelin's `Address.sendValue()` instead


**There are `2` instances of this issue:**

- Payable calls in [PayableCalls.transfer(address)](solidity/test_payable_calls.sol#L3-L5):
	- [address(to).transfer(1)](solidity/test_payable_calls.sol#L4)

- Payable calls in [PayableCalls.send(address)](solidity/test_payable_calls.sol#L7-L10):
	- [address(to).send(1)](solidity/test_payable_calls.sol#L8)

#### Exploit scenario

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
- solidity/test_payable_calls.sol#L3-L5
- solidity/test_payable_calls.sol#L7-L10

### severity:
Low

### category:
payable-calls

## [Low] Missing zero address validation

### description:
Detect missing zero address validation.

**There are `2` instances of this issue:**

- [PayableCalls.send(address).to](solidity/test_payable_calls.sol#L7) lacks a zero-check on :
		- [address(to).send(1)](solidity/test_payable_calls.sol#L8)

- [PayableCalls.transfer(address).to](solidity/test_payable_calls.sol#L3) lacks a zero-check on :
		- [address(to).transfer(1)](solidity/test_payable_calls.sol#L4)

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


### recommendation:
Check that the address is not zero.

### locations:
- solidity/test_payable_calls.sol#L7
- solidity/test_payable_calls.sol#L3

### severity:
Low

### category:
missing-zero-check
