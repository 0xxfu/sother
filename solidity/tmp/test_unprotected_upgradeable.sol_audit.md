## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | Unprotected upgradeable contract | 1 |
| [H-1] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Use `disableInitializers` to prevent front-running on the initialize function | 1 |
| [L-1] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 4 |
| [L-2] | Upgradeable contracts are not initialized | 1 |
| [L-3] | Missing Event Setter | 13 |
| [L-4] | initialize method should has permission check | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 5 |
| [N-2] | .. | 10 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 1 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-2] | Using custom errors replace `require` or `assert` | 11 |
| [G-3] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 1 |
| [G-4] | Cache state variables instead of rereading | 4 |
| [G-5] | Use assembly to check for `address(0)` | 6 |
| [G-6] | Setting the constructor to `payable` | 5 |
| [G-7] | Shortening revert strings to fit in 32 `bytes` | 1 |
| [G-8] | Empty blocks should be removed or emit something | 1 |
| [G-9] | State variables that could be declared constant | 1 |



## [High] Unprotected upgradeable contract

### description
Detects logic contract that can be destructed.

**There is `1` instance of this issue:**

- [Buggy](solidity/tmp/test_unprotected_upgradeable.sol#L19-L30) is an upgradeable contract that does not protect its initialize functions: [Buggy.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L22-L25). Anyone can delete the contract with: [Buggy.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L26-L29)
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


### recommendation
Add a constructor to ensure `initialize` cannot be called on the logic contract.

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L19-L30

### severity
High

### category
unprotected-upgrade

### confidence
High

## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [Initializable._initializing](solidity/tmp/test_unprotected_upgradeable.sol#L3) not initialized and not written in contract but be used in contract

#### Exploit scenario

```solidity
    struct BalancesStruct{
        address owner;
        array[]] balances;
    }
    array[] public stackBalance;

    function remove() internal{
         delete stackBalance[msg.sender];
    }
```
`remove` deletes an item of `stackBalance`.
The array `balances` is never deleted, so `remove` does not work as intended.

### recommendation
Use a lock mechanism instead of a deletion to disable structure containing a array.

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L3

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There is `1` instance of this issue:**

- function:[Fixed.other_function()](solidity/tmp/test_unprotected_upgradeable.sol#L60-L62)is empty 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Implement the function

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L60-L62

### severity
Medium

### category
void-function

### confidence
High

## [Low] Use `disableInitializers` to prevent front-running on the initialize function

### description

The implementation contracts behind a proxy can be initialized by any address. This is not a security problem in the sense that it impacts the system directly, as the attacker will not be able to cause any contract to self-destruct or modify any values in the proxy contracts. However, taking ownership of implementation contracts can open other attack vectors, like social engineering or phishing attacks.

More detail see [this OpenZeppelin docs](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#initializing_the_implementation_contract) and [this](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L47).


**There is `1` instance of this issue:**

- [Buggy2](solidity/tmp/test_unprotected_upgradeable.sol#L32-L38) is an upgradeable contract that does not protect its initialize functions: [Buggy2.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L34-L37)

### recommendation

Use [disableInitializers](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/62e2b8811b3cd80eb189aee7ae6764e937f8647b/contracts/proxy/utils/Initializable.sol#L150-L165) 
to prevent front-running on the initialize function, as it would make you deploy the smart contract 
again if someone initializes it before you.

```
    constructor(){
        _disableInitializers();
    }
```



### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L32-L38

### severity
Low

### category
unprotected-upgrade-front-run

### confidence
High

## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `4` instances of this issue:**

- [Buggy](solidity/tmp/test_unprotected_upgradeable.sol#L19-L30) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [Buggy2](solidity/tmp/test_unprotected_upgradeable.sol#L32-L38) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [UpgradeableNoInitialized](solidity/tmp/test_unprotected_upgradeable.sol#L67-L74) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [UpgradeableNoDestruct](solidity/tmp/test_unprotected_upgradeable.sol#L76-L87) is an upgradeable contract that miss `__gap` to allow for new storage variables.

### recommendation

It is considered a best practice in upgradeable contracts to include a
state variable named `__gap`. This `__gap` state variable will be used as a
reserved space for future upgrades. It allows adding new state variables
freely in the future without compromising the storage compatibility with
existing deployments.
The size of the `__gap` array is usually calculated so that the amount of
storage used by a contract always adds up to the same number (usually 50
storage slots).

```
contract Contract {
    ...
    
    # declare `__gap` variable at the end of all states
    uint256[50] private __gap;
}
```



### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L19-L30
- solidity/tmp/test_unprotected_upgradeable.sol#L32-L38
- solidity/tmp/test_unprotected_upgradeable.sol#L67-L74
- solidity/tmp/test_unprotected_upgradeable.sol#L76-L87

### severity
Low

### category
missing-gap-state-variable

### confidence
High

## [Low] Upgradeable contracts are not initialized

### description

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There is `1` instance of this issue:**

- [UpgradeableNoInitialized](solidity/tmp/test_unprotected_upgradeable.sol#L67-L74) is an upgradeable contract that does not initialized

### recommendation

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


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L67-L74

### severity
Low

### category
upgradeable-uninitialized

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `13` instances of this issue:**

- Setter function [Buggy.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L22-L25) does not emit an event

- Setter function [Buggy.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L26-L29) does not emit an event

- Setter function [Buggy2.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L34-L37) does not emit an event

- Setter function [Fixed.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L46-L48) does not emit an event

- Setter function [Fixed.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L50-L54) does not emit an event

- Setter function [Fixed.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L55-L58) does not emit an event

- Setter function [UpgradeableNoInitialized.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L70-L72) does not emit an event

- Setter function [UpgradeableNoDestruct.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L79-L81) does not emit an event

- Setter function [UpgradeableNoDestruct.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L83-L86) does not emit an event

- Setter function [Fixed2.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L94-L97) does not emit an event

- Setter function [Fixed2.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L99-L102) does not emit an event

- Setter function [Fixed3.initialize()](solidity/tmp/test_unprotected_upgradeable.sol#L112-L115) does not emit an event

- Setter function [Fixed3.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L117-L120) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L22-L25
- solidity/tmp/test_unprotected_upgradeable.sol#L26-L29
- solidity/tmp/test_unprotected_upgradeable.sol#L34-L37
- solidity/tmp/test_unprotected_upgradeable.sol#L46-L48
- solidity/tmp/test_unprotected_upgradeable.sol#L50-L54
- solidity/tmp/test_unprotected_upgradeable.sol#L55-L58
- solidity/tmp/test_unprotected_upgradeable.sol#L70-L72
- solidity/tmp/test_unprotected_upgradeable.sol#L79-L81
- solidity/tmp/test_unprotected_upgradeable.sol#L83-L86
- solidity/tmp/test_unprotected_upgradeable.sol#L94-L97
- solidity/tmp/test_unprotected_upgradeable.sol#L99-L102
- solidity/tmp/test_unprotected_upgradeable.sol#L112-L115
- solidity/tmp/test_unprotected_upgradeable.sol#L117-L120

### severity
Low

### category
pess-event-setter

### confidence
Medium

## [Low] initialize method should has permission check

### description
initialize method should has permission check

**There is `1` instance of this issue:**

- Condition variable is not initialized found in [Initializable._disableInitializers()](solidity/tmp/test_unprotected_upgradeable.sol#L9-L14)


### recommendation
initialize method should has permission check

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L9-L14

### severity
Low

### category
initialize-permission

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

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `5` instances of this issue:**

- Variable [Fixed.__gap](solidity/tmp/test_unprotected_upgradeable.sol#L45) is not in mixedCase

- Function [Fixed.other_function()](solidity/tmp/test_unprotected_upgradeable.sol#L60-L62) is not in mixedCase

- Contract [Not_Upgradeable](solidity/tmp/test_unprotected_upgradeable.sol#L65-L66) is not in CapWords

- Variable [Fixed2.__gap](solidity/tmp/test_unprotected_upgradeable.sol#L91) is not in mixedCase

- Variable [Fixed3.__gap](solidity/tmp/test_unprotected_upgradeable.sol#L107) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L45
- solidity/tmp/test_unprotected_upgradeable.sol#L60-L62
- solidity/tmp/test_unprotected_upgradeable.sol#L65-L66
- solidity/tmp/test_unprotected_upgradeable.sol#L91
- solidity/tmp/test_unprotected_upgradeable.sol#L107

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] ..

### description
..

**There are `10` instances of this issue:**

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L23)

- require() missing error messages
	 - [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L27)

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L35)

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L51)

- require() missing error messages
	 - [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L56)

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L84)

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L95)

- require() missing error messages
	 - [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L100)

- require() missing error messages
	 - [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L113)

- require() missing error messages
	 - [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L118)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L23
- solidity/tmp/test_unprotected_upgradeable.sol#L27
- solidity/tmp/test_unprotected_upgradeable.sol#L35
- solidity/tmp/test_unprotected_upgradeable.sol#L51
- solidity/tmp/test_unprotected_upgradeable.sol#L56
- solidity/tmp/test_unprotected_upgradeable.sol#L84
- solidity/tmp/test_unprotected_upgradeable.sol#L95
- solidity/tmp/test_unprotected_upgradeable.sol#L100
- solidity/tmp/test_unprotected_upgradeable.sol#L113
- solidity/tmp/test_unprotected_upgradeable.sol#L118

### severity
Informational

### category
error-msg

### confidence
Medium

## [Optimization] State variables only set in the constructor should be declared immutable

### description

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There is `1` instance of this issue:**

- [UpgradeableNoInitialized.owner](solidity/tmp/test_unprotected_upgradeable.sol#L68) should be immutable 


### recommendation
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L68

### severity
Optimization

### category
immutable-states

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- [Initializable._disableInitializers()](solidity/tmp/test_unprotected_upgradeable.sol#L9-L14) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L9-L14

### severity
Optimization

### category
internal-function-to-inline

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `11` instances of this issue:**

- [require(bool,string)(! _initializing,"Initializable: contract is initializing")](solidity/tmp/test_unprotected_upgradeable.sol#L10) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L23) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L27) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L35) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L51) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L56) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L84) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L95) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L100) should use custom error to save gas.

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L113) should use custom error to save gas.

- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L118) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L10
- solidity/tmp/test_unprotected_upgradeable.sol#L23
- solidity/tmp/test_unprotected_upgradeable.sol#L27
- solidity/tmp/test_unprotected_upgradeable.sol#L35
- solidity/tmp/test_unprotected_upgradeable.sol#L51
- solidity/tmp/test_unprotected_upgradeable.sol#L56
- solidity/tmp/test_unprotected_upgradeable.sol#L84
- solidity/tmp/test_unprotected_upgradeable.sol#L95
- solidity/tmp/test_unprotected_upgradeable.sol#L100
- solidity/tmp/test_unprotected_upgradeable.sol#L113
- solidity/tmp/test_unprotected_upgradeable.sol#L118

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There is `1` instance of this issue:**

- `uint8 `[Initializable._initialized](solidity/tmp/test_unprotected_upgradeable.sol#L2) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L2

### severity
Optimization

### category
smaller-uint-int

### confidence
High

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `4` instances of this issue:**

- [Buggy.owner](solidity/tmp/test_unprotected_upgradeable.sol#L20) should be cached with local memory-based variable in [Buggy.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L26-L29), It is called more than once:
	- [selfdestruct(address)(owner)](solidity/tmp/test_unprotected_upgradeable.sol#L28)
	- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L27)

- [Fixed.owner](solidity/tmp/test_unprotected_upgradeable.sol#L44) should be cached with local memory-based variable in [Fixed.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L55-L58), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L56)
	- [selfdestruct(address)(owner)](solidity/tmp/test_unprotected_upgradeable.sol#L57)

- [Fixed2.owner](solidity/tmp/test_unprotected_upgradeable.sol#L90) should be cached with local memory-based variable in [Fixed2.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L99-L102), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L100)
	- [selfdestruct(address)(owner)](solidity/tmp/test_unprotected_upgradeable.sol#L101)

- [Fixed3.owner](solidity/tmp/test_unprotected_upgradeable.sol#L106) should be cached with local memory-based variable in [Fixed3.kill()](solidity/tmp/test_unprotected_upgradeable.sol#L117-L120), It is called more than once:
	- [require(bool)(msg.sender == owner)](solidity/tmp/test_unprotected_upgradeable.sol#L118)
	- [selfdestruct(address)(owner)](solidity/tmp/test_unprotected_upgradeable.sol#L119)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L20
- solidity/tmp/test_unprotected_upgradeable.sol#L44
- solidity/tmp/test_unprotected_upgradeable.sol#L90
- solidity/tmp/test_unprotected_upgradeable.sol#L106

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There are `6` instances of this issue:**

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L23) should use assembly to check for `address(0)`

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L35) should use assembly to check for `address(0)`

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L51) should use assembly to check for `address(0)`

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L84) should use assembly to check for `address(0)`

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L95) should use assembly to check for `address(0)`

- [require(bool)(owner == address(0))](solidity/tmp/test_unprotected_upgradeable.sol#L113) should use assembly to check for `address(0)`


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
- solidity/tmp/test_unprotected_upgradeable.sol#L23
- solidity/tmp/test_unprotected_upgradeable.sol#L35
- solidity/tmp/test_unprotected_upgradeable.sol#L51
- solidity/tmp/test_unprotected_upgradeable.sol#L84
- solidity/tmp/test_unprotected_upgradeable.sol#L95
- solidity/tmp/test_unprotected_upgradeable.sol#L113

### severity
Optimization

### category
zero-address-optimization

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `5` instances of this issue:**

- [Fixed.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L46-L48) should be set to `payable` 

- [UpgradeableNoInitialized.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L70-L72) should be set to `payable` 

- [UpgradeableNoDestruct.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L79-L81) should be set to `payable` 

- [Fixed2.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L92) should be set to `payable` 

- [Fixed3.constructor()](solidity/tmp/test_unprotected_upgradeable.sol#L108-L110) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L46-L48
- solidity/tmp/test_unprotected_upgradeable.sol#L70-L72
- solidity/tmp/test_unprotected_upgradeable.sol#L79-L81
- solidity/tmp/test_unprotected_upgradeable.sol#L92
- solidity/tmp/test_unprotected_upgradeable.sol#L108-L110

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] Shortening revert strings to fit in 32 `bytes`

### description

In Solidity, the size of a string is not fixed and depends on the length of the string. 
Each character in a string requires 2 `bytes` of storage. 
Additionally, there is an overhead of 32 `bytes` to store the length of the string.

Shortening revert strings to fit in 32 bytes will decrease deployment time gas 
and will decrease runtime gas when the revert condition is met.


**There is `1` instance of this issue:**

- [require(bool,string)(! _initializing,"Initializable: contract is initializing")](solidity/tmp/test_unprotected_upgradeable.sol#L10) should be shortened strings to fit in 32 `bytes` (16 characters).


### recommendation

Shortening revert strings to fit in 32 `bytes`


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L10

### severity
Optimization

### category
revert-long-strings

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [Fixed.other_function()](solidity/tmp/test_unprotected_upgradeable.sol#L60-L62) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L60-L62

### severity
Optimization

### category
empty-block

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [Initializable._initializing](solidity/tmp/test_unprotected_upgradeable.sol#L3) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_unprotected_upgradeable.sol#L3

### severity
Optimization

### category
state-should-be-constant

### confidence
High
