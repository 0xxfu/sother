## Summary 

### Non-critical Issues

| |Issue|Instances|
|---|:---|:---:|
| [N-0] | Function Initializing State | 2 |
| [N-1] | Conformance to Solidity naming conventions | 16 |
| [N-2] | Variable names too similar | 11 |
| [N-3] | Unused state variable | 16 |


### Gas Optimizations

| |Issue|Instances|
|---|:---|:---:|
| [G-0] | State variables only set in the constructor should be declared immutable | 4 |
| [G-1] | Using `private` rather than `public` for constants, saves gas | 1 |
| [G-2] | State variables that could be declared constant | 7 |



## [Informational] Function Initializing State

### description:
Detects the immediate initialization of state variables through function calls that are not pure/constant, or that use non-constant state variable.

**There are `2` instances of this issue:**

- [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) is set pre-construction with a non-constant function or state variable:
	- getNumber()

- [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is set pre-construction with a non-constant function or state variable:
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


### recommendation:
Remove any initialization of state variables via non-constant state variables or function calls. If variables must be set upon contract deployment, locate initialization in the constructor instead.

### location:
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L67

### severity:
Informational

### category:
function-init-state

## [Informational] Conformance to Solidity naming conventions

### description:

Solidity defines a [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions) that should be followed.
#### Rule exceptions
- Allow constant variable name/symbol/decimals to be lowercase (`ERC20`).
- Allow `_` at the beginning of the `mixed_case` match for private variables and unused parameters.

**There are `16` instances of this issue:**

- Variable [Bad.should_be_immutable_5](solidity/immut_stat_variables.sol#L46) is not in mixedCase

- Constant [Good.should_be_constant_2](solidity/immut_stat_variables.sol#L64) is not in UPPER_CASE_WITH_UNDERSCORES

- Variable [Bad.should_be_constant_3](solidity/immut_stat_variables.sol#L42) is not in mixedCase

- Variable [Good.should_be_immutable_3](solidity/immut_stat_variables.sol#L68) is not in mixedCase

- Variable [Bad.should_be_constant_2](solidity/immut_stat_variables.sol#L41) is not in mixedCase

- Constant [Good.should_be_constant](solidity/immut_stat_variables.sol#L63) is not in UPPER_CASE_WITH_UNDERSCORES

- Variable [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is not in mixedCase

- Variable [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) is not in mixedCase

- Variable [Good.should_be_immutable_4](solidity/immut_stat_variables.sol#L69) is not in mixedCase

- Variable [Bad.should_be_immutable_3](solidity/immut_stat_variables.sol#L45) is not in mixedCase

- Variable [Bad.should_be_immutable](solidity/immut_stat_variables.sol#L43) is not in mixedCase

- Variable [Good.should_be_immutable_5](solidity/immut_stat_variables.sol#L70) is not in mixedCase

- Constant [Good.should_be_constant_3](solidity/immut_stat_variables.sol#L65) is not in UPPER_CASE_WITH_UNDERSCORES

- Variable [Bad.cannote_be_immutable](solidity/immut_stat_variables.sol#L47) is not in mixedCase

- Variable [Bad.should_be_constant](solidity/immut_stat_variables.sol#L40) is not in mixedCase

- Variable [Good.should_be_immutable](solidity/immut_stat_variables.sol#L66) is not in mixedCase


### recommendation:
Follow the Solidity [naming convention](https://solidity.readthedocs.io/en/v0.4.25/style-guide.html#naming-conventions).

### location:
- solidity/immut_stat_variables.sol#L46
- solidity/immut_stat_variables.sol#L64
- solidity/immut_stat_variables.sol#L42
- solidity/immut_stat_variables.sol#L68
- solidity/immut_stat_variables.sol#L41
- solidity/immut_stat_variables.sol#L63
- solidity/immut_stat_variables.sol#L67
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L69
- solidity/immut_stat_variables.sol#L45
- solidity/immut_stat_variables.sol#L43
- solidity/immut_stat_variables.sol#L70
- solidity/immut_stat_variables.sol#L65
- solidity/immut_stat_variables.sol#L47
- solidity/immut_stat_variables.sol#L40
- solidity/immut_stat_variables.sol#L66

### severity:
Informational

### category:
naming-convention

## [Informational] Variable names too similar

### description:
Detect variables with names that are too similar.

**There are `11` instances of this issue:**

- Variable [Good.should_be_immutable_3](solidity/immut_stat_variables.sol#L68) is too similar to [Good.should_be_immutable_5](solidity/immut_stat_variables.sol#L70)

- Variable [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_3](solidity/immut_stat_variables.sol#L68)

- Variable [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) is too similar to [Bad.should_be_immutable_3](solidity/immut_stat_variables.sol#L45)

- Variable [Good.should_be_immutable_3](solidity/immut_stat_variables.sol#L68) is too similar to [Good.should_be_immutable_4](solidity/immut_stat_variables.sol#L69)

- Variable [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) is too similar to [Bad.should_be_immutable_5](solidity/immut_stat_variables.sol#L46)

- Variable [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_4](solidity/immut_stat_variables.sol#L69)

- Variable [Bad.should_be_immutable_3](solidity/immut_stat_variables.sol#L45) is too similar to [Bad.should_be_immutable_5](solidity/immut_stat_variables.sol#L46)

- Variable [Bad.should_be_constant_2](solidity/immut_stat_variables.sol#L41) is too similar to [Bad.should_be_constant_3](solidity/immut_stat_variables.sol#L42)

- Variable [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is too similar to [Good.should_be_immutable_5](solidity/immut_stat_variables.sol#L70)

- Variable [Good.should_be_immutable_4](solidity/immut_stat_variables.sol#L69) is too similar to [Good.should_be_immutable_5](solidity/immut_stat_variables.sol#L70)

- Variable [Good.should_be_constant_2](solidity/immut_stat_variables.sol#L64) is too similar to [Good.should_be_constant_3](solidity/immut_stat_variables.sol#L65)

#### Exploit scenario
Bob uses several variables with similar names. As a result, his code is difficult to review.

### recommendation:
Prevent variables from having similar names.

### location:
- solidity/immut_stat_variables.sol#L68
- solidity/immut_stat_variables.sol#L67
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L68
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L67
- solidity/immut_stat_variables.sol#L45
- solidity/immut_stat_variables.sol#L41
- solidity/immut_stat_variables.sol#L67
- solidity/immut_stat_variables.sol#L69
- solidity/immut_stat_variables.sol#L64

### severity:
Informational

### category:
similar-names

## [Informational] Unused state variable

### description:
Unused state variable.

**There are `16` instances of this issue:**

- [Good.should_be_constant_2](solidity/immut_stat_variables.sol#L64) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [Bad.should_be_constant](solidity/immut_stat_variables.sol#L40) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [Good.should_be_immutable_4](solidity/immut_stat_variables.sol#L69) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [Bad.should_be_immutable](solidity/immut_stat_variables.sol#L43) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [Bad.should_be_immutable_3](solidity/immut_stat_variables.sol#L45) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [Good.should_be_constant](solidity/immut_stat_variables.sol#L63) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [Bad.should_be_constant_2](solidity/immut_stat_variables.sol#L41) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [Good.should_be_immutable](solidity/immut_stat_variables.sol#L66) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [A.TEXT1](solidity/immut_stat_variables.sol#L11) is never used in [B](solidity/immut_stat_variables.sol#L22-L35)

- [Good.should_be_immutable_3](solidity/immut_stat_variables.sol#L68) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [Bad.should_be_constant_3](solidity/immut_stat_variables.sol#L42) is never used in [Bad](solidity/immut_stat_variables.sol#L37-L58)

- [A.X](solidity/immut_stat_variables.sol#L10) is never used in [B](solidity/immut_stat_variables.sol#L22-L35)

- [A.text2](solidity/immut_stat_variables.sol#L12) is never used in [B](solidity/immut_stat_variables.sol#L22-L35)

- [Good.should_be_immutable_2](solidity/immut_stat_variables.sol#L67) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)

- [Good.should_be_constant_3](solidity/immut_stat_variables.sol#L65) is never used in [Good](solidity/immut_stat_variables.sol#L60-L81)


### recommendation:
Remove unused state variables.

### location:
- solidity/immut_stat_variables.sol#L64
- solidity/immut_stat_variables.sol#L40
- solidity/immut_stat_variables.sol#L69
- solidity/immut_stat_variables.sol#L43
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L45
- solidity/immut_stat_variables.sol#L63
- solidity/immut_stat_variables.sol#L41
- solidity/immut_stat_variables.sol#L66
- solidity/immut_stat_variables.sol#L11
- solidity/immut_stat_variables.sol#L68
- solidity/immut_stat_variables.sol#L42
- solidity/immut_stat_variables.sol#L10
- solidity/immut_stat_variables.sol#L12
- solidity/immut_stat_variables.sol#L67
- solidity/immut_stat_variables.sol#L65

### severity:
Informational

### category:
unused-state

## [Optimization] State variables only set in the constructor should be declared immutable

### description:

Avoids a Gsset (20000 gas) in the constructor, and replaces the first access in each transaction (Gcoldsload - 2100 gas) and each access thereafter (Gwarmacces - 100 gas) with a PUSH32 (3 gas).

While strings are not value types, and therefore cannot be immutable/constant if not hard-coded outside of the constructor, the same behavior can be achieved by making the current contract abstract with virtual functions for the string accessors, and having a child contract override the functions with the hard-coded implementation-specific values.
    

**There are `4` instances of this issue:**

- [Bad.should_be_immutable_5](solidity/immut_stat_variables.sol#L46) should be immutable 

- [Bad.should_be_immutable_2](solidity/immut_stat_variables.sol#L44) should be immutable 

- [Bad.should_be_immutable](solidity/immut_stat_variables.sol#L43) should be immutable 

- [Bad.should_be_immutable_3](solidity/immut_stat_variables.sol#L45) should be immutable 


### recommendation:
Add the `immutable` attribute to state variables that never change or are set only in the constructor.

### location:
- solidity/immut_stat_variables.sol#L46
- solidity/immut_stat_variables.sol#L44
- solidity/immut_stat_variables.sol#L43
- solidity/immut_stat_variables.sol#L45

### severity:
Optimization

### category:
immutable-states

## [Optimization] Using `private` rather than `public` for constants, saves gas

### description:

If needed, the values can be read from the verified contract source code, or if there are multiple values there can be a single getter function that [returns a tuple](https://github.com/code-423n4/2022-08-frax/blob/90f55a9ce4e25bceed3a74290b854341d8de6afa/src/contracts/FraxlendPair.sol#L156-L178) of the values of all currently-public constants. 

Saves **3406-3606 gas** in deployment gas due to the compiler not having to create non-payable getter functions for deployment calldata, not having to store the bytes of the value outside of where it's used, and not adding another entry to the method ID table


**There is `1` instance of this issue:**

- [A.MY_ADDRESS](solidity/immut_stat_variables.sol#L4) should be used `private` visibility to save gas.


### recommendation:

Using `private` replace `public` with constant.


### location:
- solidity/immut_stat_variables.sol#L4

### severity:
Optimization

### category:
public-to-private-constant

## [Optimization] State variables that could be declared constant

### description:
State variables that are not updated following deployment should be declared constant to save gas.

**There are `7` instances of this issue:**

- [A.text2](solidity/immut_stat_variables.sol#L12) should be constant 

- [Bad.should_be_constant_2](solidity/immut_stat_variables.sol#L41) should be constant 

- [B.mySistersAddress](solidity/immut_stat_variables.sol#L24) should be constant 

- [A.myFriendsAddress](solidity/immut_stat_variables.sol#L5) should be constant 

- [Bad.should_be_constant](solidity/immut_stat_variables.sol#L40) should be constant 

- [Bad.should_be_constant_3](solidity/immut_stat_variables.sol#L42) should be constant 

- [A.test](solidity/immut_stat_variables.sol#L8) should be constant 


### recommendation:
Add the `constant` attribute to state variables that never change.

### location:
- solidity/immut_stat_variables.sol#L12
- solidity/immut_stat_variables.sol#L41
- solidity/immut_stat_variables.sol#L24
- solidity/immut_stat_variables.sol#L5
- solidity/immut_stat_variables.sol#L40
- solidity/immut_stat_variables.sol#L42
- solidity/immut_stat_variables.sol#L8

### severity:
Optimization

### category:
constable-states
