## Summary 

### Gas Optimizations

|ID|Issues|Instances|
|---|:---|:---:|
| [G-0] | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables | 2 |



## [Optimization] `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables

### description:
Using the addition operator instead of plus-equals saves **[113 gas](https://gist.github.com/0xxfu/86ae4bdd07d7db169cea110dba5a5af4)**

**There are `2` instances of this issue:**

- should use arithmetic operator `=` replace `+=` in [varr += block.number](solidity/test_assignment_operation.sol#L14)
- should use arithmetic operator `=` replace `-=` in [varr -= 0](solidity/test_assignment_operation.sol#L21)

### recommendation:
Using arithmetic operator `=` replace assignment operator `+=` or `-=` 

### location:
- solidity/test_assignment_operation.sol#L14
- solidity/test_assignment_operation.sol#L21

### severity:
Optimization

### category:
assignment-left-operation
