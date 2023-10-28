## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Upgradeable contracts are not initialized | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Immutable variables used in upgradable contracts may cause DoS | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove or replace unused state variables | 1 |
| [G-1] | Setting the constructor to `payable` | 1 |
| [G-2] | Use `delete` to Clear Variables | 1 |
| [G-3] | State variables that could be declared constant | 1 |
| [G-4] | State variables that could be declared constant | 1 |



## [Medium] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There is `1` instance of this issue:**

- [ImmutableInUpgradeable](solidity/test_immutable_in_upgradeable.sol#L3-L13) is an upgradeable contract that miss `__gap` to allow for new storage variables.

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
- solidity/test_immutable_in_upgradeable.sol#L3-L13

### severity
Medium

### category
missing-gap-state-variable

### confidence
High

## [Low] Upgradeable contracts are not initialized

### description

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There is `1` instance of this issue:**

- [ImmutableInUpgradeable](solidity/test_immutable_in_upgradeable.sol#L3-L13) is an upgradeable contract that does not initialized

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
- solidity/test_immutable_in_upgradeable.sol#L3-L13

### severity
Low

### category
upgradeable-uninitialized

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
- 0.8.22

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

## [Informational] Immutable variables used in upgradable contracts may cause DoS

### description

The upgradeable contracts have some variables defined as immutable which are set during the constructor call.
This may probably work during the first deployment, but once the contract needs to be updated, the initialize
function needs to be called, and since the immutable variables are stored in the contract bytecode, 
the new upgradeable contracts will not retain these changes.
As a result, making the upgraded contract useless causing DoS.

References by OpenZeppelin for the Issue and Fix:
1. https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#avoid-initial-values-in-field-declarations
2. https://docs.openzeppelin.com/upgrades-plugins/1.x/faq#why-cant-i-use-immutable-variables


**There are `2` instances of this issue:**

- `immutable` keyword of [ImmutableInUpgradeable.a](solidity/test_immutable_in_upgradeable.sol#L4) should be removedÏ.

- `immutable` keyword of [ImmutableInUpgradeable.b](solidity/test_immutable_in_upgradeable.sol#L5) should be removedÏ.


### recommendation

Remove the `immutable` keyword and move the constructor logic to initialize function.


### locations
- solidity/test_immutable_in_upgradeable.sol#L4
- solidity/test_immutable_in_upgradeable.sol#L5

### severity
Informational

### category
immutable-in-upgradeable

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

- [ImmutableInUpgradeable.c](solidity/test_immutable_in_upgradeable.sol#L7) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/test_immutable_in_upgradeable.sol#L7

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- [ImmutableInUpgradeable.constructor()](solidity/test_immutable_in_upgradeable.sol#L9-L12) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/test_immutable_in_upgradeable.sol#L9-L12

### severity
Optimization

### category
payable-constructor

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


**There is `1` instance of this issue:**

- Should use `delete` statement instead of [b = address(0)](solidity/test_immutable_in_upgradeable.sol#L11)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/test_immutable_in_upgradeable.sol#L11

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [ImmutableInUpgradeable.c](solidity/test_immutable_in_upgradeable.sol#L7) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/test_immutable_in_upgradeable.sol#L7

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There is `1` instance of this issue:**

- [ImmutableInUpgradeable.c](solidity/test_immutable_in_upgradeable.sol#L7) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/test_immutable_in_upgradeable.sol#L7

### severity
Optimization

### category
state-should-be-constant

### confidence
High
