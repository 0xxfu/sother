## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Return values of `transfer()/transferFrom()` not checked | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 1 |
| [G-1] | Use `calldata` instead of `memory` for function parameters | 2 |
| [G-2] | use custom errors instead of revert strings | 4 |



## [Medium] Unused return

### description:
The return value of an external call is not stored in a local or state variable.

**There is `1` instance of this issue:**

- [C.good10()](solidity/unused_return_transfers.sol#L60-L62) ignores return value by [t.other()](solidity/unused_return_transfers.sol#L61)

#### Exploit scenario

```solidity
contract MyConc{
    using SafeMath for uint;   
    function my_func(uint a, uint b) public{
        a.add(b);
    }
}
```
`MyConc` calls `add` of `SafeMath`, but does not store the result in `a`. As a result, the computation has no effect.

### recommendation:
Ensure that all the return values of the function calls are used.

### location:
- solidity/unused_return_transfers.sol#L60-L62

### severity:
Medium

### category:
unused-return

## [Low] Return values of `transfer()/transferFrom()` not checked

### description:

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `2` instances of this issue:**

- [C.bad0()](solidity/unused_return_transfers.sol#L20-L22) ignores return value by [t.transfer(address(0),1000000000000000000)](solidity/unused_return_transfers.sol#L21)

- [C.bad1()](solidity/unused_return_transfers.sol#L40-L42) ignores return value by [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/unused_return_transfers.sol#L41)

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
- solidity/unused_return_transfers.sol#L20-L22
- solidity/unused_return_transfers.sol#L40-L42

### severity:
Low

### category:
unchecked-transfer

## [Optimization] State variables only set in the constructor should be declared immutable

### description:

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There is `1` instance of this issue:**

- [C.t](solidity/unused_return_transfers.sol#L13) should be immutable 


### recommendation:
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### location:
- solidity/unused_return_transfers.sol#L13

### severity:
Optimization

### category:
immutable-states

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `2` instances of this issue:**

- [Token.transferFrom(address,address,uint256)](solidity/unused_return_transfers.sol#L5-L7) read-only `memory` parameters below should be changed to `calldata` :
	- [Token.transferFrom(address,address,uint256)._from](solidity/unused_return_transfers.sol#L5)
	- [Token.transferFrom(address,address,uint256)._to](solidity/unused_return_transfers.sol#L5)
	- [Token.transferFrom(address,address,uint256)._value](solidity/unused_return_transfers.sol#L5)

- [Token.transfer(address,uint256)](solidity/unused_return_transfers.sol#L2-L4) read-only `memory` parameters below should be changed to `calldata` :
	- [Token.transfer(address,uint256)._to](solidity/unused_return_transfers.sol#L2)
	- [Token.transfer(address,uint256)._value](solidity/unused_return_transfers.sol#L2)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### location:
- solidity/unused_return_transfers.sol#L5-L7
- solidity/unused_return_transfers.sol#L2-L4

### severity:
Optimization

### category:
memory-in-parameters

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `4` instances of this issue:**

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/unused_return_transfers.sol#L30) should use custom error to save gas.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/unused_return_transfers.sol#L50) should use custom error to save gas.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),failed)](solidity/unused_return_transfers.sol#L47) should use custom error to save gas.

- [require(bool,string)(t.transfer(address(0),1000000000000000000),failed)](solidity/unused_return_transfers.sol#L27) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### location:
- solidity/unused_return_transfers.sol#L30
- solidity/unused_return_transfers.sol#L50
- solidity/unused_return_transfers.sol#L47
- solidity/unused_return_transfers.sol#L27

### severity:
Optimization

### category:
use-custom-error
