## Summary 

### High Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [H-0] | State variable not initialized | 1 |


### Medium Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [M-0] | Usage of deprecated ChainLink APIs | 8 |
| [M-1] | `latestRoundData` returns has been ignored | 1 |
| [M-2] | `latestRoundData` might return stale results | 2 |
| [M-3] | Unchecked return data `roundId` from Chainlink aggregators | 2 |


### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Unsafe downcasting arithmetic operation | 2 |
| [L-1] | Setters should check the input value | 1 |
| [L-2] | Block timestamp | 3 |
| [L-3] | Missing Event Setter | 2 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |
| [N-1] | Conformance to Solidity naming conventions | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 2 |
| [G-1] | `internal` functions only called once can be inlined to save gas | 1 |
| [G-2] | Using custom errors replace `require` or `assert` | 1 |
| [G-3] | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead | 28 |
| [G-4] | Using `private` rather than `public` for constants, saves gas | 1 |
| [G-5] | Cache state variables instead of rereading | 1 |
| [G-6] | Not using the named return variables anywhere in the function is confusing | 3 |
| [G-7] | Remove unused local variables | 2 |
| [G-8] | Use indexed events for value types as they are less costly compared to non-indexed ones | 2 |
| [G-9] | Setting the constructor to `payable` | 1 |
| [G-10] | `!= 0` is less gas than `> 0` for unsigned integers | 1 |
| [G-11] | `Bytes` constants are more efficient than `string` constants | 1 |
| [G-12] | State variables that could be declared constant | 1 |



## [High] State variable not initialized

### description
A state variable not initialized and not written in contract but be used in contract

**There is `1` instance of this issue:**

- state variable: [UncheckedReturns.aggregator](solidity/tmp/test_chaink_link.sol#L241) not initialized and not written in contract but be used in contract

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
- solidity/tmp/test_chaink_link.sol#L241

### severity
High

### category
state-variable-not-initialized

### confidence
High

## [Medium] Usage of deprecated ChainLink APIs

### description

According to [Chainlink's documentation](https://docs.chain.link/data-feeds/api-reference),
the following functions are deprecated: `latestRound()`/`latestAnswer()`/`latestTimestamp()`/
`getAnswer(uint256 _roundId)`/`getTimestamp(uint256 _roundId)`. 

> This does not error if no
> answer has been reached, it will simply return 0. Either wait to point to
> an already answered Aggregator or use the recommended `getRoundData`
> instead which includes better verification information.

Impact: Deprecated API stops working. 
Prices cannot be obtained. Protocol stops and contracts have to be redeployed.


**There are `8` instances of this issue:**

-  should use `latestRoundData()` instead of [aggregator.latestRound()](solidity/tmp/test_chaink_link.sol#L84)

-  should use `latestRoundData()` instead of [aggregator.latestAnswer()](solidity/tmp/test_chaink_link.sol#L96)

-  should use `latestRoundData()` instead of [aggregator.latestTimestamp()](solidity/tmp/test_chaink_link.sol#L114)

-  should use `latestRoundData()` instead of [_getRoundData(uint80(aggregator.latestRound()))](solidity/tmp/test_chaink_link.sol#L144)

-  should use `latestRoundData()` instead of [aggregator.getAnswer(_roundId)](solidity/tmp/test_chaink_link.sol#L163)

-  should use `latestRoundData()` instead of [aggregator.getTimestamp(_roundId)](solidity/tmp/test_chaink_link.sol#L182)

-  should use `latestRoundData()` instead of [answer = aggregator.getAnswer(_roundId)](solidity/tmp/test_chaink_link.sol#L231)

-  should use `latestRoundData()` instead of [updatedAt = uint64(aggregator.getTimestamp(_roundId))](solidity/tmp/test_chaink_link.sol#L232)


### recommendation

It is recommended to use `latestRoundData()` method instead of deprecated APIs.


### locations
- solidity/tmp/test_chaink_link.sol#L84
- solidity/tmp/test_chaink_link.sol#L96
- solidity/tmp/test_chaink_link.sol#L114
- solidity/tmp/test_chaink_link.sol#L144
- solidity/tmp/test_chaink_link.sol#L163
- solidity/tmp/test_chaink_link.sol#L182
- solidity/tmp/test_chaink_link.sol#L231
- solidity/tmp/test_chaink_link.sol#L232

### severity
Medium

### category
deprecated-chainlink

### confidence
High

## [Medium] `latestRoundData` returns has been ignored

### description

The `latestRoundData` function in the contract `xxx.sol` fetches the asset price 
from a Chainlink aggregator using the latestRoundData function. 
However, the returns is ignored.

If there is a problem with chainlink starting a new round and finding consensus 
on the new value for the oracle (e.g. chainlink nodes abandon the oracle, 
chain congestion, vulnerability/attacks on the chainlink system) 
consumers of this contract may continue using outdated stale data 
(if oracles are unable to submit no new round is started)



**There is `1` instance of this issue:**

- [(roundId,price,None,None,answeredInRound) = aggregator.latestRoundData()](solidity/tmp/test_chaink_link.sol#L246-L247) returns has been ignored.


### recommendation

Consider checking the all oracle responses value after calling out 
to `chainlinkOracle.latestRoundData()` verifying that the result is within 
an allowed margin.

For example:
```
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = aggregator.latestRoundData();
    
    if (answeredInRound < roundId){
        revert("answer is being carried over");
    }
    if (startedAt == 0) {
        revert("Round not complete");
    }
    if (price == 0) {
        revert("answer reporting 0");
    }
    if (updatedAt < block.timestamp - maxDelayTime) {
        revert("time err");
    }
```


### locations
- solidity/tmp/test_chaink_link.sol#L246-L247

### severity
Medium

### category
ignored-chainlink-returns

### confidence
High

## [Medium] `latestRoundData` might return stale results

### description

The `latestRoundData` function in the contract `xxx.sol` fetches the asset price 
from a Chainlink aggregator using the latestRoundData function. 
However, the returns `updatedAt` timestamp is not checked.

If there is a problem with chainlink starting a new round and finding consensus 
on the new value for the oracle (e.g. chainlink nodes abandon the oracle, 
chain congestion, vulnerability/attacks on the chainlink system) 
consumers of this contract may continue using outdated stale data 
(if oracles are unable to submit no new round is started)



**There are `2` instances of this issue:**

- [(roundId,price,startedAt,updatedAt,answeredInRound) = aggregator.latestRoundData()](solidity/tmp/test_chaink_link.sol#L254-L260) unchecked `updatedAt` of `latestRoundData()`.

- [(roundId,price,startedAt,updatedAt,answeredInRound) = aggregator.latestRoundData()](solidity/tmp/test_chaink_link.sol#L267-L273) unchecked `updatedAt` of `latestRoundData()`.


### recommendation

Consider checking the oracle responses `updatedAt` value after calling out 
to `chainlinkOracle.latestRoundData()` verifying that the result is within 
an allowed margin of freshness.

For example:
```
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = aggregator.latestRoundData();

    if (answeredInRound < roundId){
        revert("answer is being carried over");
    }
    if (startedAt == 0) {
        revert("Round not complete");
    }
    if (price == 0) {
        revert("answer reporting 0");
    }
    if (updatedAt < block.timestamp - maxDelayTime) {
        revert("time err");
    }
```


### locations
- solidity/tmp/test_chaink_link.sol#L254-L260
- solidity/tmp/test_chaink_link.sol#L267-L273

### severity
Medium

### category
unchecked-chainlink-staleness

### confidence
High

## [Medium] Unchecked return data `roundId` from Chainlink aggregators

### description

The `latestRoundData` function in the contract `xxx.sol` fetches the asset price 
from a Chainlink aggregator using the latestRoundData function. 
However, there are no checks on `roundId`.

Stale prices could put funds at risk. 
According to Chainlink's documentation, This function does not error 
if no answer has been reached but returns 0, 
causing an incorrect price fed to the PriceOracle. 
The external Chainlink oracle, which provides index price information to the system, 
introduces risk inherent to any dependency on third-party data sources. 
For example, the oracle could fall behind or otherwise fail to be maintained, 
resulting in outdated data being fed to the index price calculations of the liquidity.



**There are `2` instances of this issue:**

- [(roundId,price,startedAt,updatedAt,answeredInRound) = aggregator.latestRoundData()](solidity/tmp/test_chaink_link.sol#L254-L260) unchecked `roundId` of `latestRoundData()`.

- [(roundId,price,startedAt,updatedAt,answeredInRound) = aggregator.latestRoundData()](solidity/tmp/test_chaink_link.sol#L267-L273) unchecked `roundId` of `latestRoundData()`.


### recommendation

Consider checking the oracle responses `answeredInRound` and `roundId` values after calling out 
to `chainlinkOracle.latestRoundData()` verifying that the result is within 
an allowed margin of freshness.

For example:
```
    (
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) = aggregator.latestRoundData();

    if (answeredInRound < roundId){
        revert("answer is being carried over");
    }
    if (startedAt == 0) {
        revert("Round not complete");
    }
    if (price == 0) {
        revert("answer reporting 0");
    }
    if (updatedAt < block.timestamp - maxDelayTime) {
        revert("time err");
    }
```


### locations
- solidity/tmp/test_chaink_link.sol#L254-L260
- solidity/tmp/test_chaink_link.sol#L267-L273

### severity
Medium

### category
unchecked-chainlink-round

### confidence
High

## [Low] Unsafe downcasting arithmetic operation

### description

Downcasting from uint256/int256 in Solidity does not revert on overflow.
When a type is downcast to a smaller type, the higher order bits are truncated, 
effectively applying a modulo to the original value. 
Without any other checks, this wrapping will lead to unexpected behavior and bugs.


**There are `2` instances of this issue:**

- [_getRoundData(uint80(aggregator.latestRound()))](solidity/tmp/test_chaink_link.sol#L144) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.
- [updatedAt = uint64(aggregator.getTimestamp(_roundId))](solidity/tmp/test_chaink_link.sol#L232) should use `uint256/int256` or `OpenZeppelin SafeCast lib`.

### recommendation

Just use `uint256/int256`, or use [OpenZeppelin SafeCast lib](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeCast.sol#).


### locations
- solidity/tmp/test_chaink_link.sol#L144
- solidity/tmp/test_chaink_link.sol#L232

### severity
Low

### category
unsafe-downcast

### confidence
High

## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There is `1` instance of this issue:**

- [AggregatorFacade.constructor(address,uint8,string)._decimals](solidity/tmp/test_chaink_link.sol#L68) lacks an upper limit check on :
	- [decimals = _decimals](solidity/tmp/test_chaink_link.sol#L72)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/test_chaink_link.sol#L68

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Block timestamp

### description
Dangerous usage of `block.timestamp`. `block.timestamp` can be manipulated by miners.

**There are `3` instances of this issue:**

- [UncheckedReturns.bad3()](solidity/tmp/test_chaink_link.sol#L266-L280) uses timestamp for comparisons
	Dangerous comparisons:
	- [valid = price > 0 && answeredInRound == roundId && ((block.timestamp - updatedAt) <= 10)](solidity/tmp/test_chaink_link.sol#L275-L277)

- [UncheckedReturns.good1()](solidity/tmp/test_chaink_link.sol#L282-L309) uses timestamp for comparisons
	Dangerous comparisons:
	- [updatedAt < block.timestamp - maxDelayTime](solidity/tmp/test_chaink_link.sol#L304)

- [UncheckedReturns.checkChainlink(uint80,int256,uint256,uint256,uint80)](solidity/tmp/test_chaink_link.sol#L323-L346) uses timestamp for comparisons
	Dangerous comparisons:
	- [updatedAt < block.timestamp - maxDelayTime](solidity/tmp/test_chaink_link.sol#L343)

#### Exploit scenario
"Bob's contract relies on `block.timestamp` for its randomness. Eve is a miner and manipulates `block.timestamp` to exploit Bob's contract.

### recommendation
Avoid relying on `block.timestamp`.

### locations
- solidity/tmp/test_chaink_link.sol#L266-L280
- solidity/tmp/test_chaink_link.sol#L282-L309
- solidity/tmp/test_chaink_link.sol#L323-L346

### severity
Low

### category
timestamp

### confidence
Medium

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `2` instances of this issue:**

- Setter function [AggregatorFacade.slitherConstructorConstantVariables()](solidity/tmp/test_chaink_link.sol#L55-L238) does not emit an event

- Setter function [UncheckedReturns.slitherConstructorConstantVariables()](solidity/tmp/test_chaink_link.sol#L240-L347) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/test_chaink_link.sol#L55-L238
- solidity/tmp/test_chaink_link.sol#L240-L347

### severity
Low

### category
pess-event-setter

### confidence
Medium

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

**There are `4` instances of this issue:**

- Parameter [AggregatorFacade.getAnswer(uint256)._roundId](solidity/tmp/test_chaink_link.sol#L156) is not in mixedCase

- Parameter [AggregatorFacade.getTimestamp(uint256)._roundId](solidity/tmp/test_chaink_link.sol#L175) is not in mixedCase

- Parameter [AggregatorFacade.getRoundData(uint80)._roundId](solidity/tmp/test_chaink_link.sol#L200) is not in mixedCase

- Constant [UncheckedReturns.maxDelayTime](solidity/tmp/test_chaink_link.sol#L243) is not in UPPER_CASE_WITH_UNDERSCORES


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/test_chaink_link.sol#L156
- solidity/tmp/test_chaink_link.sol#L175
- solidity/tmp/test_chaink_link.sol#L200
- solidity/tmp/test_chaink_link.sol#L243

### severity
Informational

### category
naming-convention

### confidence
High

## [Optimization] State variables only set in the constructor should be declared immutable

### description

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There are `2` instances of this issue:**

- [AggregatorFacade.aggregator](solidity/tmp/test_chaink_link.sol#L56) should be immutable 

- [AggregatorFacade.decimals](solidity/tmp/test_chaink_link.sol#L57) should be immutable 


### recommendation
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations
- solidity/tmp/test_chaink_link.sol#L56
- solidity/tmp/test_chaink_link.sol#L57

### severity
Optimization

### category
immutable-states

### confidence
High

## [Optimization] `internal` functions only called once can be inlined to save gas

### description

Not inlining costs **20 to 40 gas** because of two extra `JUMP` instructions and additional stack operations needed for function calls.
more detail see [this](https://docs.soliditylang.org/en/v0.8.20/internals/optimizer.html#function-inlining) and [this](https://blog.soliditylang.org/2021/03/02/saving-gas-with-simple-inliner/)
        

**There is `1` instance of this issue:**

- [UncheckedReturns.checkChainlink(uint80,int256,uint256,uint256,uint80)](solidity/tmp/test_chaink_link.sol#L323-L346) could be inlined to save gas.


### recommendation
Using inlining replace `internal` function which only called once

### locations
- solidity/tmp/test_chaink_link.sol#L323-L346

### severity
Optimization

### category
internal-function-to-inline

### confidence
High

## [Optimization] Using custom errors replace `require` or `assert`

### description

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There is `1` instance of this issue:**

- [require(bool,string)(updatedAt > 0,V3_NO_DATA_ERROR)](solidity/tmp/test_chaink_link.sol#L234) should use custom error to save gas.


### recommendation

Using custom errors replace `require` or `assert`.


### locations
- solidity/tmp/test_chaink_link.sol#L234

### severity
Optimization

### category
use-custom-error

### confidence
High

## [Optimization] Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead

### description

> When using elements that are smaller than 32 bytes, your contract’s gas usage may be higher. This is because the EVM operates on 32 bytes at a time. Therefore, if the element is smaller than that, the EVM must use more operations in order to reduce the size of the element from 32 bytes to the desired size.

More detail see [this.](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)

Each operation involving a `uint8` costs an extra [**22-28 gas**](https://gist.github.com/0xxfu/3672fec07eb3031cd5da14ac015e04a1) (depending on whether the other operand is also a variable of type `uint8`) as compared to ones involving `uint256`, due to the compiler having to clear the higher bits of the memory word before operating on the `uint8`, as well as the associated stack operations of doing so. Use a larger size then downcast where needed


**There are `28` instances of this issue:**

- `uint8 `[AggregatorV3Interface.decimals().](solidity/tmp/test_chaink_link.sol#L26) should be used `uint256/int256`.

- `uint80 `[AggregatorV3Interface.getRoundData(uint80)._roundId](solidity/tmp/test_chaink_link.sol#L32) should be used `uint256/int256`.

- `uint80 `[AggregatorV3Interface.getRoundData(uint80).roundId](solidity/tmp/test_chaink_link.sol#L36) should be used `uint256/int256`.

- `uint80 `[AggregatorV3Interface.getRoundData(uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L40) should be used `uint256/int256`.

- `uint80 `[AggregatorV3Interface.latestRoundData().roundId](solidity/tmp/test_chaink_link.sol#L47) should be used `uint256/int256`.

- `uint80 `[AggregatorV3Interface.latestRoundData().answeredInRound](solidity/tmp/test_chaink_link.sol#L51) should be used `uint256/int256`.

- `uint8 `[AggregatorFacade.decimals](solidity/tmp/test_chaink_link.sol#L57) should be used `uint256/int256`.

- `uint8 `[AggregatorFacade.constructor(address,uint8,string)._decimals](solidity/tmp/test_chaink_link.sol#L68) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade.latestRoundData().roundId](solidity/tmp/test_chaink_link.sol#L137) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade.latestRoundData().answeredInRound](solidity/tmp/test_chaink_link.sol#L141) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade.getRoundData(uint80)._roundId](solidity/tmp/test_chaink_link.sol#L200) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade.getRoundData(uint80).roundId](solidity/tmp/test_chaink_link.sol#L206) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade.getRoundData(uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L210) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade._getRoundData(uint80)._roundId](solidity/tmp/test_chaink_link.sol#L220) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade._getRoundData(uint80).roundId](solidity/tmp/test_chaink_link.sol#L224) should be used `uint256/int256`.

- `uint80 `[AggregatorFacade._getRoundData(uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L228) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad().roundId](solidity/tmp/test_chaink_link.sol#L246) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad().answeredInRound](solidity/tmp/test_chaink_link.sol#L246) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad2().roundId](solidity/tmp/test_chaink_link.sol#L255) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad2().answeredInRound](solidity/tmp/test_chaink_link.sol#L259) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad3().roundId](solidity/tmp/test_chaink_link.sol#L268) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.bad3().answeredInRound](solidity/tmp/test_chaink_link.sol#L272) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.good1().roundId](solidity/tmp/test_chaink_link.sol#L284) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.good1().answeredInRound](solidity/tmp/test_chaink_link.sol#L288) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.good2().roundId](solidity/tmp/test_chaink_link.sol#L313) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.good2().answeredInRound](solidity/tmp/test_chaink_link.sol#L317) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.checkChainlink(uint80,int256,uint256,uint256,uint80).roundId](solidity/tmp/test_chaink_link.sol#L324) should be used `uint256/int256`.

- `uint80 `[UncheckedReturns.checkChainlink(uint80,int256,uint256,uint256,uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L328) should be used `uint256/int256`.


### recommendation

Using `uint256/int256` replace `uint128/uint64/uint32/uint16/uint8` or `int128/int64/int32/int16/int8`


### locations
- solidity/tmp/test_chaink_link.sol#L26
- solidity/tmp/test_chaink_link.sol#L32
- solidity/tmp/test_chaink_link.sol#L36
- solidity/tmp/test_chaink_link.sol#L40
- solidity/tmp/test_chaink_link.sol#L47
- solidity/tmp/test_chaink_link.sol#L51
- solidity/tmp/test_chaink_link.sol#L57
- solidity/tmp/test_chaink_link.sol#L68
- solidity/tmp/test_chaink_link.sol#L137
- solidity/tmp/test_chaink_link.sol#L141
- solidity/tmp/test_chaink_link.sol#L200
- solidity/tmp/test_chaink_link.sol#L206
- solidity/tmp/test_chaink_link.sol#L210
- solidity/tmp/test_chaink_link.sol#L220
- solidity/tmp/test_chaink_link.sol#L224
- solidity/tmp/test_chaink_link.sol#L228
- solidity/tmp/test_chaink_link.sol#L246
- solidity/tmp/test_chaink_link.sol#L246
- solidity/tmp/test_chaink_link.sol#L255
- solidity/tmp/test_chaink_link.sol#L259
- solidity/tmp/test_chaink_link.sol#L268
- solidity/tmp/test_chaink_link.sol#L272
- solidity/tmp/test_chaink_link.sol#L284
- solidity/tmp/test_chaink_link.sol#L288
- solidity/tmp/test_chaink_link.sol#L313
- solidity/tmp/test_chaink_link.sol#L317
- solidity/tmp/test_chaink_link.sol#L324
- solidity/tmp/test_chaink_link.sol#L328

### severity
Optimization

### category
smaller-uint-int

### confidence
High

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There is `1` instance of this issue:**

- [AggregatorFacade.version](solidity/tmp/test_chaink_link.sol#L60) should be used `private` visibility to save gas.


### recommendation

Using `private` replace `public` with constant.


### locations
- solidity/tmp/test_chaink_link.sol#L60

### severity
Optimization

### category
public-to-private-constant

### confidence
High

## [Optimization] Cache state variables instead of rereading

### description

The instances below point to the second+ access of a state variable within a function. Caching of a state variable replaces each Gwarmaccess (**100 gas**) with a much cheaper stack read. Other less obvious fixes/optimizations include having local memory caches of state variable structs, or having local caches of state variable contracts/addresses.

More detail see [this.](https://gist.github.com/0xxfu/af8f63ccbf36af9d067ed6eff9ff7129)


**There is `1` instance of this issue:**

- [AggregatorFacade.aggregator](solidity/tmp/test_chaink_link.sol#L56) should be cached with local memory-based variable in [AggregatorFacade._getRoundData(uint80)](solidity/tmp/test_chaink_link.sol#L220-L237), It is called more than once:
	- [updatedAt = uint64(aggregator.getTimestamp(_roundId))](solidity/tmp/test_chaink_link.sol#L232)
	- [answer = aggregator.getAnswer(_roundId)](solidity/tmp/test_chaink_link.sol#L231)


### recommendation

Cache storage-based state variables in local memory-based variables appropriately to convert SLOADs to MLOADs and reduce gas consumption from 100 units to 3 units. than once for a function


### locations
- solidity/tmp/test_chaink_link.sol#L56

### severity
Optimization

### category
reread-state-variables

### confidence
High

## [Optimization] Not using the named return variables anywhere in the function is confusing

### description

Consider changing the variable to be an unnamed one, 
since the variable is never assigned, nor is it returned by name. 
If the optimizer is not turned on, leaving the code as it is will also waste gas 
for the stack variable.


**There are `3` instances of this issue:**

- The named return variables in [AggregatorFacade.latestRoundData()](solidity/tmp/test_chaink_link.sol#L131-L145) are unused.
	- [AggregatorFacade.latestRoundData().answeredInRound](solidity/tmp/test_chaink_link.sol#L141)
	- [AggregatorFacade.latestRoundData().startedAt](solidity/tmp/test_chaink_link.sol#L139)
	- [AggregatorFacade.latestRoundData().roundId](solidity/tmp/test_chaink_link.sol#L137)
	- [AggregatorFacade.latestRoundData().updatedAt](solidity/tmp/test_chaink_link.sol#L140)
	- [AggregatorFacade.latestRoundData().answer](solidity/tmp/test_chaink_link.sol#L138)

- The named return variables in [AggregatorFacade.getRoundData(uint80)](solidity/tmp/test_chaink_link.sol#L200-L214) are unused.
	- [AggregatorFacade.getRoundData(uint80).updatedAt](solidity/tmp/test_chaink_link.sol#L209)
	- [AggregatorFacade.getRoundData(uint80).answer](solidity/tmp/test_chaink_link.sol#L207)
	- [AggregatorFacade.getRoundData(uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L210)
	- [AggregatorFacade.getRoundData(uint80).startedAt](solidity/tmp/test_chaink_link.sol#L208)
	- [AggregatorFacade.getRoundData(uint80).roundId](solidity/tmp/test_chaink_link.sol#L206)

- The named return variables in [AggregatorFacade._getRoundData(uint80)](solidity/tmp/test_chaink_link.sol#L220-L237) are unused.
	- [AggregatorFacade._getRoundData(uint80).startedAt](solidity/tmp/test_chaink_link.sol#L226)
	- [AggregatorFacade._getRoundData(uint80).answeredInRound](solidity/tmp/test_chaink_link.sol#L228)
	- [AggregatorFacade._getRoundData(uint80).roundId](solidity/tmp/test_chaink_link.sol#L224)


### recommendation

Remove the unused named return variables.


### locations
- solidity/tmp/test_chaink_link.sol#L131-L145
- solidity/tmp/test_chaink_link.sol#L200-L214
- solidity/tmp/test_chaink_link.sol#L220-L237

### severity
Optimization

### category
unused-named-return-variables

### confidence
High

## [Optimization] Remove unused local variables

### description

Unused local variables are gas consuming, 
since the initial value assignment costs gas. 
And are a bad code practice. 
Removing those variables can save deployment and called gas. and improve code quality. 


**There are `2` instances of this issue:**

- The local variables in [UncheckedReturns.bad2()](solidity/tmp/test_chaink_link.sol#L253-L264) are unused.
	- [UncheckedReturns.bad2().startedAt](solidity/tmp/test_chaink_link.sol#L257)
	- [UncheckedReturns.bad2().updatedAt](solidity/tmp/test_chaink_link.sol#L258)

- The local variables in [UncheckedReturns.bad3()](solidity/tmp/test_chaink_link.sol#L266-L280) are unused.
	- [UncheckedReturns.bad3().startedAt](solidity/tmp/test_chaink_link.sol#L270)


### recommendation

Remove the unused local variables.


### locations
- solidity/tmp/test_chaink_link.sol#L253-L264
- solidity/tmp/test_chaink_link.sol#L266-L280

### severity
Optimization

### category
unused-local-var

### confidence
High

## [Optimization] Use indexed events for value types as they are less costly compared to non-indexed ones

### description

Using the `indexed` keyword for [value types](https://docs.soliditylang.org/en/v0.8.20/types.html#value-types) (`bool/int/address/string/bytes`) saves gas costs, as seen in [this example](https://gist.github.com/0xxfu/c292a65ecb61cae6fd2090366ea0877e).

However, this is only the case for value types, whereas indexing [reference types](https://docs.soliditylang.org/en/v0.8.20/types.html#reference-types) (`array/struct`) are more expensive than their unindexed version.


**There are `2` instances of this issue:**

- The following variables should be indexed in [AggregatorInterface.AnswerUpdated(int256,uint256,uint256)](solidity/tmp/test_chaink_link.sol#L12-L16):

	- [updatedAt](solidity/tmp/test_chaink_link.sol#L15)

- The following variables should be indexed in [AggregatorInterface.NewRound(uint256,address,uint256)](solidity/tmp/test_chaink_link.sol#L18-L22):

	- [startedAt](solidity/tmp/test_chaink_link.sol#L21)


### recommendation

Using the `indexed` keyword for values types `bool/int/address/string/bytes` in event


### locations
- solidity/tmp/test_chaink_link.sol#L12-L16
- solidity/tmp/test_chaink_link.sol#L18-L22

### severity
Optimization

### category
unindexed-event

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There is `1` instance of this issue:**

- [AggregatorFacade.constructor(address,uint8,string)](solidity/tmp/test_chaink_link.sol#L66-L74) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/test_chaink_link.sol#L66-L74

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] `!= 0` is less gas than `> 0` for unsigned integers

### description

`!= 0` costs less gas compared to `> 0` for unsigned integers in require statements 
with the optimizer enabled (6 gas)

While it may seem that `> 0` is cheaper than `!=`, this is only true without the 
optimizer enabled and outside a require statement. 
If you enable the optimizer at 10k and you’re in a `require` statement, 
this will save gas.



**There is `1` instance of this issue:**

- [require(bool,string)(updatedAt > 0,V3_NO_DATA_ERROR)](solidity/tmp/test_chaink_link.sol#L234) should use `!= 0` instead of `> 0` for unsigned integer comparison.


### recommendation

Use `!= 0` instead of `> 0` for unsigned integer comparison.


### locations
- solidity/tmp/test_chaink_link.sol#L234

### severity
Optimization

### category
unsigned-int-compare-zero

### confidence
High

## [Optimization] `Bytes` constants are more efficient than `string` constants

### description

From the [Solidity doc](https://docs.soliditylang.org/en/develop/types.html#arrays):
> If you can limit the length to a certain number of bytes, 
> always use one of the value types `bytes1` to `bytes32` because they are much cheaper.

[Why do Solidity examples use bytes32 type instead of string?](https://ethereum.stackexchange.com/questions/3795/why-do-solidity-examples-use-bytes32-type-instead-of-string)

`bytes32` uses less gas because it fits in a single word of the EVM, 
and `string` is a dynamically sized-type which has current limitations in Solidity 
(such as can’t be returned from a function to a contract).

If data can fit into 32 bytes, then you should use `bytes32` datatype rather than `bytes` or `strings`
 as it is cheaper in solidity. 
 Basically, any fixed size variable in solidity is cheaper than variable size. 
 That will save gas on the contract.


**There is `1` instance of this issue:**

- [AggregatorFacade.V3_NO_DATA_ERROR](solidity/tmp/test_chaink_link.sol#L64) should use `bytes(1..31)` instead of `string`.


### recommendation

Replace `string` constant with `bytes(1..32)` constant.


### locations
- solidity/tmp/test_chaink_link.sol#L64

### severity
Optimization

### category
string-constants

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There is `1` instance of this issue:**

- [UncheckedReturns.aggregator](solidity/tmp/test_chaink_link.sol#L241) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/test_chaink_link.sol#L241

### severity
Optimization

### category
constable-states

### confidence
High
