## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 1 |
| [H-1] | Uninitialized state variables | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Return values of `transfer()/transferFrom()` not checked | 2 |
| [M-1] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 4 |
| [G-1] | State variables that could be declared constant | 2 |



## [High] Arbitrary `from` in transferFrom

### description:
Detect when `msg.sender` is not used as `from` in transferFrom.

**There is `1` instance of this issue:**

- [UnsafeErc721Transfer.bad0(address,address,uint256)](solidity/test_unsafe_transfer.sol#L30-L36) uses arbitrary from in transferFrom: [t.transferFrom(from,to,tokenId)](solidity/test_unsafe_transfer.sol#L35)

#### Exploit scenario

```solidity
    function a(address from, address to, uint256 amount) public {
        erc20.transferFrom(from, to, am);
    }
```
Alice approves this contract to spend her ERC20 tokens. Bob can call `a` and specify Alice's address as the `from` parameter in `transferFrom`, allowing him to transfer Alice's tokens to himself.

### recommendation:

Use `msg.sender` as `from` in transferFrom.


### locations:
- solidity/test_unsafe_transfer.sol#L30-L36

### severity:
High

### category:
arbitrary-send-erc20

## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There are `2` instances of this issue:**

- [UnsafeErc721Transfer.t](solidity/test_unsafe_transfer.sol#L28) is never initialized. It is used in:
	- [UnsafeErc721Transfer.bad0(address,address,uint256)](solidity/test_unsafe_transfer.sol#L30-L36)
	- [UnsafeErc721Transfer.good0(address,address,uint256)](solidity/test_unsafe_transfer.sol#L38-L44)

- [UnsafeErc20Transfer.t](solidity/test_unsafe_transfer.sol#L48) is never initialized. It is used in:
	- [UnsafeErc20Transfer.bad0()](solidity/test_unsafe_transfer.sol#L51-L53)
	- [UnsafeErc20Transfer.good0()](solidity/test_unsafe_transfer.sol#L55-L57)
	- [UnsafeErc20Transfer.good1()](solidity/test_unsafe_transfer.sol#L59-L61)
	- [UnsafeErc20Transfer.good2()](solidity/test_unsafe_transfer.sol#L63-L65)
	- [UnsafeErc20Transfer.good3()](solidity/test_unsafe_transfer.sol#L67-L69)
	- [UnsafeErc20Transfer.good4()](solidity/test_unsafe_transfer.sol#L71-L73)
	- [UnsafeErc20Transfer.bad1()](solidity/test_unsafe_transfer.sol#L76-L78)
	- [UnsafeErc20Transfer.good5()](solidity/test_unsafe_transfer.sol#L80-L82)
	- [UnsafeErc20Transfer.good6()](solidity/test_unsafe_transfer.sol#L84-L86)
	- [UnsafeErc20Transfer.good7()](solidity/test_unsafe_transfer.sol#L88-L90)
	- [UnsafeErc20Transfer.good8()](solidity/test_unsafe_transfer.sol#L92-L94)
	- [UnsafeErc20Transfer.good9()](solidity/test_unsafe_transfer.sol#L96-L98)

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
- solidity/test_unsafe_transfer.sol#L28
- solidity/test_unsafe_transfer.sol#L48

### severity:
High

### category:
uninitialized-state

## [Medium] Return values of `transfer()/transferFrom()` not checked

### description:

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `2` instances of this issue:**

- [UnsafeErc20Transfer.bad0()](solidity/test_unsafe_transfer.sol#L51-L53) ignores return value by [t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L52)

- [UnsafeErc20Transfer.bad1()](solidity/test_unsafe_transfer.sol#L76-L78) ignores return value by [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L77)

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

### locations:
- solidity/test_unsafe_transfer.sol#L51-L53
- solidity/test_unsafe_transfer.sol#L76-L78

### severity:
Medium

### category:
unchecked-transfer

## [Medium] Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721

### description:

ERC721 NFTs may get locked forever if the recipient is not aware of ERC721 for some reason. 
While `safeTransferFrom()` is used for ERC1155 NFTs (which has the `_doSafeTransferAcceptanceCheck` 
check on recipient and does not have an option to avoid this), `transferFrom()` is used for 
ERC721 NFTs presumably for gas savings and reentrancy concerns over its `safeTransferFrom` 
variant (which has the `_checkOnERC721Received` check on the recipient).


**There is `1` instance of this issue:**

- [t.transferFrom(from,to,tokenId)](solidity/test_unsafe_transfer.sol#L35) should be replaced by `safeTransferFrom()`.

#### Exploit scenario

if `_to` is a contract address that does not support ERC721, the NFT can be frozen in 
that contract.

As per the documentation of EIP-721:
> A wallet/broker/auction application MUST implement the wallet interface if it will 
accept safe transfers.

Ref: https://eips.ethereum.org/EIPS/eip-721


### recommendation:

Evaluate using ERC721 `safeTransferFrom()` to avoid NFTs getting stuck vis-a-vis its 
reentrancy risk and gas costs.


### locations:
- solidity/test_unsafe_transfer.sol#L35

### severity:
Medium

### category:
unsafe-transfer-erc721

## [Low] `revert CustomError()` should be used instead of `assert()`

### description:

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the transaction's available gas** rather than returning it, as `require()`/`revert()` do. `assert()` should be avoided even past solidity version 0.8.0 as its [documentation](https://docs.soliditylang.org/en/v0.8.19/control-structures.html#panic-via-assert-and-error-via-require) states that "The assert function creates an error of type Panic(uint256). ... Properly functioning code should never create a Panic, not even on invalid external input. If this happens, then there is a bug in your contract which you should fix.



**There are `2` instances of this issue:**

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L64) should be replaced by `if (!condition) revert CustomError();`.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L89) should be replaced by `if (!condition) revert CustomError();`.


### recommendation:

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations:
- solidity/test_unsafe_transfer.sol#L64
- solidity/test_unsafe_transfer.sol#L89

### severity:
Low

### category:
deprecated-assert

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `4` instances of this issue:**

- [require(bool,string)(t.transfer(address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L60) should use custom error to save gas.

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L64) should use custom error to save gas.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L85) should use custom error to save gas.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L89) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unsafe_transfer.sol#L60
- solidity/test_unsafe_transfer.sol#L64
- solidity/test_unsafe_transfer.sol#L85
- solidity/test_unsafe_transfer.sol#L89

### severity:
Optimization

### category:
use-custom-error

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnsafeErc721Transfer.t](solidity/test_unsafe_transfer.sol#L28) should be constant 

- [UnsafeErc20Transfer.t](solidity/test_unsafe_transfer.sol#L48) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unsafe_transfer.sol#L28
- solidity/test_unsafe_transfer.sol#L48

### severity:
Optimization

### category:
constable-states