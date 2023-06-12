
## Arbitrary `from` in transferFrom

### description:
Detect when `msg.sender` is not used as `from` in transferFrom.

There are `2` instances of this issue:
[C.bad3(address,address,uint256)](solidity/send_erc20_2.sol#L31-L33) uses arbitrary from in transferFrom: [erc20.safeTransferFrom(from,to,amount)](solidity/send_erc20_2.sol#L32)

[C.bad4(address,address,uint256)](solidity/send_erc20_2.sol#L35-L37) uses arbitrary from in transferFrom: [SafeERC20.safeTransferFrom(erc20,from,to,amount)](solidity/send_erc20_2.sol#L36)

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

## This is WIKI_TITLE

### description:
This is WIKI_DESCRIPTION

There is `1` instance of this issue:
This is an example!

#### Exploit scenario
This is WIKI_EXPLOIT_SCENARIO

### recommendation:
This is WIKI_RECOMMENDATION

### location:
- 

### severity:
Medium

### category:
mydetector
