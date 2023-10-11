## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Integer Overflow and Underflow | 6 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | DoS With Block Gas Limit | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache the `<array>.length` for the loop condition | 4 |
| [G-1] | Dead-code: functions not used should be removed to save deployment gas | 1 |
| [G-2] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 5 |
| [G-3] | Use `delete` to Clear Variables | 5 |



## [Medium] Integer Overflow and Underflow

### description

    若不使用OpenZeppelin的SafeMath(或类似的库)检查溢出/下溢，
    如果用户/攻击者能够控制这种算术运算的整数操作数，
    可能会导致漏洞或意外行为。
    Solc v0.8.0为所有算术运算引入了默认的溢出/底溢检查。(见这里和这里)

**There are `6` instances of this issue:**

- bad(uint256[]) has possible integer overflow/underflow:
	- [sum += ns[i]](solidity/tmp/test_array_length_in_loop.sol#L9)

- bad(uint256[]) has possible integer overflow/underflow:
	- [state = state + ns.length](solidity/tmp/test_array_length_in_loop.sol#L14)

- externalView(uint256[]) has possible integer overflow/underflow:
	- [sum += ns[i]](solidity/tmp/test_array_length_in_loop.sol#L20)

- externalPure(uint256[]) has possible integer overflow/underflow:
	- [sum += ns[i]](solidity/tmp/test_array_length_in_loop.sol#L31)

- internalView(uint256[]) has possible integer overflow/underflow:
	- [sum += ns[i]](solidity/tmp/test_array_length_in_loop.sol#L42)

- good(uint256[]) has possible integer overflow/underflow:
	- [sum += ns[i]](solidity/tmp/test_array_length_in_loop.sol#L54)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_array_length_in_loop.sol#L9
- solidity/tmp/test_array_length_in_loop.sol#L14
- solidity/tmp/test_array_length_in_loop.sol#L20
- solidity/tmp/test_array_length_in_loop.sol#L31
- solidity/tmp/test_array_length_in_loop.sol#L42
- solidity/tmp/test_array_length_in_loop.sol#L54

### severity
Medium

### category
integer-overflow

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [LoopArrayLength.bad(uint256[])](solidity/tmp/test_array_length_in_loop.sol#L6-L15) does not emit an event

- Setter function [LoopArrayLength.good(uint256[])](solidity/tmp/test_array_length_in_loop.sol#L50-L60) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_array_length_in_loop.sol#L6-L15
- solidity/tmp/test_array_length_in_loop.sol#L50-L60

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

## [Informational] DoS With Block Gas Limit

### description

    When smart contracts are deployed or functions inside them are called, the execution of these actions always requires a certain amount of gas, based of how much computation is needed to complete them. The Ethereum network specifies a block gas limit and the sum of all transactions included in a block can not exceed the threshold.
    Programming patterns that are harmless in centralized applications can lead to Denial of Service conditions in smart contracts when the cost of executing a function exceeds the block gas limit. Modifying an array of unknown size, that increases in size over time, can lead to such a Denial of Service condition.
    

**There are `2` instances of this issue:**

- Potential DoS Gas Limit Attack occur in[LoopArrayLength.bad(uint256[])](solidity/tmp/test_array_length_in_loop.sol#L6-L15)[BEGIN_LOOP](solidity/tmp/test_array_length_in_loop.sol#L8-L13)

- Potential DoS Gas Limit Attack occur in[LoopArrayLength.good(uint256[])](solidity/tmp/test_array_length_in_loop.sol#L50-L60)[BEGIN_LOOP](solidity/tmp/test_array_length_in_loop.sol#L53-L58)


### recommendation

    Caution is advised when you expect to have large arrays that grow over time. Actions that require looping across the entire data structure should be avoided.
    If you absolutely must loop over an array of unknown size, then you should plan for it to potentially take multiple blocks, and therefore require multiple transactions.
    

### locations
- solidity/tmp/test_array_length_in_loop.sol#L6-L15
- solidity/tmp/test_array_length_in_loop.sol#L50-L60

### severity
Informational

### category
uncontrolled-resource-consumption

### confidence
Medium

## [Optimization] Cache the `<array>.length` for the loop condition

### description

The overheads outlined below are _PER LOOP_, excluding the first loop
* storage arrays incur a Gwarmaccess (**100 gas**)
* memory arrays use `MLOAD` (**3 gas**)
* calldata arrays use `CALLDATALOAD` (**3 gas**)

Caching the length changes each of these to a `DUP<N>` (**3 gas**), and gets rid of the extra `DUP<N>` needed to store the stack offset.
More detail optimization see [this](https://gist.github.com/0xxfu/80fcbc39d2d38d85ae61b4b8838ef30b)


**There are `4` instances of this issue:**

- [i < ns.length](solidity/tmp/test_array_length_in_loop.sol#L8) `<array>.length` should be cached.

- [i < ns.length](solidity/tmp/test_array_length_in_loop.sol#L19) `<array>.length` should be cached.

- [i < ns.length](solidity/tmp/test_array_length_in_loop.sol#L30) `<array>.length` should be cached.

- [i < ns.length](solidity/tmp/test_array_length_in_loop.sol#L41) `<array>.length` should be cached.


### recommendation

Caching the `<array>.length` for the loop condition, for example:
```solidity
// gas save (-230)
function loopArray_cached(uint256[] calldata ns) public returns (uint256 sum) {
    uint256 length = ns.length;
    for(uint256 i = 0; i < length;) {
        sum += ns[i];
        unchecked {
            i++;
        }
    }
}
```


### locations
- solidity/tmp/test_array_length_in_loop.sol#L8
- solidity/tmp/test_array_length_in_loop.sol#L19
- solidity/tmp/test_array_length_in_loop.sol#L30
- solidity/tmp/test_array_length_in_loop.sol#L41

### severity
Optimization

### category
array-length-in-loop

### confidence
High

## [Optimization] Dead-code: functions not used should be removed to save deployment gas

### description
Functions that are not sued.

**There is `1` instance of this issue:**

- [LoopArrayLength.internalView(uint256[])](solidity/tmp/test_array_length_in_loop.sol#L39-L48) is never used and should be removed


### recommendation
Remove unused functions.

### locations
- solidity/tmp/test_array_length_in_loop.sol#L39-L48

### severity
Optimization

### category
dead-code

### confidence
High

## [Optimization] `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)

### description

`++i` costs less gas compared to `i++` or `i += 1` for unsigned integer, as pre-increment is cheaper (about 5 gas per iteration). 
This statement is true even with the optimizer enabled.

`i++` increments i and returns the initial value of i. Which means:
```
uint i = 1;  
i++; // == 1 but i == 2  
```
But ++i returns the actual incremented value:
```
uint i = 1;  
++i; // == 2 and i == 2 too, so no need for a temporary variable  
```
In the first case, the compiler has to create a temporary variable (when used) 
for returning 1 instead of 2


**There are `5` instances of this issue:**

- [i ++](solidity/tmp/test_array_length_in_loop.sol#L11) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [i ++](solidity/tmp/test_array_length_in_loop.sol#L22) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [i ++](solidity/tmp/test_array_length_in_loop.sol#L33) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [i ++](solidity/tmp/test_array_length_in_loop.sol#L44) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- [i ++](solidity/tmp/test_array_length_in_loop.sol#L56) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.


### recommendation

Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.



### locations
- solidity/tmp/test_array_length_in_loop.sol#L11
- solidity/tmp/test_array_length_in_loop.sol#L22
- solidity/tmp/test_array_length_in_loop.sol#L33
- solidity/tmp/test_array_length_in_loop.sol#L44
- solidity/tmp/test_array_length_in_loop.sol#L56

### severity
Optimization

### category
pre-plus-plus

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There are `5` instances of this issue:**

- Should use `delete` statement instead of [sum = 0](solidity/tmp/test_array_length_in_loop.sol#L7)

- Should use `delete` statement instead of [sum = 0](solidity/tmp/test_array_length_in_loop.sol#L18)

- Should use `delete` statement instead of [sum = 0](solidity/tmp/test_array_length_in_loop.sol#L29)

- Should use `delete` statement instead of [sum = 0](solidity/tmp/test_array_length_in_loop.sol#L40)

- Should use `delete` statement instead of [sum = 0](solidity/tmp/test_array_length_in_loop.sol#L52)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/test_array_length_in_loop.sol#L7
- solidity/tmp/test_array_length_in_loop.sol#L18
- solidity/tmp/test_array_length_in_loop.sol#L29
- solidity/tmp/test_array_length_in_loop.sol#L40
- solidity/tmp/test_array_length_in_loop.sol#L52

### severity
Optimization

### category
use-delete-statement

### confidence
High
