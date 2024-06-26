## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |
| [H-1] | Arbitrary `from` in transferFrom | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Incompatibility with transfer-on-fee or deflationary tokens | 13 |
| [M-1] | Return values of `transfer()/transferFrom()` not checked | 2 |
| [M-2] | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721 | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | use custom errors instead of revert strings | 4 |
| [G-1] | Amounts should be checked for `0` before calling a `transfer` | 13 |
| [G-2] | State variables that could be declared constant | 2 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

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
- solidity/test_unsafe_transfer.sol#L48

### severity:
High

### category:
uninitialized-state

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

## [Medium] Incompatibility with transfer-on-fee or deflationary tokens

### description:

Some ERC20 tokens make modifications to the standard implementations of
their ERC20’s `transfer` or `balanceOf` functions.
One type of such token is deflationary tokens that charge a fee on every
`transfer()` and `transferFrom()`.
The protocol does not have incompatibility with fee-on-transfer tokens.

Note that there has been a real-world exploit related to this with 
[Balancer pool and STA deflationary tokens](https://medium.com/1inch-network/balancer-hack-2020-a8f7131c980e).


**There are `13` instances of this issue:**

- [t.transferFrom(from,to,tokenId)](solidity/test_unsafe_transfer.sol#L35) with fee on transfer are not supported.

- [t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L52) with fee on transfer are not supported.

- [a = t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L56) with fee on transfer are not supported.

- [require(bool,string)(t.transfer(address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L60) with fee on transfer are not supported.

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L64) with fee on transfer are not supported.

- [t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L68) with fee on transfer are not supported.

- [ret = t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L72) with fee on transfer are not supported.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L77) with fee on transfer are not supported.

- [a = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L81) with fee on transfer are not supported.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L85) with fee on transfer are not supported.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L89) with fee on transfer are not supported.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L93) with fee on transfer are not supported.

- [ret = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L97) with fee on transfer are not supported.

#### Exploit scenario

i.e. Fee-on-transfer scenario:
1. Contract calls transfer from contractA 100 tokens to current contract
2. Current contract thinks it received 100 tokens
3. It updates balances to increase +100 tokens
4. While actually contract received only 90 tokens
5. That breaks whole math for given token


### recommendation:

1. Consider comparing before and after balance to get the actual transferred amount.
2. Alternatively, disallow tokens with fee-on-transfer mechanics to be added as tokens.


### locations:
- solidity/test_unsafe_transfer.sol#L35
- solidity/test_unsafe_transfer.sol#L52
- solidity/test_unsafe_transfer.sol#L56
- solidity/test_unsafe_transfer.sol#L60
- solidity/test_unsafe_transfer.sol#L64
- solidity/test_unsafe_transfer.sol#L68
- solidity/test_unsafe_transfer.sol#L72
- solidity/test_unsafe_transfer.sol#L77
- solidity/test_unsafe_transfer.sol#L81
- solidity/test_unsafe_transfer.sol#L85
- solidity/test_unsafe_transfer.sol#L89
- solidity/test_unsafe_transfer.sol#L93
- solidity/test_unsafe_transfer.sol#L97

### severity:
Medium

### category:
fee-on-transfer

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
unsafe-721-transfer

## [Low] `revert CustomError()` should be used instead of `assert()`

### description:

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the 
transaction's available gas** rather than returning it, as `require()`/`revert()` do. 
`assert()` should be avoided even past solidity version 0.8.0 as its 
[documentation](https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require) 
states that "The assert function creates an error of type Panic(uint256). ... 
Properly functioning code should never create a Panic, not even on invalid external 
input. If this happens, then there is a bug in your contract which you should fix.



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

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description:

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `13` instances of this issue:**

- Adding a non-zero-value check for [t.transferFrom(from,to,tokenId)](solidity/test_unsafe_transfer.sol#L35) at the beginning of [UnsafeErc721Transfer.bad0(address,address,uint256)](solidity/test_unsafe_transfer.sol#L30-L36)

- Adding a non-zero-value check for [t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L52) at the beginning of [UnsafeErc20Transfer.bad0()](solidity/test_unsafe_transfer.sol#L51-L53)

- Adding a non-zero-value check for [a = t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L56) at the beginning of [UnsafeErc20Transfer.good0()](solidity/test_unsafe_transfer.sol#L55-L57)

- Adding a non-zero-value check for [require(bool,string)(t.transfer(address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L60) at the beginning of [UnsafeErc20Transfer.good1()](solidity/test_unsafe_transfer.sol#L59-L61)

- Adding a non-zero-value check for [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L64) at the beginning of [UnsafeErc20Transfer.good2()](solidity/test_unsafe_transfer.sol#L63-L65)

- Adding a non-zero-value check for [t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L68) at the beginning of [UnsafeErc20Transfer.good3()](solidity/test_unsafe_transfer.sol#L67-L69)

- Adding a non-zero-value check for [ret = t.transfer(address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L72) at the beginning of [UnsafeErc20Transfer.good4()](solidity/test_unsafe_transfer.sol#L71-L73)

- Adding a non-zero-value check for [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L77) at the beginning of [UnsafeErc20Transfer.bad1()](solidity/test_unsafe_transfer.sol#L76-L78)

- Adding a non-zero-value check for [a = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L81) at the beginning of [UnsafeErc20Transfer.good5()](solidity/test_unsafe_transfer.sol#L80-L82)

- Adding a non-zero-value check for [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),failed)](solidity/test_unsafe_transfer.sol#L85) at the beginning of [UnsafeErc20Transfer.good6()](solidity/test_unsafe_transfer.sol#L84-L86)

- Adding a non-zero-value check for [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/test_unsafe_transfer.sol#L89) at the beginning of [UnsafeErc20Transfer.good7()](solidity/test_unsafe_transfer.sol#L88-L90)

- Adding a non-zero-value check for [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L93) at the beginning of [UnsafeErc20Transfer.good8()](solidity/test_unsafe_transfer.sol#L92-L94)

- Adding a non-zero-value check for [ret = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/test_unsafe_transfer.sol#L97) at the beginning of [UnsafeErc20Transfer.good9()](solidity/test_unsafe_transfer.sol#L96-L98)


### recommendation:

Consider adding a non-zero-value check at the beginning of function.


### locations:
- solidity/test_unsafe_transfer.sol#L35
- solidity/test_unsafe_transfer.sol#L52
- solidity/test_unsafe_transfer.sol#L56
- solidity/test_unsafe_transfer.sol#L60
- solidity/test_unsafe_transfer.sol#L64
- solidity/test_unsafe_transfer.sol#L68
- solidity/test_unsafe_transfer.sol#L72
- solidity/test_unsafe_transfer.sol#L77
- solidity/test_unsafe_transfer.sol#L81
- solidity/test_unsafe_transfer.sol#L85
- solidity/test_unsafe_transfer.sol#L89
- solidity/test_unsafe_transfer.sol#L93
- solidity/test_unsafe_transfer.sol#L97

### severity:
Optimization

### category:
zero-check-with-transfer

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
