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
| [L-0] | Missing zero address validation | 2 |



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
