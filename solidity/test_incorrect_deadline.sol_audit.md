## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Incorrect EIP-2612 deadline check | 6 |
| [L-1] | Block timestamp | 4 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | Using custom errors replace `require` or `assert` | 6 |



## [Low] Incorrect EIP-2612 deadline check

### description:

According to [EIP-2612](https://github.com/ethereum/EIPs/blob/71dc97318013bf2ac572ab63fab530ac9ef419ca/EIPS/eip-2612.md?plain=1#L58), 
signatures used on exactly the deadline timestamp are supposed to be allowed. 
While the signature may or may not be used for the exact EIP-2612 use case 
(transfer approvals), for consistency's sake, all deadlines should follow this semantic. 
If the timestamp is an expiration rather than a deadline, 
consider whether it makes more sense to include the expiration timestamp as 
a valid timestamp, as is done for deadlines.


**There are `6` instances of this issue:**

- [deadline <= block.timestamp](solidity/test_incorrect_deadline.sol#L3) use at deadlines should be allowed.

- [block.timestamp >= deadline](solidity/test_incorrect_deadline.sol#L6) use at deadlines should be allowed.

- [deadline <= blocktime](solidity/test_incorrect_deadline.sol#L11) use at deadlines should be allowed.

- [require(bool,string)(deadline > block.timestamp,err)](solidity/test_incorrect_deadline.sol#L17) use at deadlines should be allowed.

- [require(bool,string)(block.timestamp < deadline,err)](solidity/test_incorrect_deadline.sol#L18) use at deadlines should be allowed.

- [require(bool,string)(deadline > blocktime,err)](solidity/test_incorrect_deadline.sol#L21) use at deadlines should be allowed.


### recommendation:

The current `blocktime` should less than or equal to `deadline`.
```
    // `if` statement
    if (block.timestamp > deadline) {
            revert("deadline");
    }
    
    // Alternative, `require` statement
    require(block.timestamp <= deadline, "deadline");
```


### locations:
- solidity/test_incorrect_deadline.sol#L3
- solidity/test_incorrect_deadline.sol#L6
- solidity/test_incorrect_deadline.sol#L11
- solidity/test_incorrect_deadline.sol#L17
- solidity/test_incorrect_deadline.sol#L18
- solidity/test_incorrect_deadline.sol#L21

### severity:
Low

### category:
incorrect-deadline

## [Low] Block timestamp

### description:
Dangerous usage of `block.timestamp`. `block.timestamp` can be manipulated by miners.

**There are `4` instances of this issue:**

- [IncorrectDeadline.bad0(uint256)](solidity/test_incorrect_deadline.sol#L2-L14) uses timestamp for comparisons
	Dangerous comparisons:
	- [deadline <= block.timestamp](solidity/test_incorrect_deadline.sol#L3)
	- [block.timestamp >= deadline](solidity/test_incorrect_deadline.sol#L6)
	- [deadline <= blocktime](solidity/test_incorrect_deadline.sol#L11)

- [IncorrectDeadline.bad1(uint256)](solidity/test_incorrect_deadline.sol#L16-L22) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(deadline > block.timestamp,err)](solidity/test_incorrect_deadline.sol#L17)
	- [require(bool,string)(block.timestamp < deadline,err)](solidity/test_incorrect_deadline.sol#L18)
	- [require(bool,string)(deadline > blocktime,err)](solidity/test_incorrect_deadline.sol#L21)

- [IncorrectDeadline.notBbad(uint256)](solidity/test_incorrect_deadline.sol#L24-L36) uses timestamp for comparisons
	Dangerous comparisons:
	- [deadline < block.timestamp](solidity/test_incorrect_deadline.sol#L25)
	- [block.timestamp > deadline](solidity/test_incorrect_deadline.sol#L28)
	- [blocktime > deadline](solidity/test_incorrect_deadline.sol#L33)

- [IncorrectDeadline.notBad1(uint256)](solidity/test_incorrect_deadline.sol#L38-L44) uses timestamp for comparisons
	Dangerous comparisons:
	- [require(bool,string)(deadline >= block.timestamp,err)](solidity/test_incorrect_deadline.sol#L39)
	- [require(bool,string)(block.timestamp <= deadline,err)](solidity/test_incorrect_deadline.sol#L40)
	- [require(bool,string)(blocktime <= deadline,err)](solidity/test_incorrect_deadline.sol#L43)

#### Exploit scenario
"Bob's contract relies on `block.timestamp` for its randomness. Eve is a miner and manipulates `block.timestamp` to exploit Bob's contract.

### recommendation:
Avoid relying on `block.timestamp`.

### locations:
- solidity/test_incorrect_deadline.sol#L2-L14
- solidity/test_incorrect_deadline.sol#L16-L22
- solidity/test_incorrect_deadline.sol#L24-L36
- solidity/test_incorrect_deadline.sol#L38-L44

### severity:
Low

### category:
timestamp

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

## [Optimization] Using custom errors replace `require` or `assert`

### description:

Using a custom error instance will usually be much cheaper than a string description, because you can use the name of the error to describe it, which is encoded in only four bytes. A longer description can be supplied via NatSpec which does not incur any costs.

More detail see [this](https://gist.github.com/0xxfu/712f7965446526f8c5bc53a91d97a215) and [this](https://docs.soliditylang.org/en/latest/control-structures.html#revert).


**There are `6` instances of this issue:**

- [require(bool,string)(deadline > block.timestamp,err)](solidity/test_incorrect_deadline.sol#L17) should use custom error to save gas.

- [require(bool,string)(block.timestamp < deadline,err)](solidity/test_incorrect_deadline.sol#L18) should use custom error to save gas.

- [require(bool,string)(deadline > blocktime,err)](solidity/test_incorrect_deadline.sol#L21) should use custom error to save gas.

- [require(bool,string)(deadline >= block.timestamp,err)](solidity/test_incorrect_deadline.sol#L39) should use custom error to save gas.

- [require(bool,string)(block.timestamp <= deadline,err)](solidity/test_incorrect_deadline.sol#L40) should use custom error to save gas.

- [require(bool,string)(blocktime <= deadline,err)](solidity/test_incorrect_deadline.sol#L43) should use custom error to save gas.


### recommendation:

Using custom errors replace `require` or `assert`.


### locations:
- solidity/test_incorrect_deadline.sol#L17
- solidity/test_incorrect_deadline.sol#L18
- solidity/test_incorrect_deadline.sol#L21
- solidity/test_incorrect_deadline.sol#L39
- solidity/test_incorrect_deadline.sol#L40
- solidity/test_incorrect_deadline.sol#L43

### severity:
Optimization

### category:
use-custom-error
