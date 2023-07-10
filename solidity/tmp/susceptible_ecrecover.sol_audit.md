## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | return value of 0 from `ecrecover` not checked | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Direct usage of `ecrecover` allows signature malleability | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 4 |
| [G-1] | Using custom errors replace `require` or `assert` | 1 |
| [G-2] | Use assembly to check for `address(0)` | 2 |



## [High] return value of 0 from `ecrecover` not checked

### description:

The solidity function `ecrecover` is used, however the error result of 0 is not checked for.
See documentation:
https://docs.soliditylang.org/en/latest/units-and-global-variables.html#mathematical-and-cryptographic-functions
> recover the address associated with the public key from elliptic curve signature or return zero on error.  


**There are `2` instances of this issue:**

- [ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L8) should check the result from `ecrecover` isn't `0`.

- [result = ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L17) should check the result from `ecrecover` isn't `0`.


### recommendation:

Verify that the result from `ecrecover` isn't `0`


### locations:
- solidity/susceptible_ecrecover.sol#L8
- solidity/susceptible_ecrecover.sol#L17

### severity:
High

### category:
unchecked-ecrecover

## [Low] Direct usage of `ecrecover` allows signature malleability

### description:

The `ecrecover` function is used to verify and execute Meta transactions. 
The built-in EVM precompile `ecrecover` is susceptible to signature malleability 
(because of non-unique s and v values) which could lead to replay attacks 
(references: https://swcregistry.io/docs/SWC-117, https://swcregistry.io/docs/SWC-121 and https://medium.com/cryptronics/signature-replay-vulnerabilities-in-smart-contracts-3b6f7596df57).

While this is not exploitable for replay attacks in the current implementation because of the use of nonces, this may become a vulnerability if used elsewhere.


**There are `4` instances of this issue:**

- [ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L8) should OpenZeppelin’s ECDSA instead of the built-in function.

- [result = ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L17) should OpenZeppelin’s ECDSA instead of the built-in function.

- [result = ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L27) should OpenZeppelin’s ECDSA instead of the built-in function.

- [result = ecrecover(bytes32,uint8,bytes32,bytes32)(digest,v,r,s)](solidity/susceptible_ecrecover.sol#L38) should OpenZeppelin’s ECDSA instead of the built-in function.


### recommendation:

Consider using [OpenZeppelin’s ECDSA library](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol) 
(which prevents this malleability) instead of the built-in function.


### locations:
- solidity/susceptible_ecrecover.sol#L8
- solidity/susceptible_ecrecover.sol#L17
- solidity/susceptible_ecrecover.sol#L27
- solidity/susceptible_ecrecover.sol#L38

### severity:
Low

### category:
susceptible-ecrecover

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

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description:

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `4` instances of this issue:**

- `uint8 `[SusceptibleEcrecover.bad(bytes32,uint8,bytes32,bytes32).v](solidity/susceptible_ecrecover.sol#L4) should be used `uint256/int256`.

- `uint8 `[SusceptibleEcrecover.bad2(bytes32,uint8,bytes32,bytes32).v](solidity/susceptible_ecrecover.sol#L13) should be used `uint256/int256`.

- `uint8 `[SusceptibleEcrecover.notBad(bytes32,uint8,bytes32,bytes32).v](solidity/susceptible_ecrecover.sol#L23) should be used `uint256/int256`.

- `uint8 `[SusceptibleEcrecover.notBad2(bytes32,uint8,bytes32,bytes32).v](solidity/susceptible_ecrecover.sol#L34) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/susceptible_ecrecover.sol#L4
- solidity/susceptible_ecrecover.sol#L13
- solidity/susceptible_ecrecover.sol#L23
- solidity/susceptible_ecrecover.sol#L34

### severity:
Optimization

### category:
smaller-uint-int

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(result != address(0),address err)](solidity/susceptible_ecrecover.sol#L28) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/susceptible_ecrecover.sol#L28

### severity:
Optimization

### category:
use-custom-error

## [Optimization] Use assembly to check for `address(0)`

### description:

[Inline Assembly](https://docs.soliditylang.org/en/latest/assembly.html) more gas efficient and [Saving Gas with Simple Inlining](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/).



**There are `2` instances of this issue:**

- [require(bool,string)(result != address(0),address err)](solidity/susceptible_ecrecover.sol#L28) should use assembly to check for `address(0)`

- [result == address(0)](solidity/susceptible_ecrecover.sol#L39) should use assembly to check for `address(0)`


### recommendation:

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


### locations:
- solidity/susceptible_ecrecover.sol#L28
- solidity/susceptible_ecrecover.sol#L39

### severity:
Optimization

### category:
zero-address-optimization
