## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Assembly usage | 1 |
| [N-2] | Costly operations inside a loop | 1 |
| [N-3] | Conformance to Solidity naming conventions | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}` | 1 |
| [G-1] | Use assembly to check for `address(0)` | 1 |
| [G-2] | Use `assembly` to write address storage values | 3 |



## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `3` instances of this issue:**

- Setter function [AddressOptimizatioin.bad(address)](solidity/tmp/test_address_optimization.sol#L4-L8) does not emit an event

- Setter function [AddressOptimizatioin.bad2()](solidity/tmp/test_address_optimization.sol#L10-L12) does not emit an event

- Setter function [AddressOptimizatioin.bad3(uint256)](solidity/tmp/test_address_optimization.sol#L14-L18) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_address_optimization.sol#L4-L8
- solidity/tmp/test_address_optimization.sol#L10-L12
- solidity/tmp/test_address_optimization.sol#L14-L18

### severity
Low

### category
pess-event-setter

### confidence
Medium

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

## [Informational] Assembly usage

### description
The use of assembly is error-prone and should be avoided.

**There is `1` instance of this issue:**

- [AddressOptimizatioin.notBad(address)](solidity/tmp/test_address_optimization.sol#L20-L24) uses assembly
	- [INLINE ASM](solidity/tmp/test_address_optimization.sol#L21-L23)


### recommendation
Do not use `evm` assembly.

### locations
- solidity/tmp/test_address_optimization.sol#L20-L24

### severity
Informational

### category
assembly

### confidence
High

## [Informational] Costly operations inside a loop

### description
Costly operations inside a loop might waste gas, so optimizations are justified.

**There is `1` instance of this issue:**

- [AddressOptimizatioin.bad3(uint256)](solidity/tmp/test_address_optimization.sol#L14-L18) has costly operations inside a loop:
	- [addr = msg.sender](solidity/tmp/test_address_optimization.sol#L16)

#### Exploit scenario

```solidity
contract CostlyOperationsInLoop{

    uint loop_count = 100;
    uint state_variable=0;

    function bad() external{
        for (uint i=0; i < loop_count; i++){
            state_variable++;
        }
    }

    function good() external{
      uint local_variable = state_variable;
      for (uint i=0; i < loop_count; i++){
        local_variable++;
      }
      state_variable = local_variable;
    }
}
```
Incrementing `state_variable` in a loop incurs a lot of gas because of expensive `SSTOREs`, which might lead to an `out-of-gas`.

### recommendation
Use a local variable to hold the loop computation result.

### locations
- solidity/tmp/test_address_optimization.sol#L14-L18

### severity
Informational

### category
costly-loop

### confidence
Medium

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `2` instances of this issue:**

- Parameter [AddressOptimizatioin.bad(address)._addr](solidity/tmp/test_address_optimization.sol#L4) is not in mixedCase

- Parameter [AddressOptimizatioin.notBad(address)._addr](solidity/tmp/test_address_optimization.sol#L20) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_address_optimization.sol#L4
- solidity/tmp/test_address_optimization.sol#L20

### severity
Informational

### category
naming-convention

### confidence
High

## [Optimization] The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`

### description

The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)


**There is `1` instance of this issue:**

- [++ a](solidity/tmp/test_address_optimization.sol#L15) should be used `unchecked{++i}/unchecked{i++}`.


### recommendation

Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.


### locations
- solidity/tmp/test_address_optimization.sol#L15

### severity
Optimization

### category
unchecked-in-loop

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There is `1` instance of this issue:**

- [_addr != address(0)](solidity/tmp/test_address_optimization.sol#L5) should use assembly to check for `address(0)`


### recommendation

Use assembly to check for `address(0)`:

```
function addrNotZero(address _addr) public pure {
        assembly {
            if iszero(_addr) {
                mstore(0x00, "zero address")
                revert(0x00, 0x20)
            }
        }
}
```


### locations
- solidity/tmp/test_address_optimization.sol#L5

### severity
Optimization

### category
zero-address-optimization

### confidence
High

## [Optimization] Use `assembly` to write address storage values

### description

Where it does not affect readability, 
using assembly for simple setters allows to save gas not only on deployment, 
but also on function calls.


**There are `3` instances of this issue:**

- [addr = _addr](solidity/tmp/test_address_optimization.sol#L6) should use `assembly` update address to save gas.

- [addr = msg.sender](solidity/tmp/test_address_optimization.sol#L11) should use `assembly` update address to save gas.

- [addr = msg.sender](solidity/tmp/test_address_optimization.sol#L16) should use `assembly` update address to save gas.


### recommendation

Using `assembly` update address to save gas.

For example:
```
contract Contract1 {
    address owner;

    function assemblyUpdateOwner(address newOwner) public {
        assembly {
            sstore(owner.slot, newOwner)
        }
    }
}
```


### locations
- solidity/tmp/test_address_optimization.sol#L6
- solidity/tmp/test_address_optimization.sol#L11
- solidity/tmp/test_address_optimization.sol#L16

### severity
Optimization

### category
assembly-update-address

### confidence
High
