## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | NFT doesn't handle hard forks | 1 |
| [L-1] | `tokenURI()` does not follow EIP-721 | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | .. | 1 |
| [N-2] | Unnecessary Public Function Modifier | 2 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 1 |
| [G-1] | Cache state variables instead of rereading | 2 |
| [G-2] | Remove unused parameter variables | 1 |
| [G-3] | State variables that could be declared constant | 2 |
| [G-4] | State variables that could be declared constant | 2 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There are `2` instances of this issue:**

- state variable: [UnprotectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L9) not initialized and not written in contract but be used in contract

- state variable: [ProtectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L26) not initialized and not written in contract but be used in contract

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
- solidity/tmp/test_unprotected_nft_fork.sol#L9
- solidity/tmp/test_unprotected_nft_fork.sol#L26

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Low] NFT doesn't handle hard forks

### description

When there are hard forks, users often have to go through 
[many hoops](https://twitter.com/elerium115/status/1558471934924431363) to ensure that 
they control ownership on every fork. Consider adding `require(1 == chain.chainId)`, 
or the chain ID of whichever chain you prefer, to the functions below, 
or at least include the chain ID in the URI, 
so that there is no confusion about which chain is the owner of the NFT.



**There is `1` instance of this issue:**

- Protect NFT from copying in forks at the beginning of :
[UnprotectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L11-L21)

### recommendation

Add the following check:
```
if(block.chainid != 1) { 
    revert(); 
}
```


### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L11-L21

### severity
Low

### category
unprotected-nft-fork

### confidence
High

## [Low] `tokenURI()` does not follow EIP-721

### description

The [EIP](https://eips.ethereum.org/EIPS/eip-721) states that `tokenURI()` 
"Throws if `_tokenId` is not a valid NFT", which the code below does not do. 
f the NFT has not yet been minted, `tokenURI()` should revert.



**There are `2` instances of this issue:**

- Check if `tokenId` has minted at the beginning of :
[UnprotectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L11-L21)
- Check if `tokenId` has minted at the beginning of :
[ProtectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L28-L39)

### recommendation

Check if `tokenId` has minted at the beginning of `tokenURI` function.

For example:
```
    function tokenURI(uint256 tokenId) public view virtual returns (string memory) {
        if (_owners[tokenId] == address(0)) {
            revert("err");
        }

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 ? string.concat(baseURI, tokenId.toString()) : "";
    }
```


### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L11-L21
- solidity/tmp/test_unprotected_nft_fork.sol#L28-L39

### severity
Low

### category
unchecked-token-id

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

## [Informational] ..

### description
..

**There is `1` instance of this issue:**

- require() missing error messages
	 - [require(bool)(1 == block.chainid)](solidity/tmp/test_unprotected_nft_fork.sol#L34)

#### Exploit scenario
..

### recommendation
..

### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L34

### severity
Informational

### category
error-msg

### confidence
Medium

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `2` instances of this issue:**

- function:[UnprotectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L11-L21)is public and can be replaced with external 

- function:[ProtectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L28-L39)is public and can be replaced with external 

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
- solidity/tmp/test_unprotected_nft_fork.sol#L11-L21
- solidity/tmp/test_unprotected_nft_fork.sol#L28-L39

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool)(1 == block.chainid)](solidity/tmp/test_unprotected_nft_fork.sol#L34) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L34

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `2` instances of this issue:**

- [UnprotectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L9) should be cached with local memory-based variable in [UnprotectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L11-L21), It is called more than once:
	- [string.concat(baseURI,tokenId.toString())](solidity/tmp/test_unprotected_nft_fork.sol#L17-L20)
	- [bytes(baseURI).length > 0](solidity/tmp/test_unprotected_nft_fork.sol#L17-L20)

- [ProtectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L26) should be cached with local memory-based variable in [ProtectedNFTFork.tokenURI(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L28-L39), It is called more than once:
	- [bytes(baseURI).length > 0](solidity/tmp/test_unprotected_nft_fork.sol#L35-L38)
	- [string.concat(baseURI,tokenId.toString())](solidity/tmp/test_unprotected_nft_fork.sol#L35-L38)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L9
- solidity/tmp/test_unprotected_nft_fork.sol#L26

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The param variables in [Strings.toString(uint256)](solidity/tmp/test_unprotected_nft_fork.sol#L2-L4) are unused.
	- [Strings.toString(uint256).value](solidity/tmp/test_unprotected_nft_fork.sol#L2)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L2-L4

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnprotectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L9) should be constant 

- [ProtectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L26) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L9
- solidity/tmp/test_unprotected_nft_fork.sol#L26

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `2` instances of this issue:**

- [UnprotectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L9) should be constant

- [ProtectedNFTFork.baseURI](solidity/tmp/test_unprotected_nft_fork.sol#L26) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/test_unprotected_nft_fork.sol#L9
- solidity/tmp/test_unprotected_nft_fork.sol#L26

### severity
Optimization

### category
state-should-be-constant

### confidence
High
