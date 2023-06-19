## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 3 |
| [H-1] | Unchecked transfer | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 3 |



## [High] Arbitrary `from` in transferFrom

### description:
Detect when `msg.sender` is not used as `from` in transferFrom.

**There are `3` instances of this issue:**

- [C.bad4(address,address,uint256)](solidity/send_erc20.sol#L65-L67) uses arbitrary from in transferFrom: [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/send_erc20.sol#L66)

- [C.bad3(address,address,uint256)](solidity/send_erc20.sol#L57-L59) uses arbitrary from in transferFrom: [erc20.safeTransferFrom(from,to,amount)](solidity/send_erc20.sol#L58)

- [C.bad1(address,uint256)](solidity/send_erc20.sol#L35-L37) uses arbitrary from in transferFrom: [erc20.transferFrom(notsend,to,am)](solidity/send_erc20.sol#L36)

#### Exploit scenario

```solidity
    function a(address from, address to, uint256 amount) public {
        erc20.transferFrom(from, to, am);
    }
```
Alice approves this contract to spend her ERC20 tokens. Bob can call `a` and specify Alice's address as the `from` parameter in `transferFrom`, allowing him to transfer Alice's tokens to himself.

### recommendation:

Use `msg.sender` as `from` in transferFrom.


### location:
- solidity/send_erc20.sol#L65-L67
- solidity/send_erc20.sol#L57-L59
- solidity/send_erc20.sol#L35-L37

### severity:
High

### category:
arbitrary-send-erc20

## [High] Unchecked transfer

### description:
The return value of an external transfer/transferFrom call is not checked

**There are `3` instances of this issue:**

- [C.good1(address,uint256)](solidity/send_erc20.sol#L30-L33) ignores return value by [erc20.transferFrom(from_msgsender,to,am)](solidity/send_erc20.sol#L32)

- [C.int_transferFrom(address,address,uint256)](solidity/send_erc20.sol#L49-L51) ignores return value by [erc20.transferFrom(from,to,amount)](solidity/send_erc20.sol#L50)

- [C.bad1(address,uint256)](solidity/send_erc20.sol#L35-L37) ignores return value by [erc20.transferFrom(notsend,to,am)](solidity/send_erc20.sol#L36)

#### Exploit scenario

```solidity
contract Token {
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
}
contract MyBank{  
    mapping(address => uint) balances;
    Token token;
    function deposit(uint amount) public{
        token.transferFrom(msg.sender, address(this), amount);
        balances[msg.sender] += amount;
    }
}
```
Several tokens do not revert in case of failure and return false. If one of these tokens is used in `MyBank`, `deposit` will not revert if the transfer fails, and an attacker can call `deposit` for free..

### recommendation:
Use `SafeERC20`, or ensure that the transfer/transferFrom return value is checked.

### location:
- solidity/send_erc20.sol#L30-L33
- solidity/send_erc20.sol#L49-L51
- solidity/send_erc20.sol#L35-L37

### severity:
High

### category:
unchecked-transfer

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Function [C.int_transferFrom(address,address,uint256)](solidity/send_erc20.sol#L49-L51) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/send_erc20.sol#L49-L51

### severity:
Informational

### category:
naming-convention

## [Optimization] State variables only set in the constructor should be declared immutable

### description:

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There are `3` instances of this issue:**

- [C.notsend](solidity/send_erc20.sol#L21) should be immutable 

- [C.erc20](solidity/send_erc20.sol#L20) should be immutable 

- [C.send](solidity/send_erc20.sol#L22) should be immutable 


### recommendation:
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### location:
- solidity/send_erc20.sol#L21
- solidity/send_erc20.sol#L20
- solidity/send_erc20.sol#L22

### severity:
Optimization

### category:
immutable-states
