## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Return values of `transfer()/transferFrom()` not checked | 2 |
| [M-1] | Unsafe use of `transfer()/transferFrom()` with IERC20 | 12 |
| [M-2] | Unused return | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | `revert CustomError()` should be used instead of `assert()` | 2 |
| [L-1] | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards | 12 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 16 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 1 |
| [G-1] | Using custom errors replace `require` or `assert` | 4 |
| [G-2] | Not using the named return variables anywhere in the function is confusing | 2 |
| [G-3] | Remove unused parameter variables | 2 |
| [G-4] | Remove unused local variables | 2 |
| [G-5] | Amounts should be checked for `0` before calling a `transfer` | 12 |
| [G-6] | Setting the constructor to `payable` | 1 |



## [Medium] Return values of `transfer()/transferFrom()` not checked

### description

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `2` instances of this issue:**

- [C.bad0()](solidity/tmp/unused_return_transfers.sol#L20-L22) ignores return value by [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L21)

- [C.bad1()](solidity/tmp/unused_return_transfers.sol#L40-L42) ignores return value by [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L41)

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

### recommendation
Use `SafeERC20`, or ensure that the transfer/transferFrom return value is checked.

### locations
- solidity/tmp/unused_return_transfers.sol#L20-L22
- solidity/tmp/unused_return_transfers.sol#L40-L42

### severity
Medium

### category
unchecked-transfer

### confidence
Medium

## [Medium] Unsafe use of `transfer()/transferFrom()` with IERC20

### description

Some tokens do not implement the ERC20 standard properly but are still accepted by most code 
that accepts ERC20 tokens. For example Tether (USDT)'s `transfer()` and `transferFrom()` functions 
on L1 do not return booleans as the specification requires, and instead have no return value. 
When these sorts of tokens are cast to IERC20, their [function signatures](https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca) 
do not match and therefore the calls made, revert.


**There are `12` instances of this issue:**

- [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L21) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [a = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L24) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [require(bool,string)(t.transfer(address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L27) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L30) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L33) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [ret = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L36) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L41) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [a = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L44) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L47) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L50) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L53) should be replaced by `safeTransfer()/safeTransferFrom()`.

- [ret = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L56) should be replaced by `safeTransfer()/safeTransferFrom()`.


### recommendation

Use [OpenZeppelin’s SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) 
`safeTransfer()/safeTransferFrom()` instead of `transfer()/transferFrom()`


### locations
- solidity/tmp/unused_return_transfers.sol#L21
- solidity/tmp/unused_return_transfers.sol#L24
- solidity/tmp/unused_return_transfers.sol#L27
- solidity/tmp/unused_return_transfers.sol#L30
- solidity/tmp/unused_return_transfers.sol#L33
- solidity/tmp/unused_return_transfers.sol#L36
- solidity/tmp/unused_return_transfers.sol#L41
- solidity/tmp/unused_return_transfers.sol#L44
- solidity/tmp/unused_return_transfers.sol#L47
- solidity/tmp/unused_return_transfers.sol#L50
- solidity/tmp/unused_return_transfers.sol#L53
- solidity/tmp/unused_return_transfers.sol#L56

### severity
Medium

### category
unsafe-transfer

### confidence
High

## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There is `1` instance of this issue:**

- [C.good10()](solidity/tmp/unused_return_transfers.sol#L60-L62) ignores return value by [t.other()](solidity/tmp/unused_return_transfers.sol#L61)

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

### recommendation
Ensure that all the return values of the function calls are used.

### locations
- solidity/tmp/unused_return_transfers.sol#L60-L62

### severity
Medium

### category
unused-return

### confidence
Medium

## [Low] `revert CustomError()` should be used instead of `assert()`

### description

Prior to solidity version 0.8.0, hitting an assert consumes the **remainder of the 
transaction's available gas** rather than returning it, as `require()`/`revert()` do. 
`assert()` should be avoided even past solidity version 0.8.0 as its 
[documentation](https://docs.soliditylang.org/en/latest/control-structures.html#panic-via-assert-and-error-via-require) 
states that "The assert function creates an error of type Panic(uint256). ... 
Properly functioning code should never create a Panic, not even on invalid external 
input. If this happens, then there is a bug in your contract which you should fix.



**There are `2` instances of this issue:**

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L30) should be replaced by `if (!condition) revert CustomError();`.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L50) should be replaced by `if (!condition) revert CustomError();`.


### recommendation

Please use `if (!condition) revert CustomError();` instead of `assert()`.


### locations
- solidity/tmp/unused_return_transfers.sol#L30
- solidity/tmp/unused_return_transfers.sol#L50

### severity
Low

### category
deprecated-assert

### confidence
High

## [Low] Functions calling contracts/addresses with transfer hooks are missing reentrancy guards

### description

Even if the function follows the best practice of check-effects-interaction, 
not using a reentrancy guard when there may be transfer hooks will open the 
users of this protocol up to 
[read-only reentrancies](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem/) 
with no way to protect against it, except by block-listing the whole protocol.


**There are `12` instances of this issue:**

- [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L21) should use Reentrancy-Guard.

- [a = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L24) should use Reentrancy-Guard.

- [require(bool,string)(t.transfer(address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L27) should use Reentrancy-Guard.

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L30) should use Reentrancy-Guard.

- [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L33) should use Reentrancy-Guard.

- [ret = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L36) should use Reentrancy-Guard.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L41) should use Reentrancy-Guard.

- [a = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L44) should use Reentrancy-Guard.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L47) should use Reentrancy-Guard.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L50) should use Reentrancy-Guard.

- [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L53) should use Reentrancy-Guard.

- [ret = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L56) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when calling contracts/addresses with transfer hooks.


### locations
- solidity/tmp/unused_return_transfers.sol#L21
- solidity/tmp/unused_return_transfers.sol#L24
- solidity/tmp/unused_return_transfers.sol#L27
- solidity/tmp/unused_return_transfers.sol#L30
- solidity/tmp/unused_return_transfers.sol#L33
- solidity/tmp/unused_return_transfers.sol#L36
- solidity/tmp/unused_return_transfers.sol#L41
- solidity/tmp/unused_return_transfers.sol#L44
- solidity/tmp/unused_return_transfers.sol#L47
- solidity/tmp/unused_return_transfers.sol#L50
- solidity/tmp/unused_return_transfers.sol#L53
- solidity/tmp/unused_return_transfers.sol#L56

### severity
Low

### category
reentrancy-transfer

### confidence
High

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

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `16` instances of this issue:**

- function:[Token.transfer(address,uint256)](solidity/tmp/unused_return_transfers.sol#L2-L4)is public and can be replaced with external 

- function:[Token.transferFrom(address,address,uint256)](solidity/tmp/unused_return_transfers.sol#L5-L7)is public and can be replaced with external 

- function:[Token.other()](solidity/tmp/unused_return_transfers.sol#L8-L10)is public and can be replaced with external 

- function:[C.bad0()](solidity/tmp/unused_return_transfers.sol#L20-L22)is public and can be replaced with external 

- function:[C.good0()](solidity/tmp/unused_return_transfers.sol#L23-L25)is public and can be replaced with external 

- function:[C.good1()](solidity/tmp/unused_return_transfers.sol#L26-L28)is public and can be replaced with external 

- function:[C.good2()](solidity/tmp/unused_return_transfers.sol#L29-L31)is public and can be replaced with external 

- function:[C.good3()](solidity/tmp/unused_return_transfers.sol#L32-L34)is public and can be replaced with external 

- function:[C.good4()](solidity/tmp/unused_return_transfers.sol#L35-L37)is public and can be replaced with external 

- function:[C.bad1()](solidity/tmp/unused_return_transfers.sol#L40-L42)is public and can be replaced with external 

- function:[C.good5()](solidity/tmp/unused_return_transfers.sol#L43-L45)is public and can be replaced with external 

- function:[C.good6()](solidity/tmp/unused_return_transfers.sol#L46-L48)is public and can be replaced with external 

- function:[C.good7()](solidity/tmp/unused_return_transfers.sol#L49-L51)is public and can be replaced with external 

- function:[C.good8()](solidity/tmp/unused_return_transfers.sol#L52-L54)is public and can be replaced with external 

- function:[C.good9()](solidity/tmp/unused_return_transfers.sol#L55-L57)is public and can be replaced with external 

- function:[C.good10()](solidity/tmp/unused_return_transfers.sol#L60-L62)is public and can be replaced with external 

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
- solidity/tmp/unused_return_transfers.sol#L2-L4
- solidity/tmp/unused_return_transfers.sol#L5-L7
- solidity/tmp/unused_return_transfers.sol#L8-L10
- solidity/tmp/unused_return_transfers.sol#L20-L22
- solidity/tmp/unused_return_transfers.sol#L23-L25
- solidity/tmp/unused_return_transfers.sol#L26-L28
- solidity/tmp/unused_return_transfers.sol#L29-L31
- solidity/tmp/unused_return_transfers.sol#L32-L34
- solidity/tmp/unused_return_transfers.sol#L35-L37
- solidity/tmp/unused_return_transfers.sol#L40-L42
- solidity/tmp/unused_return_transfers.sol#L43-L45
- solidity/tmp/unused_return_transfers.sol#L46-L48
- solidity/tmp/unused_return_transfers.sol#L49-L51
- solidity/tmp/unused_return_transfers.sol#L52-L54
- solidity/tmp/unused_return_transfers.sol#L55-L57
- solidity/tmp/unused_return_transfers.sol#L60-L62

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] State variables only set in the constructor should be declared immutable

### description

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There is `1` instance of this issue:**

- [C.t](solidity/tmp/unused_return_transfers.sol#L13) should be immutable 


### recommendation
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations
- solidity/tmp/unused_return_transfers.sol#L13

### severity
Optimization

### category
immutable-states

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `4` instances of this issue:**

- [require(bool,string)(t.transfer(address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L27) should use custom error to save gas.

- [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L30) should use custom error to save gas.

- [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L47) should use custom error to save gas.

- [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L50) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/unused_return_transfers.sol#L27
- solidity/tmp/unused_return_transfers.sol#L30
- solidity/tmp/unused_return_transfers.sol#L47
- solidity/tmp/unused_return_transfers.sol#L50

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Not using the named return variables anywhere in the function is confusing

### description

Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.


**There are `2` instances of this issue:**

- The named return variables in [Token.transfer(address,uint256)](solidity/tmp/unused_return_transfers.sol#L2-L4) are unused.
	- [Token.transfer(address,uint256).success](solidity/tmp/unused_return_transfers.sol#L2)

- The named return variables in [Token.transferFrom(address,address,uint256)](solidity/tmp/unused_return_transfers.sol#L5-L7) are unused.
	- [Token.transferFrom(address,address,uint256).success](solidity/tmp/unused_return_transfers.sol#L5)


### recommendation

Remove the unused named return variables.


### locations
- solidity/tmp/unused_return_transfers.sol#L2-L4
- solidity/tmp/unused_return_transfers.sol#L5-L7

### severity
Optimization

### category
unused-named-return-variables

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `2` instances of this issue:**

- The param variables in [Token.transfer(address,uint256)](solidity/tmp/unused_return_transfers.sol#L2-L4) are unused.
	- [Token.transfer(address,uint256)._value](solidity/tmp/unused_return_transfers.sol#L2)
	- [Token.transfer(address,uint256)._to](solidity/tmp/unused_return_transfers.sol#L2)

- The param variables in [Token.transferFrom(address,address,uint256)](solidity/tmp/unused_return_transfers.sol#L5-L7) are unused.
	- [Token.transferFrom(address,address,uint256)._to](solidity/tmp/unused_return_transfers.sol#L5)
	- [Token.transferFrom(address,address,uint256)._from](solidity/tmp/unused_return_transfers.sol#L5)
	- [Token.transferFrom(address,address,uint256)._value](solidity/tmp/unused_return_transfers.sol#L5)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/unused_return_transfers.sol#L2-L4
- solidity/tmp/unused_return_transfers.sol#L5-L7

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `2` instances of this issue:**

- The local variables in [C.good0()](solidity/tmp/unused_return_transfers.sol#L23-L25) are unused.
	- [C.good0().a](solidity/tmp/unused_return_transfers.sol#L24)

- The local variables in [C.good5()](solidity/tmp/unused_return_transfers.sol#L43-L45) are unused.
	- [C.good5().a](solidity/tmp/unused_return_transfers.sol#L44)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/unused_return_transfers.sol#L23-L25
- solidity/tmp/unused_return_transfers.sol#L43-L45

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `12` instances of this issue:**

- Adding a non-zero-value check for [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L21) at the beginning of [C.bad0()](solidity/tmp/unused_return_transfers.sol#L20-L22)

- Adding a non-zero-value check for [a = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L24) at the beginning of [C.good0()](solidity/tmp/unused_return_transfers.sol#L23-L25)

- Adding a non-zero-value check for [require(bool,string)(t.transfer(address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L27) at the beginning of [C.good1()](solidity/tmp/unused_return_transfers.sol#L26-L28)

- Adding a non-zero-value check for [assert(bool)(t.transfer(address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L30) at the beginning of [C.good2()](solidity/tmp/unused_return_transfers.sol#L29-L31)

- Adding a non-zero-value check for [t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L33) at the beginning of [C.good3()](solidity/tmp/unused_return_transfers.sol#L32-L34)

- Adding a non-zero-value check for [ret = t.transfer(address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L36) at the beginning of [C.good4()](solidity/tmp/unused_return_transfers.sol#L35-L37)

- Adding a non-zero-value check for [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L41) at the beginning of [C.bad1()](solidity/tmp/unused_return_transfers.sol#L40-L42)

- Adding a non-zero-value check for [a = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L44) at the beginning of [C.good5()](solidity/tmp/unused_return_transfers.sol#L43-L45)

- Adding a non-zero-value check for [require(bool,string)(t.transferFrom(address(this),address(0),1000000000000000000),"failed")](solidity/tmp/unused_return_transfers.sol#L47) at the beginning of [C.good6()](solidity/tmp/unused_return_transfers.sol#L46-L48)

- Adding a non-zero-value check for [assert(bool)(t.transferFrom(address(this),address(0),1000000000000000000))](solidity/tmp/unused_return_transfers.sol#L50) at the beginning of [C.good7()](solidity/tmp/unused_return_transfers.sol#L49-L51)

- Adding a non-zero-value check for [t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L53) at the beginning of [C.good8()](solidity/tmp/unused_return_transfers.sol#L52-L54)

- Adding a non-zero-value check for [ret = t.transferFrom(address(this),address(0),1000000000000000000)](solidity/tmp/unused_return_transfers.sol#L56) at the beginning of [C.good9()](solidity/tmp/unused_return_transfers.sol#L55-L57)


### recommendation

Consider adding a non-zero-value check at the beginning of function.


### locations
- solidity/tmp/unused_return_transfers.sol#L21
- solidity/tmp/unused_return_transfers.sol#L24
- solidity/tmp/unused_return_transfers.sol#L27
- solidity/tmp/unused_return_transfers.sol#L30
- solidity/tmp/unused_return_transfers.sol#L33
- solidity/tmp/unused_return_transfers.sol#L36
- solidity/tmp/unused_return_transfers.sol#L41
- solidity/tmp/unused_return_transfers.sol#L44
- solidity/tmp/unused_return_transfers.sol#L47
- solidity/tmp/unused_return_transfers.sol#L50
- solidity/tmp/unused_return_transfers.sol#L53
- solidity/tmp/unused_return_transfers.sol#L56

### severity
Optimization

### category
zero-check-with-transfer

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- [C.constructor()](solidity/tmp/unused_return_transfers.sol#L15-L17) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/unused_return_transfers.sol#L15-L17

### severity
Optimization

### category
payable-constructor

### confidence
High
