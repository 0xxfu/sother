## Summary 

### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Void function | 1 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | NFT token do not comply with `ERC721`, breaking composability | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 2 |
| [N-2] | Unnecessary Public Function Modifier | 6 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Remove unused parameter variables | 3 |
| [G-1] | Empty blocks should be removed or emit something | 1 |



## [Medium] Void function

### description
Detect the call to a function that is not implemented

**There is `1` instance of this issue:**

- function:[AbstractERC721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_non_compliant_erc721.sol#L25-L29)is empty 

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
- solidity/tmp/test_non_compliant_erc721.sol#L25-L29

### severity
Medium

### category
void-function

### confidence
High

## [Low] NFT token do not comply with `ERC721`, breaking composability

### description

The issue is not comply with ERC721 itself. From [EIP721](https://eips.ethereum.org/EIPS/eip-721):
"Every ERC-721 compliant contract must implement the ERC721 and ERC165 interfaces (subject to “caveats” below):"

interface IDs are calculating by XORing together all the function signatures in the 
interface. Therefore, returning true for IERC721Enumerable and IERC721Metadata will 
not implicitly include IERC721.


**There are `3` instances of this issue:**

- [ERC165.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L10-L17) of `Bad721` is missing support:
	- [IERC721](solidity/tmp/test_non_compliant_erc721.sol#L5)

- [Bad721_2.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L35-L45) of `Bad721_2` is missing support:
	- [IERC721](solidity/tmp/test_non_compliant_erc721.sol#L5)

- [Bad721_3.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L49-L57) of `Bad721_3` is missing support:
	- [IERC721](solidity/tmp/test_non_compliant_erc721.sol#L5)
	- [IERC721Metadata](solidity/tmp/test_non_compliant_erc721.sol#L7)


### recommendation

Change supportedInterface function:

```
function supportsInterface(bytes4 interfaceId)
    external
    view
    virtual
    override(IERC165)
    returns (bool)
{
    return
    interfaceId == type(IERC721).interfaceId || 
    interfaceId == type(IERC721Enumerable).interfaceId ||
    interfaceId == type(IERC721Metadata).interfaceId ;
}
```


### locations
- solidity/tmp/test_non_compliant_erc721.sol#L10-L17
- solidity/tmp/test_non_compliant_erc721.sol#L35-L45
- solidity/tmp/test_non_compliant_erc721.sol#L49-L57

### severity
Low

### category
non-compliant-erc721

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

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `2` instances of this issue:**

- Contract [Bad721_2](solidity/tmp/test_non_compliant_erc721.sol#L34-L46) is not in CapWords

- Contract [Bad721_3](solidity/tmp/test_non_compliant_erc721.sol#L48-L58) is not in CapWords


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_non_compliant_erc721.sol#L34-L46
- solidity/tmp/test_non_compliant_erc721.sol#L48-L58

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `6` instances of this issue:**

- function:[ERC165.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L10-L17)is public and can be replaced with external 

- function:[AbstractERC721.ownerOf(uint256)](solidity/tmp/test_non_compliant_erc721.sol#L21-L23)is public and can be replaced with external 

- function:[AbstractERC721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_non_compliant_erc721.sol#L25-L29)is public and can be replaced with external 

- function:[Bad721_2.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L35-L45)is public and can be replaced with external 

- function:[Bad721_3.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L49-L57)is public and can be replaced with external 

- function:[NotBad721.supportsInterface(bytes4)](solidity/tmp/test_non_compliant_erc721.sol#L61-L72)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/test_non_compliant_erc721.sol#L10-L17
- solidity/tmp/test_non_compliant_erc721.sol#L21-L23
- solidity/tmp/test_non_compliant_erc721.sol#L25-L29
- solidity/tmp/test_non_compliant_erc721.sol#L35-L45
- solidity/tmp/test_non_compliant_erc721.sol#L49-L57
- solidity/tmp/test_non_compliant_erc721.sol#L61-L72

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There are `3` instances of this issue:**

- The param variables in [AbstractERC721.ownerOf(uint256)](solidity/tmp/test_non_compliant_erc721.sol#L21-L23) are unused.
	- [AbstractERC721.ownerOf(uint256).tokenId](solidity/tmp/test_non_compliant_erc721.sol#L21)

- The param variables in [AbstractERC721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_non_compliant_erc721.sol#L25-L29) are unused.
	- [AbstractERC721.safeTransferFrom(address,address,uint256).tokenId](solidity/tmp/test_non_compliant_erc721.sol#L28)
	- [AbstractERC721.safeTransferFrom(address,address,uint256).from](solidity/tmp/test_non_compliant_erc721.sol#L26)
	- [AbstractERC721.safeTransferFrom(address,address,uint256).to](solidity/tmp/test_non_compliant_erc721.sol#L27)

- The param variables in [AbstractERC721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_non_compliant_erc721.sol#L25-L29) are unused.
	- [AbstractERC721.safeTransferFrom(address,address,uint256).to](solidity/tmp/test_non_compliant_erc721.sol#L27)
	- [AbstractERC721.safeTransferFrom(address,address,uint256).tokenId](solidity/tmp/test_non_compliant_erc721.sol#L28)
	- [AbstractERC721.safeTransferFrom(address,address,uint256).from](solidity/tmp/test_non_compliant_erc721.sol#L26)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_non_compliant_erc721.sol#L21-L23
- solidity/tmp/test_non_compliant_erc721.sol#L25-L29
- solidity/tmp/test_non_compliant_erc721.sol#L25-L29

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Empty blocks should be removed or emit something

### description

The code should be refactored such that they no longer exist, or the block should do 
something useful, such as emitting an event or reverting. 
If the contract is meant to be extended, the contract should be `abstract` and the function 
signatures be added without any default implementation.


**There is `1` instance of this issue:**

- [AbstractERC721.safeTransferFrom(address,address,uint256)](solidity/tmp/test_non_compliant_erc721.sol#L25-L29) should removed or do something


### recommendation

Empty blocks should emit an event, or revert. 
If not, they can simply be removed to save gas upon deployment. 
This is valid for `receive()` functions, but also `constructors()`


### locations
- solidity/tmp/test_non_compliant_erc721.sol#L25-L29

### severity
Optimization

### category
empty-block

### confidence
High
