## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Use of `tx.origin` is unsafe in almost every context | 1 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |



## [Low] Use of `tx.origin` is unsafe in almost every context

### description:

According to [Vitalik Buterin](https://ethereum.stackexchange.com/questions/196/how-do-i-make-my-dapp-serenity-proof), 
contracts should _not_ `assume that tx.origin will continue to be usable or meaningful`. 
An example of this is [EIP-3074](https://eips.ethereum.org/EIPS/eip-3074#allowing-txorigin-as-signer-1) 
which explicitly mentions the intention to change its semantics when it's used with new op 
codes. There have also been calls to 
[remove](https://github.com/ethereum/solidity/issues/683) `tx.origin`, 
and there are [security issues](https://docs.soliditylang.org/en/latest/security-considerations.html#tx-origin) 
associated with using it for authorization. 

For these reasons, it's best to completely avoid the feature.


**There is `1` instance of this issue:**

- [tx.origin](solidity/test_unsafe_tx_origin.sol#L3) should use `msg.sender` instead of `tx.origin` as much as possible.


### recommendation:

Please use `msg.sender` instead of `tx.origin` as much as possible.


### locations:
- solidity/test_unsafe_tx_origin.sol#L3

### severity:
Low

### category:
unsafe-tx-origin

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
