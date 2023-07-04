## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Uninitialized state variables | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Incompatibility with transfer-on-fee or deflationary tokens | 4 |
| [M-1] | Return values of `transfer()/transferFrom()` not checked | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `calldata` instead of `memory` for function parameters | 3 |
| [G-1] | State variables should be cached in stack variables rather than re-reading them from storage | 4 |
| [G-2] | Amounts should be checked for `0` before calling a `transfer` | 8 |
| [G-3] | State variables that could be declared constant | 1 |



## [High] Uninitialized state variables

### description:
Uninitialized state variables.

**There is `1` instance of this issue:**

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) is never initialized. It is used in:
	- [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49)
	- [FeeOnTransfer.bad1(address,uint256)](solidity/test_fee_on_transfer.sol#L51-L54)
	- [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61)
	- [FeeOnTransfer.good1(address,uint256)](solidity/test_fee_on_transfer.sol#L63-L68)

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
- solidity/test_fee_on_transfer.sol#L44

### severity:
High

### category:
uninitialized-state

## [Medium] Incompatibility with transfer-on-fee or deflationary tokens

### description:

Some ERC20 tokens make modifications to the standard implementations of
their ERC20’s `transfer` or `balanceOf` functions.
One type of such token is deflationary tokens that charge a fee on every
`transfer()` and `transferFrom()`.
The protocol does not have incompatibility with fee-on-transfer tokens.

Note that there has been a real-world exploit related to this with 
[Balancer pool and STA deflationary tokens](https://medium.com/1inch-network/balancer-hack-2020-a8f7131c980e).


**There are `4` instances of this issue:**

- [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L47) with fee on transfer are not supported.

- [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L48) with fee on transfer are not supported.

- [token.safeTransfer(to,amount)](solidity/test_fee_on_transfer.sol#L52) with fee on transfer are not supported.

- [token.safeTransferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L53) with fee on transfer are not supported.

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
- solidity/test_fee_on_transfer.sol#L47
- solidity/test_fee_on_transfer.sol#L48
- solidity/test_fee_on_transfer.sol#L52
- solidity/test_fee_on_transfer.sol#L53

### severity:
Medium

### category:
fee-on-transfer

## [Medium] Return values of `transfer()/transferFrom()` not checked

### description:

Not all `IERC20` implementations `revert()` when there's a failure in `transfer()`/`transferFrom()`. The function signature has a `boolean` return value and they indicate errors that way instead. By not checking the return value, operations that should have marked as failed, may potentially go through without actually making a payment.


**There are `4` instances of this issue:**

- [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49) ignores return value by [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L47)

- [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L48)

- [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61) ignores return value by [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L59)

- [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61) ignores return value by [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L58)

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
- solidity/test_fee_on_transfer.sol#L46-L49
- solidity/test_fee_on_transfer.sol#L46-L49
- solidity/test_fee_on_transfer.sol#L56-L61
- solidity/test_fee_on_transfer.sol#L56-L61

### severity:
Medium

### category:
unchecked-transfer

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

## [Optimization] Use `calldata` instead of `memory` for function parameters

### description:

On external functions, when using the `memory` keyword with a function argument, what's happening is a `memory` acts as an intermediate.

When the function gets called externally, the array values are kept in `calldata` and copied to memory during ABI decoding (using the opcode `calldataload` and `mstore`). 
And during the for loop, the values in the array are accessed in memory using a `mload`. That is inefficient. Reading directly from `calldata` using `calldataload` instead of going via `memory` saves the gas from the intermediate memory operations that carry the values.

More detail see [this](https://ethereum.stackexchange.com/questions/74442/when-should-i-use-calldata-and-when-should-i-use-memory)


**There are `3` instances of this issue:**

- [SafeERC20.safeTransfer(IERC20,address,uint256)](solidity/test_fee_on_transfer.sol#L4-L13) read-only `memory` parameters below should be changed to `calldata` :
	- [SafeERC20.safeTransfer(IERC20,address,uint256).token](solidity/test_fee_on_transfer.sol#L5)

- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256)](solidity/test_fee_on_transfer.sol#L15-L25) read-only `memory` parameters below should be changed to `calldata` :
	- [SafeERC20.safeTransferFrom(IERC20,address,address,uint256).token](solidity/test_fee_on_transfer.sol#L16)

- [SafeERC20._callOptionalReturn(IERC20,bytes)](solidity/test_fee_on_transfer.sol#L27) read-only `memory` parameters below should be changed to `calldata` :
	- [SafeERC20._callOptionalReturn(IERC20,bytes).token](solidity/test_fee_on_transfer.sol#L27)


### recommendation:
Use `calldata` instead of `memory` for external functions where the function argument is read-only.

### locations:
- solidity/test_fee_on_transfer.sol#L4-L13
- solidity/test_fee_on_transfer.sol#L15-L25
- solidity/test_fee_on_transfer.sol#L27

### severity:
Optimization

### category:
memory-in-parameters

## [Optimization] State variables should be cached in stack variables rather than re-reading them from storage

### description:

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `4` instances of this issue:**

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) should be cached with local memory-based variable in [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61), It is called more than once:
	- [beforeBalance = token.balanceOf(to)](solidity/test_fee_on_transfer.sol#L57)
	- [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L58)
	- [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L59)
	- [afterBalance = token.balanceOf(to)](solidity/test_fee_on_transfer.sol#L60)

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) should be cached with local memory-based variable in [FeeOnTransfer.good1(address,uint256)](solidity/test_fee_on_transfer.sol#L63-L68), It is called more than once:
	- [beforeBalance = token.balanceOf(to)](solidity/test_fee_on_transfer.sol#L64)
	- [token.safeTransfer(to,amount)](solidity/test_fee_on_transfer.sol#L65)
	- [token.safeTransferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L66)
	- [afterBalance = token.balanceOf(to)](solidity/test_fee_on_transfer.sol#L67)

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) should be cached with local memory-based variable in [FeeOnTransfer.bad1(address,uint256)](solidity/test_fee_on_transfer.sol#L51-L54), It is called more than once:
	- [token.safeTransfer(to,amount)](solidity/test_fee_on_transfer.sol#L52)
	- [token.safeTransferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L53)

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) should be cached with local memory-based variable in [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49), It is called more than once:
	- [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L47)
	- [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L48)


### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations:
- solidity/test_fee_on_transfer.sol#L44
- solidity/test_fee_on_transfer.sol#L44
- solidity/test_fee_on_transfer.sol#L44
- solidity/test_fee_on_transfer.sol#L44

### severity:
Optimization

### category:
reread-state-variables

## [Optimization] Amounts should be checked for `0` before calling a `transfer`

### description:

According to the fact that EIP-20 [states](https://github.com/ethereum/EIPs/blob/46b9b698815abbfa628cd1097311deee77dd45c5/EIPS/eip-20.md?plain=1#L116) that zero-valued transfers must be accepted.

Checking non-zero transfer values can avoid an expensive external call and save gas.
While this is done at some places, it’s not consistently done in the solution.


**There are `8` instances of this issue:**

- Adding a non-zero-value check for [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L47) at the beginning of [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49)

- Adding a non-zero-value check for [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L48) at the beginning of [FeeOnTransfer.bad0(address,uint256)](solidity/test_fee_on_transfer.sol#L46-L49)

- Adding a non-zero-value check for [token.safeTransfer(to,amount)](solidity/test_fee_on_transfer.sol#L52) at the beginning of [FeeOnTransfer.bad1(address,uint256)](solidity/test_fee_on_transfer.sol#L51-L54)

- Adding a non-zero-value check for [token.safeTransferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L53) at the beginning of [FeeOnTransfer.bad1(address,uint256)](solidity/test_fee_on_transfer.sol#L51-L54)

- Adding a non-zero-value check for [token.transfer(to,amount)](solidity/test_fee_on_transfer.sol#L58) at the beginning of [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61)

- Adding a non-zero-value check for [token.transferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L59) at the beginning of [FeeOnTransfer.good0(address,uint256)](solidity/test_fee_on_transfer.sol#L56-L61)

- Adding a non-zero-value check for [token.safeTransfer(to,amount)](solidity/test_fee_on_transfer.sol#L65) at the beginning of [FeeOnTransfer.good1(address,uint256)](solidity/test_fee_on_transfer.sol#L63-L68)

- Adding a non-zero-value check for [token.safeTransferFrom(address(this),to,amount)](solidity/test_fee_on_transfer.sol#L66) at the beginning of [FeeOnTransfer.good1(address,uint256)](solidity/test_fee_on_transfer.sol#L63-L68)


### recommendation:

Consider adding a non-zero-value check at the beginning of function.


### locations:
- solidity/test_fee_on_transfer.sol#L47
- solidity/test_fee_on_transfer.sol#L48
- solidity/test_fee_on_transfer.sol#L52
- solidity/test_fee_on_transfer.sol#L53
- solidity/test_fee_on_transfer.sol#L58
- solidity/test_fee_on_transfer.sol#L59
- solidity/test_fee_on_transfer.sol#L65
- solidity/test_fee_on_transfer.sol#L66

### severity:
Optimization

### category:
zero-check-with-transfer

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [FeeOnTransfer.token](solidity/test_fee_on_transfer.sol#L44) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_fee_on_transfer.sol#L44

### severity:
Optimization

### category:
constable-states
