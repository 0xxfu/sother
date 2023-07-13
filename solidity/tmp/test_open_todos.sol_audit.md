## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | OPEN TODOs | 3 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 1 |



## [Low] OPEN TODOs

### description:

Open To-dos can point to architecture or programming issues that still
need to be resolved. Often these kinds of comments indicate areas of
complexity or confusion for developers. This provides value and insight
to an attacker who aims to cause damage to the protocol.


**There are `3` instances of this issue:**

- Todo in [OpenTodo](solidity/test_open_todos.sol#L8-L21) content: 
	- `    // todo state`
	- `    uint256 x; // todo implement update x`
	- `        // todo implement x+y`
	- `        x = x + 1; // todo x+y+z`
	- `        return 1; // todo in code line`
	- `    // todo end contract`

- Todo in [OpenTodo](solidity/test_open_todos.sol#L8-L21) comments: 
	- ` todo in contract`

- Todo in [OpenTodo2](solidity/test_open_todos.sol#L24-L37) content: 
	- `    // todo state`
	- `    uint256 x; // todo implement update x`
	- `        // todo implement x+y`
	- `        x = x + 1; // todo x+y+z`
	- `        return 1; // todo in code line`
	- `    // todo end contract`


### recommendation:

Consider resolving the To-dos before deploying code to a production
context. Use an independent issue tracker or other project management
software to track development tasks.


### locations:
- solidity/test_open_todos.sol#L8-L21
- solidity/test_open_todos.sol#L8-L21
- solidity/test_open_todos.sol#L24-L37

### severity:
Low

### category:
open-todos

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
