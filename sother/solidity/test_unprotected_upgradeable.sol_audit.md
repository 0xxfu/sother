## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Unprotected upgradeable contract | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 4 |
| [L-1] | Use `disableInitializers` to prevent front-running on the initialize function | 1 |
| [L-2] | Upgradeable contracts are not initialized | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Conformance to Solidity naming conventions | 5 |
| [N-1] | Unused state variable | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-2] | State variables should be cached in stack variables rather than re-reading them from storage | 4 |
| [G-3] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 1 |
| [G-4] | use custom errors instead of revert strings | 11 |



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

## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description:

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `4` instances of this issue:**

- [Buggy](solidity/test_unprotected_upgradeable.sol#L19-L30) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [UpgradeableNoInitialized](solidity/test_unprotected_upgradeable.sol#L67-L74) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [Buggy2](solidity/test_unprotected_upgradeable.sol#L32-L38) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [UpgradeableNoDestruct](solidity/test_unprotected_upgradeable.sol#L76-L87) is an upgradeable contract that miss `__gap` to allow for new storage variables.

### recommendation:

It is considered a best practice in upgradeable contracts to include a
state variable named `__gap`. This `__gap` state variable will be used as a
reserved space for future upgrades. It allows adding new state variables
freely in the future without compromising the storage compatibility with
existing deployments.
The size of the __gap array is usually calculated so that the amount of
storage used by a contract always adds up to the same number (usually 50
storage slots).

```
contract Contract {
    ...
    
    # declare `__gap` variable at the end of all states
    uint256[50] private __gap;
}
```



### locations:
- solidity/test_unprotected_upgradeable.sol#L19-L30
- solidity/test_unprotected_upgradeable.sol#L67-L74
- solidity/test_unprotected_upgradeable.sol#L32-L38
- solidity/test_unprotected_upgradeable.sol#L76-L87

### severity:
Low

### category:
missing-gap-state-variable

## [Low] Use `disableInitializers` to prevent front-running on the initialize function

### description:

The implementation contracts behind a proxy can be initialized by any address. This is not a security problem in the sense that it impacts the system directly, as the attacker will not be able to cause any contract to self-destruct or modify any values in the proxy contracts. However, taking ownership of implementation contracts can open other attack vectors, like social engineering or phishing attacks.

More detail see [this OpenZeppelin docs](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializing_the_implementation_contract) and [this](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L47).


**There is `1` instance of this issue:**

- [Buggy2](solidity/test_unprotected_upgradeable.sol#L32-L38) is an upgradeable contract that does not protect its initialize functions: [Buggy2.initialize()](solidity/test_unprotected_upgradeable.sol#L34-L37)

### recommendation:

Use [disableInitializers](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L150-L165
) to prevent front-running on the initialize func-tion,
as it would make you deploy the smart contract again if someone
initializes it before you.

```
    constructor(){
        _disableInitializers();
    }
```



### locations:
- solidity/test_unprotected_upgradeable.sol#L32-L38

### severity:
Low

### category:
unprotected-upgrade-front-run

## [Low] Upgradeable contracts are not initialized

### description:

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There is `1` instance of this issue:**

- [UpgradeableNoInitialized](solidity/test_unprotected_upgradeable.sol#L67-L74) is an upgradeable contract that does not initialized

### recommendation:

Consider initializing function in the related section.

```
contract Contract {
    ...
    # 
    function initialize() public initializer {
        OwnableUpgradeable.__Ownable_init();
        __ReentrancyGuard_init();
    }

}
```


### locations:
- solidity/test_unprotected_upgradeable.sol#L67-L74

### severity:
Low

### category:
upgradeable-uninitialized

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `5` instances of this issue:**

- Contract [Not_Upgradeable](solidity/test_unprotected_upgradeable.sol#L65-L66) is not in CapWords

- Function [Fixed.other_function()](solidity/test_unprotected_upgradeable.sol#L60-L62) is not in mixedCase

- Variable [Fixed2.__gap](solidity/test_unprotected_upgradeable.sol#L91) is not in mixedCase

- Variable [Fixed.__gap](solidity/test_unprotected_upgradeable.sol#L45) is not in mixedCase

- Variable [Fixed3.__gap](solidity/test_unprotected_upgradeable.sol#L107) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_unprotected_upgradeable.sol#L65-L66
- solidity/test_unprotected_upgradeable.sol#L60-L62
- solidity/test_unprotected_upgradeable.sol#L91
- solidity/test_unprotected_upgradeable.sol#L45
- solidity/test_unprotected_upgradeable.sol#L107

### severity:
Informational

### category:
naming-convention

## [Informational] Unused state variable

### description:
Unused state variable.

**There are `3` instances of this issue:**

- [Fixed2.__gap](solidity/test_unprotected_upgradeable.sol#L91) is never used in [Fixed2](solidity/test_unprotected_upgradeable.sol#L89-L103)

- [Fixed3.__gap](solidity/test_unprotected_upgradeable.sol#L107) is never used in [Fixed3](solidity/test_unprotected_upgradeable.sol#L105-L122)

- [Fixed.__gap](solidity/test_unprotected_upgradeable.sol#L45) is never used in [Fixed](solidity/test_unprotected_upgradeable.sol#L43-L63)


### recommendation:
Remove unused state variables.

### locations:
- solidity/test_unprotected_upgradeable.sol#L91
- solidity/test_unprotected_upgradeable.sol#L107
- solidity/test_unprotected_upgradeable.sol#L45

### severity:
Informational

### category:
unused-state

## [Optimization] State variables only set in the constructor should be declared immutable

### description:

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There is `1` instance of this issue:**

- [UpgradeableNoInitialized.owner](solidity/test_unprotected_upgradeable.sol#L68) should be immutable 


### recommendation:
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations:
- solidity/test_unprotected_upgradeable.sol#L68

### severity:
Optimization

### category:
immutable-states

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

- [Fixed2.owner](solidity/test_unprotected_upgradeable.sol#L90) should be cached with local memory-based variable in [Fixed2.kill()](solidity/test_unprotected_upgradeable.sol#L99-L102), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L100)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L101)

- [Fixed3.owner](solidity/test_unprotected_upgradeable.sol#L106) should be cached with local memory-based variable in [Fixed3.kill()](solidity/test_unprotected_upgradeable.sol#L117-L120), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L118)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L119)

- [Buggy.owner](solidity/test_unprotected_upgradeable.sol#L20) should be cached with local memory-based variable in [Buggy.kill()](solidity/test_unprotected_upgradeable.sol#L26-L29), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L27)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L28)

- [Fixed.owner](solidity/test_unprotected_upgradeable.sol#L44) should be cached with local memory-based variable in [Fixed.kill()](solidity/test_unprotected_upgradeable.sol#L55-L58), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L56)
	- [selfdestruct(address)(owner)](solidity/test_unprotected_upgradeable.sol#L57)


### recommendation:

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations:
- solidity/test_unprotected_upgradeable.sol#L90
- solidity/test_unprotected_upgradeable.sol#L106
- solidity/test_unprotected_upgradeable.sol#L20
- solidity/test_unprotected_upgradeable.sol#L44

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


**There are `11` instances of this issue:**

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L84) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L35) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L51) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L23) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L118) should use custom error to save gas.

- [require(bool,string)(! _initializing,Initializable: contract is initializing)](solidity/test_unprotected_upgradeable.sol#L10) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L27) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L113) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/test_unprotected_upgradeable.sol#L95) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L56) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/test_unprotected_upgradeable.sol#L100) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_unprotected_upgradeable.sol#L84
- solidity/test_unprotected_upgradeable.sol#L35
- solidity/test_unprotected_upgradeable.sol#L51
- solidity/test_unprotected_upgradeable.sol#L23
- solidity/test_unprotected_upgradeable.sol#L118
- solidity/test_unprotected_upgradeable.sol#L10
- solidity/test_unprotected_upgradeable.sol#L27
- solidity/test_unprotected_upgradeable.sol#L113
- solidity/test_unprotected_upgradeable.sol#L95
- solidity/test_unprotected_upgradeable.sol#L56
- solidity/test_unprotected_upgradeable.sol#L100

### severity:
Optimization

### category:
use-custom-error
