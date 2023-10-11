## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 3 |
| [L-1] | Upgradeable contracts are not initialized | 3 |
| [L-2] | Contracts are not using their OZ Upgradeable counterparts | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |



## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `3` instances of this issue:**

- [ERC20Upgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L5) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [BadUpgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L7) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [NotBadUpgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L9) is an upgradeable contract that miss `__gap` to allow for new storage variables.

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
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L5
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L7
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L9

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


**There are `3` instances of this issue:**

- [ERC20Upgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L5) is an upgradeable contract that does not initialized
- [BadUpgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L7) is an upgradeable contract that does not initialized
- [NotBadUpgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L9) is an upgradeable contract that does not initialized

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
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L5
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L7
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L9

### severity
Low

### category
upgradeable-uninitialized

### confidence
High

## [Low] Contracts are not using their OZ Upgradeable counterparts

### description

The non-upgradeable standard version of OpenZeppelin’s library are inherited 
by the contracts. It would be safer to use the upgradeable versions of the library contracts 
to avoid unexpected behaviour.


**There is `1` instance of this issue:**

- [BadUpgradeable](solidity/tmp/test_unused_upgradeable_counterparts.sol#L7) should inherit upgradeable contract instead of following non-upgradeable contracts:
	- [ERC20](solidity/tmp/test_unused_upgradeable_counterparts.sol#L3)


### recommendation

Where applicable, use the contracts from `@openzeppelin/contracts-upgradeable` instead 
of `@openzeppelin/contracts`. See https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/tree/master/contracts 
for list of available upgradeable contracts


### locations
- solidity/tmp/test_unused_upgradeable_counterparts.sol#L7

### severity
Low

### category
unused-upgradeable-counterparts

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
