## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | NFT doesn't handle hard forks | 3 |
| [L-1] | `tokenURI()` does not follow EIP-721 | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Unnecessary Public Function Modifier | 3 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-1] | Remove or replace unused state variables | 1 |
| [G-2] | Remove unused parameter variables | 1 |
| [G-3] | Use assembly to check for `address(0)` | 2 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There are `2` instances of this issue:**

- state variable: [NotBad0._owners](solidity/tmp/test_unchecked_token_id.sol#L16) not initialized and not written in contract but be used in contract

- state variable: [NotBad1._owners](solidity/tmp/test_unchecked_token_id.sol#L34) not initialized and not written in contract but be used in contract

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
- solidity/tmp/test_unchecked_token_id.sol#L16
- solidity/tmp/test_unchecked_token_id.sol#L34

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



**There are `3` instances of this issue:**

- Protect NFT from copying in forks at the beginning of :
[Bad.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L4-L12)
- Protect NFT from copying in forks at the beginning of :
[NotBad0.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L18-L30)
- Protect NFT from copying in forks at the beginning of :
[NotBad1.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L36-L46)

### recommendation

Add the following check:
```
if(block.chainid != 1) { 
    revert(); 
}
```


### locations
- solidity/tmp/test_unchecked_token_id.sol#L4-L12
- solidity/tmp/test_unchecked_token_id.sol#L18-L30
- solidity/tmp/test_unchecked_token_id.sol#L36-L46

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



**There is `1` instance of this issue:**

- Check if `tokenId` has minted at the beginning of :
[Bad.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L4-L12)

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
- solidity/tmp/test_unchecked_token_id.sol#L4-L12

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

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `3` instances of this issue:**

- function:[Bad.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L4-L12)is public and can be replaced with external 

- function:[NotBad0.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L18-L30)is public and can be replaced with external 

- function:[NotBad1.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L36-L46)is public and can be replaced with external 

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
- solidity/tmp/test_unchecked_token_id.sol#L4-L12
- solidity/tmp/test_unchecked_token_id.sol#L18-L30
- solidity/tmp/test_unchecked_token_id.sol#L36-L46

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- [NotBad1._requireMinted(uint256)](solidity/tmp/test_unchecked_token_id.sol#L48-L52) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/tmp/test_unchecked_token_id.sol#L48-L52

### severity
Optimization

### category
internal-function-to-inline

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

- [Bad._owners](solidity/tmp/test_unchecked_token_id.sol#L2) is never used.

### recommendation

Remove or replace the unused state variables


### locations
- solidity/tmp/test_unchecked_token_id.sol#L2

### severity
Optimization

### category
unused-state-variables

### confidence
High

## [Optimization] Remove unused parameter variables

### description

Unused parameters variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 



**There is `1` instance of this issue:**

- The param variables in [Bad.tokenURI(uint256)](solidity/tmp/test_unchecked_token_id.sol#L4-L12) are unused.
	- [Bad.tokenURI(uint256).tokenId](solidity/tmp/test_unchecked_token_id.sol#L4)


### recommendation

Remove the unused parameter variables.


### locations
- solidity/tmp/test_unchecked_token_id.sol#L4-L12

### severity
Optimization

### category
unused-parameter

### confidence
High

## [Optimization] Use assembly to check for `address(0)`

### description

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There are `2` instances of this issue:**

- [_owners[tokenId] == address(0)](solidity/tmp/test_unchecked_token_id.sol#L24) should use assembly to check for `address(0)`

- [_owners[tokenId] == address(0)](solidity/tmp/test_unchecked_token_id.sol#L49) should use assembly to check for `address(0)`


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
- solidity/tmp/test_unchecked_token_id.sol#L24
- solidity/tmp/test_unchecked_token_id.sol#L49

### severity
Optimization

### category
zero-address-optimization

### confidence
High
