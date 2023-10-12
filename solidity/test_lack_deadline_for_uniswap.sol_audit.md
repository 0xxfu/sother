## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 2 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Unused return | 8 |
| [M-1] | Lack of deadline for Uniswap AMM | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Cache state variables instead of rereading | 2 |
| [G-1] | State variables that could be declared constant | 2 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There are `2` instances of this issue:**

- state variable: [LackDeadlineForUniswap.swapRouter](solidity/test_lack_deadline_for_uniswap.sol#L122) not initialized and not written in contract but be used in contract

- state variable: [LackDeadlineForUniswap.swapRouterBad](solidity/test_lack_deadline_for_uniswap.sol#L123) not initialized and not written in contract but be used in contract

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
- solidity/test_lack_deadline_for_uniswap.sol#L122
- solidity/test_lack_deadline_for_uniswap.sol#L123

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Unused return

### description
The return value of an external call is not stored in a local or state variable.

**There are `8` instances of this issue:**

- [LackDeadlineForUniswap.bad()](solidity/test_lack_deadline_for_uniswap.sol#L125-L169) ignores return value by [swapRouterBad.exactOutput(params4)](solidity/test_lack_deadline_for_uniswap.sol#L168)

- [LackDeadlineForUniswap.bad()](solidity/test_lack_deadline_for_uniswap.sol#L125-L169) ignores return value by [swapRouterBad.exactOutputSingle(params3)](solidity/test_lack_deadline_for_uniswap.sol#L158)

- [LackDeadlineForUniswap.bad()](solidity/test_lack_deadline_for_uniswap.sol#L125-L169) ignores return value by [swapRouterBad.exactInputSingle(params1)](solidity/test_lack_deadline_for_uniswap.sol#L136)

- [LackDeadlineForUniswap.bad()](solidity/test_lack_deadline_for_uniswap.sol#L125-L169) ignores return value by [swapRouterBad.exactInput(params2)](solidity/test_lack_deadline_for_uniswap.sol#L145)

- [LackDeadlineForUniswap.good()](solidity/test_lack_deadline_for_uniswap.sol#L171-L217) ignores return value by [swapRouter.exactOutputSingle(params3)](solidity/test_lack_deadline_for_uniswap.sol#L206)

- [LackDeadlineForUniswap.good()](solidity/test_lack_deadline_for_uniswap.sol#L171-L217) ignores return value by [swapRouter.exactOutput(params4)](solidity/test_lack_deadline_for_uniswap.sol#L216)

- [LackDeadlineForUniswap.good()](solidity/test_lack_deadline_for_uniswap.sol#L171-L217) ignores return value by [swapRouter.exactInput(params2)](solidity/test_lack_deadline_for_uniswap.sol#L193)

- [LackDeadlineForUniswap.good()](solidity/test_lack_deadline_for_uniswap.sol#L171-L217) ignores return value by [swapRouter.exactInputSingle(params1)](solidity/test_lack_deadline_for_uniswap.sol#L183)

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
- solidity/test_lack_deadline_for_uniswap.sol#L125-L169
- solidity/test_lack_deadline_for_uniswap.sol#L125-L169
- solidity/test_lack_deadline_for_uniswap.sol#L125-L169
- solidity/test_lack_deadline_for_uniswap.sol#L125-L169
- solidity/test_lack_deadline_for_uniswap.sol#L171-L217
- solidity/test_lack_deadline_for_uniswap.sol#L171-L217
- solidity/test_lack_deadline_for_uniswap.sol#L171-L217
- solidity/test_lack_deadline_for_uniswap.sol#L171-L217

### severity
Medium

### category
unused-return

### confidence
Medium

## [Medium] Lack of deadline for Uniswap AMM

### description

There is no deadline parameter in the Uniswap param struct. It can caused a lot of serious problems:

1. Alice wants to swap eth for safEth
2. The transaction is submitted to the mempool, however, Alice chose a transaction fee that is too low for miners to be interested in including her transaction in a block. The transaction stays pending in the mempool for extended periods, which could be hours, days, weeks, or even longer.
3. When the average gas fee dropped far enough for Alice's transaction to become interesting again for miners to include it, her swap will be executed. In the meantime, the price of ETH could have drastically changed. She will still get 1 ETH but the safEth value of that output might be significantly lower. She has unknowingly performed a bad trade due to the pending transaction she forgot about.

An even worse way this issue can be maliciously exploited is through MEV:

1. The swap transaction is still pending in the mempool. Average fees are still too high for miners to be interested in it. The price of tokens has gone up significantly since the transaction was signed, meaning Alice would receive a lot more ETH when the swap is executed. But that also means that her maximum slippage value (sqrtPriceLimitX96 and minOut ) is outdated and would allow for significant slippage.
2. A MEV bot detects the pending transaction. Since the outdated maximum slippage value now allows for high slippage, the bot sandwiches Alice, resulting in significant profit for the bot and significant loss for Alice.

Also for the same reason it is necessary to provide the user to pass in the slippage to prevent something like this too.


**There are `4` instances of this issue:**

- [swapRouterBad.exactInputSingle(params1)](solidity/test_lack_deadline_for_uniswap.sol#L136) lack of deadline for Uniswap AMM.

- [swapRouterBad.exactInput(params2)](solidity/test_lack_deadline_for_uniswap.sol#L145) lack of deadline for Uniswap AMM.

- [swapRouterBad.exactOutputSingle(params3)](solidity/test_lack_deadline_for_uniswap.sol#L158) lack of deadline for Uniswap AMM.

- [swapRouterBad.exactOutput(params4)](solidity/test_lack_deadline_for_uniswap.sol#L168) lack of deadline for Uniswap AMM.


### recommendation

Function should accept a user-input deadline param that should be passed along to Uniswap param struct.


### locations
- solidity/test_lack_deadline_for_uniswap.sol#L136
- solidity/test_lack_deadline_for_uniswap.sol#L145
- solidity/test_lack_deadline_for_uniswap.sol#L158
- solidity/test_lack_deadline_for_uniswap.sol#L168

### severity
Medium

### category
lack-deadline-in-uniswap

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

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There are `2` instances of this issue:**

- [LackDeadlineForUniswap.swapRouter](solidity/test_lack_deadline_for_uniswap.sol#L122) should be cached with local memory-based variable in [LackDeadlineForUniswap.good()](solidity/test_lack_deadline_for_uniswap.sol#L171-L217), It is called more than once:
	- [swapRouter.exactInputSingle(params1)](solidity/test_lack_deadline_for_uniswap.sol#L183)
	- [swapRouter.exactInput(params2)](solidity/test_lack_deadline_for_uniswap.sol#L193)
	- [swapRouter.exactOutputSingle(params3)](solidity/test_lack_deadline_for_uniswap.sol#L206)
	- [swapRouter.exactOutput(params4)](solidity/test_lack_deadline_for_uniswap.sol#L216)

- [LackDeadlineForUniswap.swapRouterBad](solidity/test_lack_deadline_for_uniswap.sol#L123) should be cached with local memory-based variable in [LackDeadlineForUniswap.bad()](solidity/test_lack_deadline_for_uniswap.sol#L125-L169), It is called more than once:
	- [swapRouterBad.exactOutput(params4)](solidity/test_lack_deadline_for_uniswap.sol#L168)
	- [swapRouterBad.exactInputSingle(params1)](solidity/test_lack_deadline_for_uniswap.sol#L136)
	- [swapRouterBad.exactInput(params2)](solidity/test_lack_deadline_for_uniswap.sol#L145)
	- [swapRouterBad.exactOutputSingle(params3)](solidity/test_lack_deadline_for_uniswap.sol#L158)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/test_lack_deadline_for_uniswap.sol#L122
- solidity/test_lack_deadline_for_uniswap.sol#L123

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `2` instances of this issue:**

- [LackDeadlineForUniswap.swapRouter](solidity/test_lack_deadline_for_uniswap.sol#L122) should be constant 

- [LackDeadlineForUniswap.swapRouterBad](solidity/test_lack_deadline_for_uniswap.sol#L123) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/test_lack_deadline_for_uniswap.sol#L122
- solidity/test_lack_deadline_for_uniswap.sol#L123

### severity
Optimization

### category
constable-states

### confidence
High
