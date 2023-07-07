## Summary 

### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Variable names too similar | 7 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Multiple address `mappings` can be combined into a single `mapping` | 2 |
| [G-1] | Remove or replace unused state variables | 13 |



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

## [Informational] Variable names too similar

### description:
Detect variables with names that are too similar.

**There are `7` instances of this issue:**

- Variable `BadMappings.badMapping2` (solidity/test_multiple_address_mappings.sol#L6) is too similar to `BadMappings.badMapping5` (solidity/test_multiple_address_mappings.sol#L11)

- Variable `BadMappings.badMapping2` (solidity/test_multiple_address_mappings.sol#L6) is too similar to `BadMappings.badMapping4` (solidity/test_multiple_address_mappings.sol#L10)

- Variable `BadMappings.badMapping2` (solidity/test_multiple_address_mappings.sol#L6) is too similar to `BadMappings.badMapping3` (solidity/test_multiple_address_mappings.sol#L8)

- Variable `BadMappings.badMapping3` (solidity/test_multiple_address_mappings.sol#L8) is too similar to `BadMappings.badMapping4` (solidity/test_multiple_address_mappings.sol#L10)

- Variable `BadMappings.badMapping3` (solidity/test_multiple_address_mappings.sol#L8) is too similar to `BadMappings.badMapping5` (solidity/test_multiple_address_mappings.sol#L11)

- Variable `BadMappings.badMapping4` (solidity/test_multiple_address_mappings.sol#L10) is too similar to `BadMappings.badMapping5` (solidity/test_multiple_address_mappings.sol#L11)

- Variable `NotBadMappings.notBadMapping1` (solidity/test_multiple_address_mappings.sol#L19) is too similar to `NotBadMappings.notBadMapping2` (solidity/test_multiple_address_mappings.sol#L21)

#### Exploit scenario
Bob uses several variables with similar names. As a result, his code is difficult to review.

### recommendation:
Prevent variables from having similar names.

### locations:
- solidity/test_multiple_address_mappings.sol#L6
- solidity/test_multiple_address_mappings.sol#L6
- solidity/test_multiple_address_mappings.sol#L6
- solidity/test_multiple_address_mappings.sol#L8
- solidity/test_multiple_address_mappings.sol#L8
- solidity/test_multiple_address_mappings.sol#L10
- solidity/test_multiple_address_mappings.sol#L19

### severity:
Informational

### category:
similar-names

## [Optimization] Multiple address `mappings` can be combined into a single `mapping`

### description:

Saves a storage slot for the `mapping`. 
Depending on the circumstances and sizes of types, 
can avoid a `Gsset` (20000 gas) per `mapping` combined. Reads and subsequent writes can also 
be cheaper when a function requires both values and they both fit in the same storage slot. 
Finally, if both fields are accessed in the same function, can save `~42 gas` per access 
due to not having to recalculate the key’s `keccak256` hash (Gkeccak256 - 30 gas) and 
that calculation’s associated stack operations.


**There are `2` instances of this issue:**

- Following mappings should be combined into one:
	- `BadMappings.badMapping` (solidity/test_multiple_address_mappings.sol#L4)
	- `BadMappings.badMapping2` (solidity/test_multiple_address_mappings.sol#L6)
	- `BadMappings.badMapping3` (solidity/test_multiple_address_mappings.sol#L8)

- Following mappings should be combined into one:
	- `BadMappings.badMapping4` (solidity/test_multiple_address_mappings.sol#L10)
	- `BadMappings.badMapping5` (solidity/test_multiple_address_mappings.sol#L11)


### recommendation:

Multiple address `mappings` can be combined into a single mapping of 
an address to a struct, where appropriate.


### locations:
- solidity/test_multiple_address_mappings.sol#L4
- solidity/test_multiple_address_mappings.sol#L10

### severity:
Optimization

### category:
multiple-address-mappings

## [Optimization] Remove or replace unused state variables

### description:

Saves a storage slot. If the variable is assigned a non-zero value, saves Gsset (20000 gas). If it's assigned a zero value, saves Gsreset (2900 gas). If the variable remains unassigned, there is no gas savings unless the variable is public, in which case the compiler-generated non-payable getter deployment cost is saved. If the state variable is overriding an interface's public function, mark the variable as constant or immutable so that it does not use a storage slot


**There are `13` instances of this issue:**

- `BadMappings.badMapping` (solidity/test_multiple_address_mappings.sol#L4) is never used.
- `BadMappings.badMapping2` (solidity/test_multiple_address_mappings.sol#L6) is never used.
- `BadMappings.badMapping3` (solidity/test_multiple_address_mappings.sol#L8) is never used.
- `BadMappings.badMapping4` (solidity/test_multiple_address_mappings.sol#L10) is never used.
- `BadMappings.badMapping5` (solidity/test_multiple_address_mappings.sol#L11) is never used.
- `BadMappings.notBad1` (solidity/test_multiple_address_mappings.sol#L13) is never used.
- `BadMappings.notBad2` (solidity/test_multiple_address_mappings.sol#L14) is never used.
- `BadMappings.notBad3` (solidity/test_multiple_address_mappings.sol#L15) is never used.
- `NotBadMappings.notBadMapping1` (solidity/test_multiple_address_mappings.sol#L19) is never used.
- `NotBadMappings.notBadMapping2` (solidity/test_multiple_address_mappings.sol#L21) is never used.
- `NotBadMappings.notBad1` (solidity/test_multiple_address_mappings.sol#L22) is never used.
- `NotBadMappings.notBad2` (solidity/test_multiple_address_mappings.sol#L23) is never used.
- `NotBadMappings.notBad3` (solidity/test_multiple_address_mappings.sol#L24) is never used.

### recommendation:

Remove or replace the unused state variables


### locations:
- solidity/test_multiple_address_mappings.sol#L4
- solidity/test_multiple_address_mappings.sol#L6
- solidity/test_multiple_address_mappings.sol#L8
- solidity/test_multiple_address_mappings.sol#L10
- solidity/test_multiple_address_mappings.sol#L11
- solidity/test_multiple_address_mappings.sol#L13
- solidity/test_multiple_address_mappings.sol#L14
- solidity/test_multiple_address_mappings.sol#L15
- solidity/test_multiple_address_mappings.sol#L19
- solidity/test_multiple_address_mappings.sol#L21
- solidity/test_multiple_address_mappings.sol#L22
- solidity/test_multiple_address_mappings.sol#L23
- solidity/test_multiple_address_mappings.sol#L24

### severity:
Optimization

### category:
unused-state-variables
