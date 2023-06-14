## Summary 

### High Risk Issues

| |Issue|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 2 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | Reduce gas usage by moving to Solidity 0.8.19 or later | 1 |



## [High] Arbitrary `from` in transferFrom

### description:
Detect when `msg.sender` is not used as `from` in transferFrom.

**There are `2` instances of this issue:**

- [C.bad3(address,address,uint256)](solidity/send_erc20_2.sol#L31-L33) uses arbitrary from in transferFrom: [erc20.safeTransferFrom(from,to,amount)](solidity/send_erc20_2.sol#L32)

- [C.bad4(address,address,uint256)](solidity/send_erc20_2.sol#L35-L37) uses arbitrary from in transferFrom: [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/send_erc20_2.sol#L36)

#### Exploit scenario

```solidity
    function a(address from, address to, uint256 amount) public {
        erc20.transferFrom(from, to, am);
    }
```
Alice approves this contract to spend her ERC20 tokens. Bob can call `a` and specify Alice's address as the `from` parameter in `transferFrom`, allowing him to transfer Alice's tokens to himself.

### recommendation:

Use `msg.sender` as `from` in transferFrom.


### location:
- solidity/send_erc20_2.sol#L31-L33
- solidity/send_erc20_2.sol#L35-L37

### severity:
High

### category:
arbitrary-send-erc20

## [Optimization] Reduce gas usage by moving to Solidity 0.8.19 or later

### description:
See this [link](https://blog.soliditylang.org/2023/02/22/solidity-0.8.19-release-announcement/#preventing-dead-code-in-runtime-bytecode) for the full details

**There is `1` instance of this issue:**

- pragma solidity version [0.8.18](solidity/send_erc20_2.sol#L1) should upgrade to the latest version: 0.8.19

### recommendation:
Upgrade solidity version to the latest version: 0.8.19

### location:
- solidity/send_erc20_2.sol#L1

### severity:
Optimization

### category:
upgrade-to-latest
