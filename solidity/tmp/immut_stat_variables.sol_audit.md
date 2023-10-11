## Summary 

### Low Risk Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [L-0] | Setters should check the input value | 3 |
| [L-1] | Missing Event Setter | 8 |


### Non-critical Issues

|ID|Issues|Instances|
|---|:---|:---:|
| [N-0] | Incorrect versions of Solidity | 2 |
| [N-1] | Function Initializing State | 2 |
| [N-2] | Conformance to Solidity naming conventions | 16 |
| [N-3] | Variable names too similar | 11 |
| [N-4] | SPDX license Identifier | 1 |
| [N-5] | Unnecessary Public Function Modifier | 4 |


### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 4 |
| [G-1] | Should use latest solidity version `0.8.21` for gas reduction and improved security. | 1 |
| [G-2] | Using `private` rather than `public` for constants, saves gas | 1 |
| [G-3] | Setting the constructor to `payable` | 2 |
| [G-4] | Do not calculate constants | 1 |
| [G-5] | Use `delete` to Clear Variables | 1 |
| [G-6] | State variables that could be declared constant | 7 |
| [G-7] | State variables that could be declared constant | 6 |



## [Low] Setters should check the input value

### description

Setters should have initial value check to prevent assigning wrong value to the variable. 
Assignment of wrong value can lead to unexpected behavior of the contract.


**There are `3` instances of this issue:**

- [B.setUsed(uint256).a](solidity/tmp/immut_stat_variables.sol#L30) lacks an upper limit check on :
	- [used = a](solidity/tmp/immut_stat_variables.sol#L32)

- [Bad.constructor(uint256,string).b](solidity/tmp/immut_stat_variables.sol#L49) lacks an upper limit check on :
	- [should_be_immutable_5 = b](solidity/tmp/immut_stat_variables.sol#L50)

- [Good.constructor(uint256).b](solidity/tmp/immut_stat_variables.sol#L72) lacks an upper limit check on :
	- [should_be_immutable_5 = b](solidity/tmp/immut_stat_variables.sol#L73)


### recommendation

Add an upper limit check to the setters function.


### locations
- solidity/tmp/immut_stat_variables.sol#L30
- solidity/tmp/immut_stat_variables.sol#L49
- solidity/tmp/immut_stat_variables.sol#L72

### severity
Low

### category
unchecked-setters

### confidence
High

## [Low] Missing Event Setter

### description
Setter-functions must emit events

**There are `8` instances of this issue:**

- Setter function [B.slitherConstructorVariables()](solidity/tmp/immut_stat_variables.sol#L22-L35) does not emit an event

- Setter function [B.slitherConstructorConstantVariables()](solidity/tmp/immut_stat_variables.sol#L22-L35) does not emit an event

- Setter function [B.fallback()](solidity/tmp/immut_stat_variables.sol#L26-L28) does not emit an event

- Setter function [B.setUsed(uint256)](solidity/tmp/immut_stat_variables.sol#L30-L34) does not emit an event

- Setter function [Bad.slitherConstructorVariables()](solidity/tmp/immut_stat_variables.sol#L37-L58) does not emit an event

- Setter function [Bad.slitherConstructorConstantVariables()](solidity/tmp/immut_stat_variables.sol#L37-L58) does not emit an event

- Setter function [Good.slitherConstructorConstantVariables()](solidity/tmp/immut_stat_variables.sol#L60-L81) does not emit an event

- Setter function [Good.slitherConstructorVariables()](solidity/tmp/immut_stat_variables.sol#L60-L81) does not emit an event

#### Exploit scenario
N/A

### recommendation
Emit events in setter functions

### locations
- solidity/tmp/immut_stat_variables.sol#L22-L35
- solidity/tmp/immut_stat_variables.sol#L22-L35
- solidity/tmp/immut_stat_variables.sol#L26-L28
- solidity/tmp/immut_stat_variables.sol#L30-L34
- solidity/tmp/immut_stat_variables.sol#L37-L58
- solidity/tmp/immut_stat_variables.sol#L37-L58
- solidity/tmp/immut_stat_variables.sol#L60-L81
- solidity/tmp/immut_stat_variables.sol#L60-L81

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

**There are `2` instances of this issue:**

- Pragma version[0.8.17](solidity/tmp/immut_stat_variables.sol#L1) allows old versions

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
- solidity/tmp/immut_stat_variables.sol#L1
- 

### severity
Informational

### category
solc-version

### confidence
High

## [Informational] Function Initializing State

### description
Detects the immediate initialization of state variables through function calls that are not pure/constant, or that use non-constant state variable.

**There are `2` instances of this issue:**

- [Bad.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L44) is set pre-construction with a non-constant function or state variable:
	- getNumber()

- [Good.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L67) is set pre-construction with a non-constant function or state variable:
	- getNumber()

#### Exploit scenario

```solidity
contract StateVarInitFromFunction {

    uint public v = set(); // Initialize from function (sets to 77)
    uint public w = 5;
    uint public x = set(); // Initialize from function (sets to 88)
    address public shouldntBeReported = address(8);

    constructor(){
        // The constructor is run after all state variables are initialized.
    }

    function set() public  returns(uint)  {
        // If this function is being used to initialize a state variable declared
        // before w, w will be zero. If it is declared after w, w will be set.
        if(w == 0) {
            return 77;
        }

        return 88;
    }
}
```
In this case, users might intend a function to return a value a state variable can initialize with, without realizing the context for the contract is not fully initialized. 
In the example above, the same function sets two different values for state variables because it checks a state variable that is not yet initialized in one case, and is initialized in the other. 
Special care must be taken when initializing state variables from an immediate function call so as not to incorrectly assume the state is initialized.


### recommendation
Remove any initialization of state variables via non-constant state variables or function calls. If variables must be set upon contract deployment, locate initialization in the constructor instead.

### locations
- solidity/tmp/immut_stat_variables.sol#L44
- solidity/tmp/immut_stat_variables.sol#L67

### severity
Informational

### category
function-init-state

### confidence
High

## [Informational] Conformance to Solidity naming conventions

### description

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `16` instances of this issue:**

- Variable [Bad.should_be_constant](solidity/tmp/immut_stat_variables.sol#L40) is not in mixedCase

- Variable [Bad.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L41) is not in mixedCase

- Variable [Bad.should_be_constant_3](solidity/tmp/immut_stat_variables.sol#L42) is not in mixedCase

- Variable [Bad.should_be_immutable](solidity/tmp/immut_stat_variables.sol#L43) is not in mixedCase

- Variable [Bad.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L44) is not in mixedCase

- Variable [Bad.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L45) is not in mixedCase

- Variable [Bad.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L46) is not in mixedCase

- Variable [Bad.cannote_be_immutable](solidity/tmp/immut_stat_variables.sol#L47) is not in mixedCase

- Constant [Good.should_be_constant](solidity/tmp/immut_stat_variables.sol#L63) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [Good.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L64) is not in UPPER_CASE_WITH_UNDERSCORES

- Constant [Good.should_be_constant_3](solidity/tmp/immut_stat_variables.sol#L65) is not in UPPER_CASE_WITH_UNDERSCORES

- Variable [Good.should_be_immutable](solidity/tmp/immut_stat_variables.sol#L66) is not in mixedCase

- Variable [Good.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L67) is not in mixedCase

- Variable [Good.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L68) is not in mixedCase

- Variable [Good.should_be_immutable_4](solidity/tmp/immut_stat_variables.sol#L69) is not in mixedCase

- Variable [Good.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L70) is not in mixedCase


### recommendation
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### locations
- solidity/tmp/immut_stat_variables.sol#L40
- solidity/tmp/immut_stat_variables.sol#L41
- solidity/tmp/immut_stat_variables.sol#L42
- solidity/tmp/immut_stat_variables.sol#L43
- solidity/tmp/immut_stat_variables.sol#L44
- solidity/tmp/immut_stat_variables.sol#L45
- solidity/tmp/immut_stat_variables.sol#L46
- solidity/tmp/immut_stat_variables.sol#L47
- solidity/tmp/immut_stat_variables.sol#L63
- solidity/tmp/immut_stat_variables.sol#L64
- solidity/tmp/immut_stat_variables.sol#L65
- solidity/tmp/immut_stat_variables.sol#L66
- solidity/tmp/immut_stat_variables.sol#L67
- solidity/tmp/immut_stat_variables.sol#L68
- solidity/tmp/immut_stat_variables.sol#L69
- solidity/tmp/immut_stat_variables.sol#L70

### severity
Informational

### category
naming-convention

### confidence
High

## [Informational] Variable names too similar

### description
Detect variables with names that are too similar.

**There are `11` instances of this issue:**

- Variable [Bad.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L41) is too similar to [Bad.should_be_constant_3](solidity/tmp/immut_stat_variables.sol#L42)

- Variable [Bad.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L44) is too similar to [Bad.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L45)

- Variable [Bad.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L44) is too similar to [Bad.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L46)

- Variable [Bad.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L45) is too similar to [Bad.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L46)

- Variable [Good.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L64) is too similar to [Good.should_be_constant_3](solidity/tmp/immut_stat_variables.sol#L65)

- Variable [Good.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L68)

- Variable [Good.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_4](solidity/tmp/immut_stat_variables.sol#L69)

- Variable [Good.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L70)

- Variable [Good.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L68) is too similar to [Good.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L70)

- Variable [Good.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L68) is too similar to [Good.should_be_immutable_4](solidity/tmp/immut_stat_variables.sol#L69)

- Variable [Good.should_be_immutable_4](solidity/tmp/immut_stat_variables.sol#L69) is too similar to [Good.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L70)

#### Exploit scenario
Bob uses several variables with similar names. As a result, his code is difficult to review.

### recommendation
Prevent variables from having similar names.

### locations
- solidity/tmp/immut_stat_variables.sol#L41
- solidity/tmp/immut_stat_variables.sol#L44
- solidity/tmp/immut_stat_variables.sol#L44
- solidity/tmp/immut_stat_variables.sol#L45
- solidity/tmp/immut_stat_variables.sol#L64
- solidity/tmp/immut_stat_variables.sol#L67
- solidity/tmp/immut_stat_variables.sol#L67
- solidity/tmp/immut_stat_variables.sol#L67
- solidity/tmp/immut_stat_variables.sol#L68
- solidity/tmp/immut_stat_variables.sol#L68
- solidity/tmp/immut_stat_variables.sol#L69

### severity
Informational

### category
similar-names

### confidence
Medium

## [Informational] SPDX license Identifier

### description
The source file does not specify SPDX license identifier.

**There is `1` instance of this issue:**

- key[A](solidity/tmp/immut_stat_variables.sol#L2-L19) does not specify SPDX license identifier
#### Exploit scenario

    pragma solidity ^0.4.24;

    contract NoLicense {

    function noLicense() public {
    }

    }
    

### recommendation
Consider adding the SPDX license identifier before deployment.

### locations
- solidity/tmp/immut_stat_variables.sol#L2-L19

### severity
Informational

### category
no-license

### confidence
High

## [Informational] Unnecessary Public Function Modifier

### description
Detect the public function which can be replaced with external

**There are `4` instances of this issue:**

- function:[A.setUsed()](solidity/tmp/immut_stat_variables.sol#L14-L18)is public and can be replaced with external 

- function:[B.setUsed(uint256)](solidity/tmp/immut_stat_variables.sol#L30-L34)is public and can be replaced with external 

- function:[Bad.getNumber()](solidity/tmp/immut_stat_variables.sol#L54-L56)is public and can be replaced with external 

- function:[Good.getNumber()](solidity/tmp/immut_stat_variables.sol#L76-L78)is public and can be replaced with external 

#### Exploit scenario

```solidity
contract A{}
contract B is A{
    constructor() public A(){}
}
```
When reading `B`'s constructor definition, we might assume that `A()` initiates the contract, but no code is executed.

### recommendation
Replace public with external

### locations
- solidity/tmp/immut_stat_variables.sol#L14-L18
- solidity/tmp/immut_stat_variables.sol#L30-L34
- solidity/tmp/immut_stat_variables.sol#L54-L56
- solidity/tmp/immut_stat_variables.sol#L76-L78

### severity
Informational

### category
unnecessary-public-function-modifier

### confidence
High

## [Optimization] State variables only set in the constructor should be declared immutable

### description

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There are `4` instances of this issue:**

- [Bad.should_be_immutable](solidity/tmp/immut_stat_variables.sol#L43) should be immutable 

- [Bad.should_be_immutable_2](solidity/tmp/immut_stat_variables.sol#L44) should be immutable 

- [Bad.should_be_immutable_3](solidity/tmp/immut_stat_variables.sol#L45) should be immutable 

- [Bad.should_be_immutable_5](solidity/tmp/immut_stat_variables.sol#L46) should be immutable 


### recommendation
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### locations
- solidity/tmp/immut_stat_variables.sol#L43
- solidity/tmp/immut_stat_variables.sol#L44
- solidity/tmp/immut_stat_variables.sol#L45
- solidity/tmp/immut_stat_variables.sol#L46

### severity
Optimization

### category
immutable-states

### confidence
High

## [Optimization] Should use latest solidity version `0.8.21` for gas reduction and improved security.

### description

[Solidity `0.8.21`](https://soliditylang.org/blog/2023/07/19/solidity-0.8.21-release-announcement) has many optimization with compiler and bugfixes, 
please upgrade Solidity to the latest version(`0.8.21`) for gas reduction and improved security.


**There is `1` instance of this issue:**

- pragma solidity version [0.8.17](solidity/tmp/immut_stat_variables.sol#L1) should upgrade to the latest version: 0.8.21

### recommendation
Upgrade solidity version to the latest version: 0.8.21

### locations
- solidity/tmp/immut_stat_variables.sol#L1

### severity
Optimization

### category
upgrade-to-latest

### confidence
High

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There is `1` instance of this issue:**

- [A.MY_ADDRESS](solidity/tmp/immut_stat_variables.sol#L4) should be used `private` visibility to save gas.


### recommendation

Using `private` replace `public` with constant.


### locations
- solidity/tmp/immut_stat_variables.sol#L4

### severity
Optimization

### category
public-to-private-constant

### confidence
High

## [Optimization] Setting the constructor to `payable`

### description

You can cut out 10 opcodes in the creation-time EVM bytecode 
if you declare a constructor `payable`. 
Making the constructor `payable` eliminates the need for an initial check 
of `msg.value == 0` and saves `13 gas` on deployment with no security risks.


**There are `2` instances of this issue:**

- [Bad.constructor(uint256,string)](solidity/tmp/immut_stat_variables.sol#L49-L52) should be set to `payable` 

- [Good.constructor(uint256)](solidity/tmp/immut_stat_variables.sol#L72-L74) should be set to `payable` 


### recommendation

Set the constructor to `payable`.


### locations
- solidity/tmp/immut_stat_variables.sol#L49-L52
- solidity/tmp/immut_stat_variables.sol#L72-L74

### severity
Optimization

### category
payable-constructor

### confidence
High

## [Optimization] Do not calculate constants

### description

Due to how constant variables are implemented (replacements at compile-time), 
an expression assigned to a constant variable is recomputed each time that the variable is used, 
which wastes some gas.

See: [ethereum/solidity#9232](https://github.com/ethereum/solidity/issues/9232):
> each usage of a "constant" costs ~100gas more on each access (it is still a little better than storing the result in storage, but not much..)

> since these are not real constants, they can't be referenced from a real constant environment (e.g. from assembly, or from another library )



**There is `1` instance of this issue:**

- [Good.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L64) should use hardcode instead of calculation.


### recommendation

Pre-calculate the results(hardcode) instead of calculation in runtime.


### locations
- solidity/tmp/immut_stat_variables.sol#L64

### severity
Optimization

### category
calculate-constants

### confidence
High

## [Optimization] Use `delete` to Clear Variables

### description

delete a assigns the initial value for the type to a. i.e. 
for integers it is equivalent to a = 0, but it can also be used on arrays, 
where it assigns a dynamic array of length zero or a static array of the same 
length with all elements reset. For structs, it assigns a struct with all members reset. 
Similarly, it can also be used to set an address to zero address. 
It has no effect on whole mappings though (as the keys of mappings may be arbitrary 
and are generally unknown). However, individual keys and what they map to can be deleted: 
If a is a mapping, then delete a[x] will delete the value stored at x.

The delete key better conveys the intention and is also more idiomatic. 
Consider replacing assignments of zero with delete statements.


**There is `1` instance of this issue:**

- Should use `delete` statement instead of [used = 0](solidity/tmp/immut_stat_variables.sol#L27)


### recommendation

Replacing assignments of zero with delete statements.



### locations
- solidity/tmp/immut_stat_variables.sol#L27

### severity
Optimization

### category
use-delete-statement

### confidence
High

## [Optimization] State variables that could be declared constant

### description
State variables that are not updated following deployment should be declared constant to save gas.

**There are `7` instances of this issue:**

- [A.myFriendsAddress](solidity/tmp/immut_stat_variables.sol#L5) should be constant 

- [A.test](solidity/tmp/immut_stat_variables.sol#L8) should be constant 

- [A.text2](solidity/tmp/immut_stat_variables.sol#L12) should be constant 

- [B.mySistersAddress](solidity/tmp/immut_stat_variables.sol#L24) should be constant 

- [Bad.should_be_constant](solidity/tmp/immut_stat_variables.sol#L40) should be constant 

- [Bad.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L41) should be constant 

- [Bad.should_be_constant_3](solidity/tmp/immut_stat_variables.sol#L42) should be constant 


### recommendation
Add the `constant` attribute to state variables that never change.

### locations
- solidity/tmp/immut_stat_variables.sol#L5
- solidity/tmp/immut_stat_variables.sol#L8
- solidity/tmp/immut_stat_variables.sol#L12
- solidity/tmp/immut_stat_variables.sol#L24
- solidity/tmp/immut_stat_variables.sol#L40
- solidity/tmp/immut_stat_variables.sol#L41
- solidity/tmp/immut_stat_variables.sol#L42

### severity
Optimization

### category
constable-states

### confidence
High

## [Optimization] State variables that could be declared constant

### description
Constant state variables should be declared constant to save gas.

**There are `6` instances of this issue:**

- [A.myFriendsAddress](solidity/tmp/immut_stat_variables.sol#L5) should be constant

- [A.test](solidity/tmp/immut_stat_variables.sol#L8) should be constant

- [A.text2](solidity/tmp/immut_stat_variables.sol#L12) should be constant

- [B.mySistersAddress](solidity/tmp/immut_stat_variables.sol#L24) should be constant

- [Bad.should_be_constant](solidity/tmp/immut_stat_variables.sol#L40) should be constant

- [Bad.should_be_constant_2](solidity/tmp/immut_stat_variables.sol#L41) should be constant


### recommendation
Add the `constant` attributes to state variables that never change.

### locations
- solidity/tmp/immut_stat_variables.sol#L5
- solidity/tmp/immut_stat_variables.sol#L8
- solidity/tmp/immut_stat_variables.sol#L12
- solidity/tmp/immut_stat_variables.sol#L24
- solidity/tmp/immut_stat_variables.sol#L40
- solidity/tmp/immut_stat_variables.sol#L41

### severity
Optimization

### category
state-should-be-constant

### confidence
High
