## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | 2 |
| [L-1] | Upgradeable contracts are not initialized | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 1 |



## [Low] Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions

### description:

See [this](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps) link for a description of this storage variable. While some contracts may not currently be sub-classed, adding the variable now protects against forgetting to add it in the future.



**There are `2` instances of this issue:**

- [Buggy](solidity/test_missing_gap_state_variable.sol#L7-L9) is an upgradeable contract that miss `__gap` to allow for new storage variables.
- [Good](solidity/test_missing_gap_state_variable.sol#L15-L18) is an upgradeable contract that miss `__gap` to allow for new storage variables.

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
- solidity/test_missing_gap_state_variable.sol#L7-L9
- solidity/test_missing_gap_state_variable.sol#L15-L18

### severity:
Low

### category:
missing-gap-state-variable

## [Low] Upgradeable contracts are not initialized

### description:

Upgradeable contracts are initialized via an initializer function rather than by a constructor. 
Leaving such a contract uninitialized may lead to it being taken over by a malicious user


**There are `2` instances of this issue:**

- [Buggy](solidity/test_missing_gap_state_variable.sol#L7-L9) is an upgradeable contract that does not initialized
- [Good](solidity/test_missing_gap_state_variable.sol#L15-L18) is an upgradeable contract that does not initialized

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
- solidity/test_missing_gap_state_variable.sol#L7-L9
- solidity/test_missing_gap_state_variable.sol#L15-L18

### severity:
Low

### category:
upgradeable-uninitialized

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

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There is `1` instance of this issue:**

- Variable [Proxy.__gap](solidity/test_missing_gap_state_variable.sol#L12) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations:
- solidity/test_missing_gap_state_variable.sol#L12

### severity:
Informational

### category:
naming-convention
