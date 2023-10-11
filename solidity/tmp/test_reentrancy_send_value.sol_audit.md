## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Reentrancy-Guard when using `sendValue` from OZ's `Address.sol` | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Low-level calls | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Use `selfbalance()` instead of `address(this).balance` | 1 |



## [Low] Missing Reentrancy-Guard when using `sendValue` from OZ's `Address.sol`

### description

OZ’s Address.sol library is used. Ether transfer is done with a `sendValue` call in 
the following functions.

There is this warning in OZ’s Address.sol library. Accordingly, he used the 
Check-Effect-Interaction pattern in the project:
```solidity
    * IMPORTANT: because control is transferred to `recipient`, care must be
    * taken to not create reentrancy vulnerabilities. Consider using
    * {ReentrancyGuard} or the
    * https://solidity.readthedocs.io/en/v0.5.11/security-considerations.html#use-the-checks-effects-interactions-pattern[checks-effects-interactions pattern].
    */
```

It would be best practice to use re-entrancy Guard for reasons such as complicated 
dangers such as view Re-Entrancy that emerged in the last period and the possibility 
of expanding the project and its integration with other contracts.


**There is `1` instance of this issue:**

- [recipient.sendValue(ethToSend)](solidity/tmp/test_reentrancy_send_value.sol#L22) should use Reentrancy-Guard.


### recommendation

Using [Reentrancy-Guard](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/bfff03c0d2a59bcd8e2ead1da9aed9edf0080d05/contracts/security/ReentrancyGuard.sol#L50C5-L62) 
when using `sendValue` from OZ's `Address.sol`.


### locations
- solidity/tmp/test_reentrancy_send_value.sol#L22

### severity
Low

### category
reentrancy-send-value

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

## [Informational] Low-level calls

### description
The use of low-level calls is error-prone. Low-level calls do not check for [code existence](https://solidity.readthedocs.io/en/v0.4.25/control-structures.html#error-handling-assert-require-revert-and-exceptions) or call success.

**There is `1` instance of this issue:**

- Low level call in [Address.sendValue(address,uint256)](solidity/tmp/test_reentrancy_send_value.sol#L6-L15):
	- [(success,None) = recipient.call{value: amount}("")](solidity/tmp/test_reentrancy_send_value.sol#L11)


### recommendation
Avoid low-level calls. Check the call success. If the call is meant for a contract, check for code existence.

### locations
- solidity/tmp/test_reentrancy_send_value.sol#L6-L15

### severity
Informational

### category
low-level-calls

### confidence
High

## [Optimization] Use `selfbalance()` instead of `address(this).balance`

### description

You can use `selfbalance()` instead of `address(this).balance` when 
getting your contract’s balance of ETH to save gas. 
Additionally, you can use `balance(address)` instead of address.balance() when 
getting an external contract’s balance of ETH.


**There is `1` instance of this issue:**

- Should use `selfbalance()` instead of [address(this).balance < amount](solidity/tmp/test_reentrancy_send_value.sol#L7)


### recommendation

Using `selfbalance()` instead of `address(this).balance`, for example:

```
function assemblyInternalBalance() public returns (uint256) {
    assembly {
        let c := selfbalance()
        mstore(0x00, c)
        return(0x00, 0x20)
    }
}
```


### locations
- solidity/tmp/test_reentrancy_send_value.sol#L7

### severity
Optimization

### category
use-self-balance

### confidence
High
