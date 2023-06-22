## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Unprotected upgradeable contract | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-1] | State variables should be cached in stack variables rather than re-reading them from storage | 4 |
| [G-2] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 1 |
| [G-3] | use custom errors instead of revert strings | 10 |



## [High] Unprotected upgradeable contract

### description:
Detects logic contract that can be destructed.

**There is `1` instance of this issue:**

- [Buggy](solidity/test_unprotected_upgradeable.sol#L19-L30) is an upgradeable contract that does not protect its initialize functions: [Buggy.initialize()](solidity/test_unprotected_upgradeable.sol#L22-L25). Anyone can delete the contract with: [Buggy.kill()](solidity/test_unprotected_upgradeable.sol#L26-L29)
#### Exploit scenario

```solidity
contract Buggy is Initializable{
    address payable owner;

    function initialize() external initializer{
        require(owner == address(0));
        owner = msg.sender;
    }
    function kill() external{
        require(msg.sender == owner);
        selfdestruct(owner);
    }
}
```
Buggy is an upgradeable contract. Anyone can call initialize on the logic contract, and destruct the contract.


### recommendation:
Add a constructor to ensure `initialize` cannot be called on the logic contract.

### locations:
- solidity/test_unprotected_upgradeable.sol#L19-L30

### severity:
High

### category:
unprotected-upgrade

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `2` instances of this issue:**

- Contract [Not_Upgradeable](solidity/test_unprotected_upgradeable.sol#L56-L57) is not in CapWords

- Function [Fixed.other_function()](solidity/test_unprotected_upgradeable.sol#L51-L53) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_unprotected_upgradeable.sol#L56-L57
- solidity/test_unprotected_upgradeable.sol#L51-L53

### severity:
Informational

### category:
naming-convention

## [Optimization] `internal` functions only called once can be inlined to save gas

### description:

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- [Initializable._disableInitializers()](solidity/test_unprotected_upgradeable.sol#L9-L14) could be inlined to save gas

### recommendation:
Using inlining replace `internal` function which only called once

### locations:
- solidity/test_unprotected_upgradeable.sol#L9-L14

### severity:
Optimization

### category:
internal-function-to-inline

## [Optimization] State variables should be cached in stack variables rather than re-reading them from storage

### description:

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `4` instances of this issue:**

- [Fixed2.owner](solidity/test_unprotected_upgradeable.sol#L73) should be cached with local memory-based variable in [Fixed2.kill()](solidity/test_unprotected_upgradeable.sol#L82-L85), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L83)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L84)

- [Fixed.owner](solidity/test_unprotected_upgradeable.sol#L35) should be cached with local memory-based variable in [Fixed.kill()](solidity/test_unprotected_upgradeable.sol#L46-L49), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L47)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L48)

- [Fixed3.owner](solidity/test_unprotected_upgradeable.sol#L89) should be cached with local memory-based variable in [Fixed3.kill()](solidity/test_unprotected_upgradeable.sol#L100-L103), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L101)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L102)

- [Buggy.owner](solidity/test_unprotected_upgradeable.sol#L20) should be cached with local memory-based variable in [Buggy.kill()](solidity/test_unprotected_upgradeable.sol#L26-L29), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L27)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L28)


### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations:
- solidity/test_unprotected_upgradeable.sol#L73
- solidity/test_unprotected_upgradeable.sol#L35
- solidity/test_unprotected_upgradeable.sol#L89
- solidity/test_unprotected_upgradeable.sol#L20

### severity:
Optimization

### category:
reread-state-variables

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description:

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/v0.8.11/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There is `1` instance of this issue:**

- [Initializable._initialized](solidity/test_unprotected_upgradeable.sol#L2) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/test_unprotected_upgradeable.sol#L2

### severity:
Optimization

### category:
smaller-uint-int

## [Optimization] use custom errors instead of revert strings

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `10` instances of this issue:**

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L83) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L42) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L78) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L23) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L47) should use custom error to save gas.

- [require(bool,string)(! _initializing,Initializable: contract is initializing)](solidity/test_unprotected_upgradeable.sol#L10) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L101) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L27) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L67) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L96) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unprotected_upgradeable.sol#L83
- solidity/test_unprotected_upgradeable.sol#L42
- solidity/test_unprotected_upgradeable.sol#L78
- solidity/test_unprotected_upgradeable.sol#L23
- solidity/test_unprotected_upgradeable.sol#L47
- solidity/test_unprotected_upgradeable.sol#L10
- solidity/test_unprotected_upgradeable.sol#L101
- solidity/test_unprotected_upgradeable.sol#L27
- solidity/test_unprotected_upgradeable.sol#L67
- solidity/test_unprotected_upgradeable.sol#L96

### severity:
Optimization

### category:
use-custom-error
