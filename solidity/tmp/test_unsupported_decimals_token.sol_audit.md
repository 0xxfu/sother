## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe calls to optional ERC20 functions:`decimals()`/`name()`/`symbol()` | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 3 |
| [G-1] | State variables that could be declared constant | 1 |



## [Low] Unsafe calls to optional ERC20 functions:`decimals()`/`name()`/`symbol()`

### description:

The`decimals()`/`name()`/`symbol()` functions are not a part of the 
[ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20), 
and was added later as an [optional extension](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/extensions/IERC20Metadata.sol). 
As such, some valid ERC20 tokens do not support this interface, 
so it is unsafe to blindly cast all tokens to this interface, 
and then call this function.



**There are `3` instances of this issue:**

- [a.decimals()](solidity/test_unsupported_decimals_token.sol#L13) should use `safe` call target function.

- [a.symbol()](solidity/test_unsupported_decimals_token.sol#L17) should use `safe` call target function.

- [a.name()](solidity/test_unsupported_decimals_token.sol#L21) should use `safe` call target function.


### recommendation:

Using `safe` call target function. see [this](https://github.com/boringcrypto/BoringSolidity/blob/78f4817d9c0d95fe9c45cd42e307ccd22cf5f4fc/contracts/libraries/BoringERC20.sol#L34-L56) to resolve the issue

For example:
```
    function safeDecimals(IERC20 token) internal view returns (uint8) {
        (bool success, bytes memory data) = address(token).staticcall(abi.encodeWithSelector(SIG_DECIMALS));
        return success && data.length == 32 ? abi.decode(data, (uint8)) : 18;
    }
```


### locations:
- solidity/test_unsupported_decimals_token.sol#L13
- solidity/test_unsupported_decimals_token.sol#L17
- solidity/test_unsupported_decimals_token.sol#L21

### severity:
Low

### category:
unsupported-decimals-token

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


**There are `3` instances of this issue:**

- `uint8 `[IERC20Metadata.decimals().](solidity/test_unsupported_decimals_token.sol#L6) should be used `uint256/int256`.

- `uint8 `[UnsupportDecimalsToken.bad(IERC20Metadata).](solidity/test_unsupported_decimals_token.sol#L12) should be used `uint256/int256`.

- `uint8 `[UnsupportDecimalsToken.notBad().](solidity/test_unsupported_decimals_token.sol#L24) should be used `uint256/int256`.


### recommendation:

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations:
- solidity/test_unsupported_decimals_token.sol#L6
- solidity/test_unsupported_decimals_token.sol#L12
- solidity/test_unsupported_decimals_token.sol#L24

### severity:
Optimization

### category:
smaller-uint-int

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [UnsupportDecimalsToken.token](solidity/test_unsupported_decimals_token.sol#L10) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### locations:
- solidity/test_unsupported_decimals_token.sol#L10

### severity:
Optimization

### category:
constable-states
