## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too) | 8 |
| [G-1] | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}` | 1 |



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

## [Optimization] `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)

### description:

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


**There are `8` instances of this issue:**

- `a ++` (solidity/test_pre_plusplus.sol#L3) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `a --` (solidity/test_pre_plusplus.sol#L7) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `a += 1` (solidity/test_pre_plusplus.sol#L11) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `a -= 1` (solidity/test_pre_plusplus.sol#L15) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `i ++` (solidity/test_pre_plusplus.sol#L19) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `a -= 1` (solidity/test_pre_plusplus.sol#L20) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `i --` (solidity/test_pre_plusplus.sol#L25) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.

- `a += 1` (solidity/test_pre_plusplus.sol#L26) should use `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` operator to save gas.


### recommendation:

Using `++i`/`--i` instead of `i++`/`i--`/`i+=1`/`i-=1` to operate the value of an uint variable.



### locations:
- solidity/test_pre_plusplus.sol#L3
- solidity/test_pre_plusplus.sol#L7
- solidity/test_pre_plusplus.sol#L11
- solidity/test_pre_plusplus.sol#L15
- solidity/test_pre_plusplus.sol#L19
- solidity/test_pre_plusplus.sol#L20
- solidity/test_pre_plusplus.sol#L25
- solidity/test_pre_plusplus.sol#L26

### severity:
Optimization

### category:
pre-plus-plus

## [Optimization] The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`

### description:

The unchecked keyword is new in solidity version 0.8.0, so this only applies to that version or higher, which these instances are. 
Gas savings: roughly speaking this can save 30-40 gas per loop iteration. For lengthy loops, this can be significant!

More detail see [this.](https://gist.github.com/0xxfu/67eb8e3d8fe0b8d35370c1263e606d38)


**There is `1` instance of this issue:**

- `i ++` (solidity/test_pre_plusplus.sol#L19) should be used `unchecked{++i}/unchecked{i++}`.


### recommendation:

Using `unchecked{++i}/unchecked{i++}` replace `++i/i++` in loop.


### locations:
- solidity/test_pre_plusplus.sol#L19

### severity:
Optimization

### category:
unchecked-in-loop
