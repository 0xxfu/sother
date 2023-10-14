## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 6 |
| [M-1] | Lack of slippage protection can lead to significant loss of user funds | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Variable names too similar | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 8 |
| [G-1] | Cache state variables instead of rereading | 2 |
| [G-2] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-3] | State variables that could be declared constant | 1 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [LackSlippageProtection.positionManager](solidity/test_lack_slippage_protection.sol#L73) not initialized and not written in contract but be used in contract

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
- solidity/test_lack_slippage_protection.sol#L73

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There are `6` instances of this issue:**

- [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128)](solidity/test_lack_slippage_protection.sol#L75-L121) ignores return value by [positionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams({tokenId:tokenId,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L101-L110)

- [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128)](solidity/test_lack_slippage_protection.sol#L75-L121) ignores return value by [positionManager.decreaseLiquidity(INonfungiblePositionManager.DecreaseLiquidityParams({tokenId:tokenId,liquidity:liquidity,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L112-L120)

- [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128)](solidity/test_lack_slippage_protection.sol#L75-L121) ignores return value by [positionManager.mint(INonfungiblePositionManager.MintParams({token0:token0,token1:token1,fee:0,tickLower:tickLower,tickUpper:tickUpper,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,recipient:address(this),deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L85-L99)

- [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256)](solidity/test_lack_slippage_protection.sol#L123-L170) ignores return value by [positionManager.mint(INonfungiblePositionManager.MintParams({token0:token0,token1:token1,fee:0,tickLower:tickLower,tickUpper:tickUpper,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:100,amount1Min:100,recipient:address(this),deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L134-L148)

- [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256)](solidity/test_lack_slippage_protection.sol#L123-L170) ignores return value by [positionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams({tokenId:tokenId,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:amountMin,amount1Min:amountMin,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L150-L159)

- [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256)](solidity/test_lack_slippage_protection.sol#L123-L170) ignores return value by [positionManager.decreaseLiquidity(INonfungiblePositionManager.DecreaseLiquidityParams({tokenId:tokenId,liquidity:liquidity,amount0Min:amountMin,amount1Min:amountMin,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L161-L169)

#### Exploit scenario

```solidity
contract MyConc{
    using SafeMath for uint;   
    function my_func(uint a, uint b) public{
        a.add(b);
    }
}
```
`MyConc` calls `add` of `SafeMath`, but does not store the result in `a`. As a result, the computation has no effect.

### recommendation
Ensure that all the return values of the function calls are used.

### locations
- solidity/test_lack_slippage_protection.sol#L75-L121
- solidity/test_lack_slippage_protection.sol#L75-L121
- solidity/test_lack_slippage_protection.sol#L75-L121
- solidity/test_lack_slippage_protection.sol#L123-L170
- solidity/test_lack_slippage_protection.sol#L123-L170
- solidity/test_lack_slippage_protection.sol#L123-L170

### severity
Medium

### category
unused-return

### confidence
Medium

## [Medium] Lack of slippage protection can lead to significant loss of user funds

### description

Strategy contracts interact with Uniswap V3 in multiple areas of the code. 
However, none of these interactions contain any slippage control, 
meaning that the contract, and by extension all users who hold shares, 
can lose significant value due to illiquid pools or MEV sandwich attacks every time 
any of the relevant functions are called.

In each of the below instances, a call to Uniswap V3 is made and `amount0Min` and `amount1Min` 
are each set to 0, which allows for **100% slippage tolerance**. 
This means that the action could lead to the caller losing up to 100% of their tokens due to slippage.


**There are `3` instances of this issue:**

- [positionManager.mint(INonfungiblePositionManager.MintParams({token0:token0,token1:token1,fee:0,tickLower:tickLower,tickUpper:tickUpper,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,recipient:address(this),deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L85-L99) lack of slippage protection.

- [positionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams({tokenId:tokenId,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L101-L110) lack of slippage protection.

- [positionManager.decreaseLiquidity(INonfungiblePositionManager.DecreaseLiquidityParams({tokenId:tokenId,liquidity:liquidity,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L112-L120) lack of slippage protection.


### recommendation

For each vulnerable function, allow the caller to specify values 
for `amount0Min` and `amount1Min` instead of setting them to 0.


### locations
- solidity/test_lack_slippage_protection.sol#L85-L99
- solidity/test_lack_slippage_protection.sol#L101-L110
- solidity/test_lack_slippage_protection.sol#L112-L120

### severity
Medium

### category
lack-slippage-protection

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

## [Informational] Variable names too similar

### description
Detect variables with names that are too similar.

**There are `4` instances of this issue:**

- Variable [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).amount0Desired](solidity/test_lack_slippage_protection.sol#L80) is too similar to [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).amount1Desired](solidity/test_lack_slippage_protection.sol#L129)

- Variable [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).amount0Desired](solidity/test_lack_slippage_protection.sol#L80) is too similar to [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).amount1Desired](solidity/test_lack_slippage_protection.sol#L81)

- Variable [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).amount0Desired](solidity/test_lack_slippage_protection.sol#L128) is too similar to [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).amount1Desired](solidity/test_lack_slippage_protection.sol#L129)

- Variable [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).amount0Desired](solidity/test_lack_slippage_protection.sol#L128) is too similar to [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).amount1Desired](solidity/test_lack_slippage_protection.sol#L81)

#### Exploit scenario
Bob uses several variables with similar names. As a result, his code is difficult to review.

### recommendation
Prevent variables from having similar names.

### locations
- solidity/test_lack_slippage_protection.sol#L80
- solidity/test_lack_slippage_protection.sol#L80
- solidity/test_lack_slippage_protection.sol#L128
- solidity/test_lack_slippage_protection.sol#L128

### severity
Informational

### category
similar-names

### confidence
Medium

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `8` instances of this issue:**

- `uint128 `[INonfungiblePositionManager.mint(INonfungiblePositionManager.MintParams).liquidity](solidity/test_lack_slippage_protection.sol#L35) should be used `uint256/int256`.

- `uint128 `[INonfungiblePositionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams).liquidity](solidity/test_lack_slippage_protection.sol#L53) should be used `uint256/int256`.

- `int24 `[LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).tickLower](solidity/test_lack_slippage_protection.sol#L78) should be used `uint256/int256`.

- `int24 `[LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).tickUpper](solidity/test_lack_slippage_protection.sol#L79) should be used `uint256/int256`.

- `uint128 `[LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128).liquidity](solidity/test_lack_slippage_protection.sol#L83) should be used `uint256/int256`.

- `int24 `[LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).tickLower](solidity/test_lack_slippage_protection.sol#L126) should be used `uint256/int256`.

- `int24 `[LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).tickUpper](solidity/test_lack_slippage_protection.sol#L127) should be used `uint256/int256`.

- `uint128 `[LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256).liquidity](solidity/test_lack_slippage_protection.sol#L131) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/test_lack_slippage_protection.sol#L35
- solidity/test_lack_slippage_protection.sol#L53
- solidity/test_lack_slippage_protection.sol#L78
- solidity/test_lack_slippage_protection.sol#L79
- solidity/test_lack_slippage_protection.sol#L83
- solidity/test_lack_slippage_protection.sol#L126
- solidity/test_lack_slippage_protection.sol#L127
- solidity/test_lack_slippage_protection.sol#L131

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


**There are `2` instances of this issue:**

- [LackSlippageProtection.positionManager](solidity/test_lack_slippage_protection.sol#L73) should be cached with local memory-based variable in [LackSlippageProtection.bad(address,address,int24,int24,uint256,uint256,uint256,uint128)](solidity/test_lack_slippage_protection.sol#L75-L121), It is called more than once:
	- [positionManager.decreaseLiquidity(INonfungiblePositionManager.DecreaseLiquidityParams({tokenId:tokenId,liquidity:liquidity,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L112-L120)
	- [positionManager.mint(INonfungiblePositionManager.MintParams({token0:token0,token1:token1,fee:0,tickLower:tickLower,tickUpper:tickUpper,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,recipient:address(this),deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L85-L99)
	- [positionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams({tokenId:tokenId,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:0,amount1Min:0,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L101-L110)

- [LackSlippageProtection.positionManager](solidity/test_lack_slippage_protection.sol#L73) should be cached with local memory-based variable in [LackSlippageProtection.notBad(address,address,int24,int24,uint256,uint256,uint256,uint128,uint256)](solidity/test_lack_slippage_protection.sol#L123-L170), It is called more than once:
	- [positionManager.decreaseLiquidity(INonfungiblePositionManager.DecreaseLiquidityParams({tokenId:tokenId,liquidity:liquidity,amount0Min:amountMin,amount1Min:amountMin,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L161-L169)
	- [positionManager.increaseLiquidity(INonfungiblePositionManager.IncreaseLiquidityParams({tokenId:tokenId,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:amountMin,amount1Min:amountMin,deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L150-L159)
	- [positionManager.mint(INonfungiblePositionManager.MintParams({token0:token0,token1:token1,fee:0,tickLower:tickLower,tickUpper:tickUpper,amount0Desired:amount0Desired,amount1Desired:amount1Desired,amount0Min:100,amount1Min:100,recipient:address(this),deadline:block.timestamp}))](solidity/test_lack_slippage_protection.sol#L134-L148)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/test_lack_slippage_protection.sol#L73
- solidity/test_lack_slippage_protection.sol#L73

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [INonfungiblePositionManager.IncreaseLiquidity(uint256,uint128,uint256,uint256)](solidity/test_lack_slippage_protection.sol#L2-L7):

	- [amount0](solidity/test_lack_slippage_protection.sol#L5)

	- [liquidity](solidity/test_lack_slippage_protection.sol#L4)

	- [amount1](solidity/test_lack_slippage_protection.sol#L6)

- The following variables should be indexed in [INonfungiblePositionManager.DecreaseLiquidity(uint256,uint128,uint256,uint256)](solidity/test_lack_slippage_protection.sol#L9-L14):

	- [amount1](solidity/test_lack_slippage_protection.sol#L13)

	- [amount0](solidity/test_lack_slippage_protection.sol#L12)

	- [liquidity](solidity/test_lack_slippage_protection.sol#L11)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/test_lack_slippage_protection.sol#L2-L7
- solidity/test_lack_slippage_protection.sol#L9-L14

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [LackSlippageProtection.positionManager](solidity/test_lack_slippage_protection.sol#L73) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/test_lack_slippage_protection.sol#L73

### severity
Optimization

### category
constable-states

### confidence
High
