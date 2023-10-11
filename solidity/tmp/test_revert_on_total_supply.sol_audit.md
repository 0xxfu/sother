## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Calls will revert when `totalSupply()` returns zero | 2 |
| [L-1] | Division by zero not prevented | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 1 |
| [G-1] | Remove unused local variables | 1 |
| [G-2] | The result of function calls should be cached rather than re-calling the function | 2 |
| [G-3] | State variables that could be declared constant | 1 |



## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There is `1` instance of this issue:**

- [RevertTotalSupply.notBad4(IERC20)](solidity/tmp/test_revert_on_total_supply.sol#L45-L47) ignores return value by [addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L46)

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
- solidity/tmp/test_revert_on_total_supply.sol#L45-L47

### severity
Medium

### category
unused-return

### confidence
Medium

## [Low] Calls will revert when `totalSupply()` returns zero

### description

`totalSupply()` being zero will result in a division by zero, 
causing the transaction to fail. 
The function should instead special-case this scenario, and avoid reverting.


**There are `2` instances of this issue:**

- [localUI / addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L10) should check if `totalSupply()` greater than zero before division.

- [supply = addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L14) should check if `totalSupply()` greater than zero before division.


### recommendation

Checking if `totalSupply()` greater than zero before division. 


### locations
- solidity/tmp/test_revert_on_total_supply.sol#L10
- solidity/tmp/test_revert_on_total_supply.sol#L14

### severity
Low

### category
revert-on-total-supply

### confidence
High

## [Low] Division by zero not prevented

### description

In Solidity, transactions are reverted with the "division by zero" error
message when a division by zero is attempted.
Although divisions by zero will result in reversions, 
they will not have error messages, 
making failed transaction more difficult to debug by users.

Consider actively preventing divisions by zero with appropriate `revert` statements that 
have informative and user-friendly error messages.


**There are `4` instances of this issue:**

- [localUI / addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L10) possible divisions by `0` can be performed.

- [abc = localUI / supply](solidity/tmp/test_revert_on_total_supply.sol#L16) possible divisions by `0` can be performed.

- [localUI / addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L24) possible divisions by `0` can be performed.

- [localUI / supply](solidity/tmp/test_revert_on_total_supply.sol#L42) possible divisions by `0` can be performed.


### recommendation

It is recommended to add a sanity check to control whether the borrowed
amount is zero or not.


### locations
- solidity/tmp/test_revert_on_total_supply.sol#L10
- solidity/tmp/test_revert_on_total_supply.sol#L16
- solidity/tmp/test_revert_on_total_supply.sol#L24
- solidity/tmp/test_revert_on_total_supply.sol#L42

### severity
Low

### category
division-by-zero

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

## [Optimization] Remove or replace unused state variables

### description

Saves a storage slot. If the variable is assigned a non-zero value, 
saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). 
If the variable remains unassigned, there is no gas savings unless the variable is public, 
in which case the compiler-generated non-payable getter deployment cost is saved. 
If the state variable is overriding an interface's public function, 
mark the variable as constant or immutable so that it does not use a storage slot


**There is `1` instance of this issue:**

- [RevertTotalSupply.erc20](solidity/tmp/test_revert_on_total_supply.sol#L6) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/test_revert_on_total_supply.sol#L6

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There is `1` instance of this issue:**

- The local variables in [RevertTotalSupply.bad2(IERC20)](solidity/tmp/test_revert_on_total_supply.sol#L13-L17) are unused.
	- [RevertTotalSupply.bad2(IERC20).abc](solidity/tmp/test_revert_on_total_supply.sol#L16)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_revert_on_total_supply.sol#L13-L17

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] The result of function calls should be cached rather than re-calling the function

### description

The instances below point to the second+ call of the function within a single function


**There are `2` instances of this issue:**

- `IERC20.totalSupply()` called result should be cached with local variable in [RevertTotalSupply.notBad(IERC20)](solidity/tmp/test_revert_on_total_supply.sol#L19-L25), It is called more than once:
	- [addr.totalSupply() == 0](solidity/tmp/test_revert_on_total_supply.sol#L20)
	- [localUI / addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L24)

- `IERC20.totalSupply()` called result should be cached with local variable in [RevertTotalSupply.notBad3(IERC20)](solidity/tmp/test_revert_on_total_supply.sol#L36-L43), It is called more than once:
	- [addr.totalSupply() == 0](solidity/tmp/test_revert_on_total_supply.sol#L38)
	- [supply = addr.totalSupply()](solidity/tmp/test_revert_on_total_supply.sol#L37)


### recommendation

Using local variable to cache function called result if the same function called more than once.


### locations
- solidity/tmp/test_revert_on_total_supply.sol#L19-L25
- solidity/tmp/test_revert_on_total_supply.sol#L36-L43

### severity
Optimization

### category
cache-call-function-result

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [RevertTotalSupply.erc20](solidity/tmp/test_revert_on_total_supply.sol#L6) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_revert_on_total_supply.sol#L6

### severity
Optimization

### category
constable-states

### confidence
High
