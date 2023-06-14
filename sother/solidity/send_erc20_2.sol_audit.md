## Summary 

### High Risk Issues

| |Issue|Instances|
|---|:---|:---:|
| [H-0] | Arbitrary `from` in transferFrom | 2 |


### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |



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

## [Informational] Incorrect versions of Solidity

### description:

`solc` frequently releases new compiler versions. Using an old version prevents access to new Solidity security checks.
We also recommend avoiding complex `pragma` statement.

**There are `2` instances of this issue:**

- Pragma version[0.8.19](solidity/send_erc20_2.sol#L1) necessitates a version too recent to be trusted. Consider deploying with 0.8.18.

- solc-0.8.19 is not recommended for deployment


### recommendation:

Deploy with any of the following Solidity versions:
- 0.8.18

The recommendations take into account:
- Risks related to recent releases
- Risks of complex code generation changes
- Risks of new language features
- Risks of known bugs

Use a simple pragma version that allows any of these versions.
Consider using the latest version of Solidity for testing.

### location:
- solidity/send_erc20_2.sol#L1
- 

### severity:
Informational

### category:
solc-version
