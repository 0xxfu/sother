# Sother

Sother is a Solidity static analyzer base on [Slither](https://github.com/crytic/slither) and aggregates most of [Falcon's](https://github.com/MetaTrustLabs/falcon-metatrust) detectors.

## Install

```shell
poetry install
```

## Usage

detect vulnerability and print default markdown:

```shell
sother ./solidity --print markdown
```

## Detectors stat

```
------ All ------
High: 34
Medium: 47
Low: 52
Informational: 28
Optimization: 50
Total: 211

------ Sother ------
High: 2
Medium: 18
Low: 35
Informational: 5
Optimization: 45
Total: 105

------ Slither ------
High: 27
Medium: 21
Low: 14
Informational: 21
Optimization: 5
Total: 88

------ Falcon ------
High: 24
Medium: 20
Low: 11
Informational: 16
Optimization: 2
Total: 73
```

## Detectors list

| Num | Check                                | What it Detects                                                                                                 | Impact        | Confidence    |
| --- | ------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------- | ------------- |
| 1   | abiencoderv2-array                   | Storage abiencoderv2 array                                                                                      | High          | High          |
| 2   | arbitrary-send-erc20                 | transferFrom uses arbitrary `from`                                                                              | High          | High          |
| 3   | array-by-reference                   | Modifying storage array by value                                                                                | High          | High          |
| 4   | incorrect-constructor-name           | https://swcregistry.io/docs/SWC-118                                                                             | High          | High          |
| 5   | incorrect-shift                      | The order of parameters in a shift instruction is incorrect.                                                    | High          | High          |
| 6   | integer-underflow                    | contract needs to check if the function input incase of integer underflow or overflow                           | High          | High          |
| 7   | multiple-constructors                | Multiple constructor schemes                                                                                    | High          | High          |
| 8   | name-reused                          | Contract's name reused                                                                                          | High          | High          |
| 9   | protected-vars                       | Detected unprotected variables                                                                                  | High          | High          |
| 10  | public-mappings-nested               | Public mappings with nested variables                                                                           | High          | High          |
| 11  | rtlo                                 | Right-To-Left-Override control character is used                                                                | High          | High          |
| 12  | shadowing-state                      | State variables shadowing                                                                                       | High          | High          |
| 13  | sig-replay-attacks-protection        | SWC-121: Missing Protection Against Signature Replay Attacks                                                    | High          | High          |
| 14  | state-variable-not-initialized       | Detect that state variable not initialized and not written in contract but be used in contract                  | High          | High          |
| 15  | suicidal                             | Functions allowing anyone to destruct the contract                                                              | High          | High          |
| 16  | unchecked-ecrecover                  | return value of 0 from `ecrecover` not checked                                                                  | High          | High          |
| 17  | uninitialized-state                  | Uninitialized state variables                                                                                   | High          | High          |
| 18  | uninitialized-storage                | Uninitialized storage variables                                                                                 | High          | High          |
| 19  | unprotected-ether-withdrawal         | https://swcregistry.io/docs/SWC-105                                                                             | High          | High          |
| 20  | unprotected-upgrade                  | Unprotected upgradeable contract                                                                                | High          | High          |
| 21  | codex                                | Use Codex to find vulnerabilities.                                                                              | High          | Low           |
| 22  | arbitrary-send-erc20-permit          | transferFrom uses arbitrary from with permit                                                                    | High          | Medium        |
| 23  | arbitrary-send-eth                   | Functions that send Ether to arbitrary destinations                                                             | High          | Medium        |
| 24  | controlled-array-length              | Tainted array length assignment                                                                                 | High          | Medium        |
| 25  | controlled-delegatecall              | Controlled delegatecall destination                                                                             | High          | Medium        |
| 26  | defi-action-nested                   | transferFrom uses arbitrary from with permit                                                                    | High          | Medium        |
| 27  | delegatecall-loop                    | Payable functions using `delegatecall` inside a loop                                                            | High          | Medium        |
| 28  | modifier-unsafe                      | Modifier Unsafe                                                                                                 | High          | Medium        |
| 29  | msg-value-loop                       | msg.value inside a loop                                                                                         | High          | Medium        |
| 30  | reentrancy-eth                       | Reentrancy vulnerabilities (theft of ethers)                                                                    | High          | Medium        |
| 31  | signature-malleability               | https://swcregistry.io/docs/SWC-117                                                                             | High          | Medium        |
| 32  | storage-array                        | Signed storage integer array compiler bug                                                                       | High          | Medium        |
| 33  | weak-prng                            | Weak PRNG                                                                                                       | High          | Medium        |
| 34  | constant-result                      | Tautology Fixed                                                                                                 | Medium        | High          |
| 35  | deprecated-approve                   | `Approve` Race Condition                                                                                        | Medium        | High          |
| 36  | deprecated-chainlink                 | Usage of deprecated ChainLink APIs                                                                              | Medium        | High          |
| 37  | domain-separator-collision           | Detects ERC20 tokens that have a function whose signature collides with EIP-2612's DOMAIN_SEPARATOR()           | Medium        | High          |
| 38  | enum-conversion                      | Detect dangerous enum conversion                                                                                | Medium        | High          |
| 39  | erc20-interface                      | Incorrect ERC20 interfaces                                                                                      | Medium        | High          |
| 40  | erc721-interface                     | Incorrect ERC721 interfaces                                                                                     | Medium        | High          |
| 41  | hardcode-gas-amount                  | https://swcregistry.io/docs/SWC-134                                                                             | Medium        | High          |
| 42  | ignored-chainlink-returns            | `latestRoundData` returns has been ignored                                                                      | Medium        | High          |
| 43  | incorrect-equality                   | Dangerous strict equalities                                                                                     | Medium        | High          |
| 44  | integer-overflow                     | contract needs to check if the function input incase of integer underflow or overflow                           | Medium        | High          |
| 45  | invalid-array-deletion               | Deletion on array containing a structure                                                                        | Medium        | High          |
| 46  | lack-deadline-in-uniswap             | Lack of deadline for Uniswap AMM                                                                                | Medium        | High          |
| 47  | lack-slippage-protection             | Lack of slippage protection can lead to significant loss of user funds                                          | Medium        | High          |
| 48  | locked-ether                         | Contracts that lock ether                                                                                       | Medium        | High          |
| 49  | mapping-deletion                     | Deletion on mapping containing a structure                                                                      | Medium        | High          |
| 50  | missing-gap-state-variable           | Upgradeable contract is missing a `__gap` storage variable to allow for new storage variables in later versions | Medium        | High          |
| 51  | owner-centralization                 | The owner is a single point of failure and a centralization risk                                                | Medium        | High          |
| 52  | shadowing-abstract                   | State variables shadowing from abstract contracts                                                               | Medium        | High          |
| 53  | tautology                            | Tautology or contradiction                                                                                      | Medium        | High          |
| 54  | unchecked-chainlink-round            | Unchecked return data `roundId` from Chainlink aggregators                                                      | Medium        | High          |
| 55  | unchecked-chainlink-staleness        | `latestRoundData` might return stale results                                                                    | Medium        | High          |
| 56  | unsafe-transfer                      | Unsafe use of `transfer()/transferFrom()` with IERC20                                                           | Medium        | High          |
| 57  | void-function                        | Function not implemented                                                                                        | Medium        | High          |
| 58  | write-after-write                    | Unused write                                                                                                    | Medium        | High          |
| 59  | arbitrary-storage-location           | https://swcregistry.io/docs/SWC-124                                                                             | Medium        | Low           |
| 60  | for-continue-increment               | Loop might turn out infinite                                                                                    | Medium        | Low           |
| 61  | tx-gas-price-warning                 | The contract uses tx.gasprice variable                                                                          | Medium        | Low           |
| 62  | boolean-cst                          | Misuse of Boolean constant                                                                                      | Medium        | Medium        |
| 63  | bytes-variables-risk                 | Contract respects e standard                                                                                    | Medium        | Medium        |
| 64  | constant-function-asm                | Constant functions using assembly code                                                                          | Medium        | Medium        |
| 65  | constant-function-state              | Constant functions changing the state                                                                           | Medium        | Medium        |
| 66  | divide-before-multiply               | Imprecise arithmetic operations order                                                                           | Medium        | Medium        |
| 67  | fee-on-transfer                      | Incompatibility with transfer-on-fee or deflationary tokens                                                     | Medium        | Medium        |
| 68  | functiontype-var                     | contract needs to check if there are function type variable to avoid Arbitrary Jump with Function Type Variable | Medium        | Medium        |
| 69  | public-mint-burn                     |                                                                                                                 | Medium        | Medium        |
| 70  | reentrancy-no-eth                    | Reentrancy vulnerabilities (no theft of ethers)                                                                 | Medium        | Medium        |
| 71  | reused-constructor                   | Reused base constructor                                                                                         | Medium        | Medium        |
| 72  | transfer-in-loop                     | ether transfer inside a loop                                                                                    | Medium        | Medium        |
| 73  | tx-origin                            | Dangerous usage of `tx.origin`                                                                                  | Medium        | Medium        |
| 74  | unchecked-lowlevel                   | Unchecked low-level calls                                                                                       | Medium        | Medium        |
| 75  | unchecked-send                       | Unchecked send                                                                                                  | Medium        | Medium        |
| 76  | unchecked-transfer                   | Return values of `transfer()/transferFrom()` not checked                                                        | Medium        | Medium        |
| 77  | uninitialized-local                  | Uninitialized local variables                                                                                   | Medium        | Medium        |
| 78  | unsafe-721-mint                      | Use `_safeMint` instead of `_mint` for ERC721                                                                   | Medium        | Medium        |
| 79  | unsafe-721-transfer                  | Using `ERC721.transferFrom()` may cause the user's NFT to be frozen in a contract that does not support ERC721  | Medium        | Medium        |
| 80  | unused-return                        | Unused return values                                                                                            | Medium        | Medium        |
| 81  | deprecated-assert                    | `revert CustomError()` should be used instead of `assert()`                                                     | Low           | High          |
| 82  | deprecated-ownable                   | Lack of a double-step `transferOwnership()` pattern                                                             | Low           | High          |
| 83  | deprecated-safe-approve              | `safeApprove()` is deprecated due to `Approve` Race Condition                                                   | Low           | High          |
| 84  | division-by-zero                     | Division by zero not prevented                                                                                  | Low           | High          |
| 85  | encode-packed-collision              | ABI encodePacked Collision                                                                                      | Low           | High          |
| 86  | external-calls-in-loop               | External calls in an un-bounded `for-`loop may result in a DOS                                                  | Low           | High          |
| 87  | incorrect-deadline                   | Incorrect EIP-2612 deadline check                                                                               | Low           | High          |
| 88  | incorrect-modifier                   | Modifiers that can return the default value                                                                     | Low           | High          |
| 89  | missing-erc721-received              | `onERC721Received` not implemented in ERC721 received contract                                                  | Low           | High          |
| 90  | missing-sender-in-event              | Events are missing sender information                                                                           | Low           | High          |
| 91  | missing-supports-interface           | Missing `supportsInterface` functions                                                                           | Low           | High          |
| 92  | non-compliant-erc721                 | NFT token do not comply with `ERC721`, breaking composability                                                   | Low           | High          |
| 93  | open-todos                           | OPEN TODOs                                                                                                      | Low           | High          |
| 94  | payable-calls                        | Don't use `payable.transfer()`/`payable.send()`                                                                 | Low           | High          |
| 95  | reentrancy-send-value                | Missing Reentrancy-Guard when using `sendValue` from OZ's `Address.sol`                                         | Low           | High          |
| 96  | reentrancy-transfer                  | Functions calling contracts/addresses with transfer hooks are missing reentrancy guards                         | Low           | High          |
| 97  | revert-on-approve-max                | Approve `type(uint256).max` not work with some tokens                                                           | Low           | High          |
| 98  | revert-on-total-supply               | Calls will revert when `totalSupply()` returns zero                                                             | Low           | High          |
| 99  | shadowing-builtin                    | Built-in symbol shadowing                                                                                       | Low           | High          |
| 100 | shadowing-local                      | Local variables shadowing                                                                                       | Low           | High          |
| 101 | susceptible-ecrecover                | Direct usage of `ecrecover` allows signature malleability                                                       | Low           | High          |
| 102 | unchecked-array-length               | Missing array length check when inputting multiple arrays                                                       | Low           | High          |
| 103 | unchecked-erc721-received            | `onERC721Received` callback is never called when new tokens are minted or transferred                           | Low           | High          |
| 104 | unchecked-setters                    | Setters should check the input value                                                                            | Low           | High          |
| 105 | unchecked-token-id                   | `tokenURI()` does not follow EIP-721                                                                            | Low           | High          |
| 106 | uninitialized-fptr-cst               | Uninitialized function pointer calls in constructors                                                            | Low           | High          |
| 107 | unnecessary-reentrancy-guard         | Function not implemented                                                                                        | Low           | High          |
| 108 | unprotected-nft-fork                 | NFT doesn't handle hard forks                                                                                   | Low           | High          |
| 109 | unprotected-upgrade-front-run        | Use `disableInitializers` to prevent front-running on the initialize function                                   | Low           | High          |
| 110 | unsafe-assembly                      | Storage Write Removal Bug On Conditional Early Termination                                                      | Low           | High          |
| 111 | unsafe-double-cast                   | Double type casts create complexity within the code                                                             | Low           | High          |
| 112 | unsafe-downcast                      | Unsafe downcasting arithmetic operation                                                                         | Low           | High          |
| 113 | unsafe-floating-pragma               | Unsafe to use floating pragma                                                                                   | Low           | High          |
| 114 | unsafe-solmate-transfer-lib          | Solmate's `SafeTransferLib` doesn't check whether the ERC20 contract exists                                     | Low           | High          |
| 115 | unsafe-tx-origin                     | Use of `tx.origin` is unsafe in almost every context                                                            | Low           | High          |
| 116 | unsupported-decimals-token           | Unsafe calls to optional ERC20 functions:`decimals()`/`name()`/`symbol()`                                       | Low           | High          |
| 117 | unused-upgradeable-counterparts      | Contracts are not using their OZ Upgradeable counterparts                                                       | Low           | High          |
| 118 | upgradeable-uninitialized            | Upgradeable contracts are not initialized                                                                       | Low           | High          |
| 119 | variable-scope                       | Local variables used prior their declaration                                                                    | Low           | High          |
| 120 | void-cst                             | Constructor called not implemented                                                                              | Low           | High          |
| 121 | pess-only-eoa-check                  | msg.sender == tx.origin                                                                                         | Low           | Low           |
| 122 | calls-loop                           | Multiple calls in a loop                                                                                        | Low           | Medium        |
| 123 | events-access                        | Missing Events Access Control                                                                                   | Low           | Medium        |
| 124 | events-maths                         | Missing Events Arithmetic                                                                                       | Low           | Medium        |
| 125 | incorrect-unary                      | Dangerous unary expressions                                                                                     | Low           | Medium        |
| 126 | initialize-permission                | initialize method should has permission check                                                                   | Low           | Medium        |
| 127 | input-validation                     | input validation                                                                                                | Low           | Medium        |
| 128 | missing-zero-check                   | Missing Zero Address Validation                                                                                 | Low           | Medium        |
| 129 | pess-event-setter                    | Contract function does not emit event after the value is set                                                    | Low           | Medium        |
| 130 | reentrancy-benign                    | Benign reentrancy vulnerabilities                                                                               | Low           | Medium        |
| 131 | reentrancy-events                    | Reentrancy vulnerabilities leading to out-of-order Events                                                       | Low           | Medium        |
| 132 | timestamp                            | Dangerous usage of `block.timestamp`                                                                            | Low           | Medium        |
| 133 | assembly                             | Assembly usage                                                                                                  | Informational | High          |
| 134 | assert-state-change                  | Assert state change                                                                                             | Informational | High          |
| 135 | cyclomatic-complexity                | Detects functions with high (> 11) cyclomatic complexity                                                        | Informational | High          |
| 136 | deprecated-standards                 | Deprecated Solidity Standards                                                                                   | Informational | High          |
| 137 | erc20-indexed                        | Un-indexed ERC20 event parameters                                                                               | Informational | High          |
| 138 | function-init-state                  | Function initializing state variables                                                                           | Informational | High          |
| 139 | immutable-in-upgradeable             | Immutable variables used in upgradable contracts may cause DoS                                                  | Informational | High          |
| 140 | low-level-calls                      | Low level calls                                                                                                 | Informational | High          |
| 141 | missing-inheritance                  | Missing inheritance                                                                                             | Informational | High          |
| 142 | missing-msg-in-require               | Missing Error Messages in `require/revert` Statements                                                           | Informational | High          |
| 143 | naming-convention                    | Conformity to Solidity naming conventions                                                                       | Informational | High          |
| 144 | no-license                           | No SPDX license identifier                                                                                      | Informational | High          |
| 145 | obsolete-use                         | Deprecated Solidity Standards                                                                                   | Informational | High          |
| 146 | pragma                               | If different pragma directives are used                                                                         | Informational | High          |
| 147 | redundant-statements                 | Redundant statements                                                                                            | Informational | High          |
| 148 | slither-incorrect-using-for          | Detects using-for statement usage when no function from a given library matches a given type                    | Informational | High          |
| 149 | solc-version                         | Incorrect Solidity version                                                                                      | Informational | High          |
| 150 | unimplemented-functions              | Unimplemented functions                                                                                         | Informational | High          |
| 151 | unnecessary-public-function-modifier | Unnecessary Public Function and can be replaced with external                                                   | Informational | High          |
| 152 | unused-event                         | Unused events                                                                                                   | Informational | High          |
| 153 | upgrade-to-latest                    | Should use latest solidity version                                                                              | Informational | High          |
| 154 | using-for-any-type                   | Using for any type '\*'                                                                                         | Informational | Informational |
| 155 | costly-loop                          | Costly operations in a loop                                                                                     | Informational | Medium        |
| 156 | error-msg                            | Code style required                                                                                             | Informational | Medium        |
| 157 | reentrancy-unlimited-gas             | Reentrancy vulnerabilities through send and transfer                                                            | Informational | Medium        |
| 158 | similar-names                        | Variable names are too similar                                                                                  | Informational | Medium        |
| 159 | too-many-digits                      | Conformance to numeric notation best practices                                                                  | Informational | Medium        |
| 160 | uncontrolled-resource-consumption    | https://swcregistry.io/docs/SWC-128                                                                             | Informational | Medium        |
| 161 | array-length-in-loop                 | Cache the `<array>.length` for the loop condition                                                               | Optimization  | High          |
| 162 | assembly-update-address              | Use `assembly` to write address storage values                                                                  | Optimization  | High          |
| 163 | assignment-left-operation            | `<x> += <y>` costs more gas than `<x> = <x> + <y>` for state variables                                          | Optimization  | High          |
| 164 | bool-state-variables                 | Use `uint256(1)/uint256(2)` instead for `true` and `false` boolean states                                       | Optimization  | High          |
| 165 | boolean-equal                        | Don't compare booleans to `true` or `false`                                                                     | Optimization  | High          |
| 166 | cache-call-function-result           | The result of function calls should be cached rather than re-calling the function                               | Optimization  | High          |
| 167 | constable-states                     | State variables that could be declared constant                                                                 | Optimization  | High          |
| 168 | dead-code                            | Functions that are not used                                                                                     | Optimization  | High          |
| 169 | divide-by-constant                   | Using `x >> constant(uint)` with the right shift operator is a more gas-efficient                               | Optimization  | High          |
| 170 | empty-block                          | Empty blocks should be removed or emit something                                                                | Optimization  | High          |
| 171 | external-function                    | Public function that could be declared external                                                                 | Optimization  | High          |
| 172 | fetch-storage-to-memory              | Using `storage` instead of `memory` for structs/arrays saves gas                                                | Optimization  | High          |
| 173 | immutable-states                     | State variables that could be declared immutable                                                                | Optimization  | High          |
| 174 | inefficient-new-bytes                | Expression `""` is cheaper than `new bytes(0)`                                                                  | Optimization  | High          |
| 175 | internal-function-to-inline          | `internal` functions only called once can be inlined to save gas                                                | Optimization  | High          |
| 176 | memory-in-parameters                 | Use `calldata` instead of `memory` for function parameters                                                      | Optimization  | High          |
| 177 | mul-power-two                        | Multiplications of powers of 2 can be replaced by a left shift operation to save gas                            | Optimization  | High          |
| 178 | multiple-address-mappings            | Multiple address `mappings` can be combined into a single `mapping`                                             | Optimization  | High          |
| 179 | operator-and-in-require              | Splitting `&&` in `require()` statements to saves gas                                                           | Optimization  | High          |
| 180 | payable-constructor                  | Setting the constructor to `payable`                                                                            | Optimization  | High          |
| 181 | payable-function                     | Functions guaranteed to revert when called by normal users can be marked `payable`                              | Optimization  | High          |
| 182 | pre-plus-plus                        | `++i` costs less gas than `i++`, especially when it's used in for-loops (`--i/i--` too)                         | Optimization  | High          |
| 183 | public-to-private-constant           | Using `private` rather than `public` for constants, saves gas                                                   | Optimization  | High          |
| 184 | reread-state-variables               | Cache state variables instead of rereading                                                                      | Optimization  | High          |
| 185 | revert-long-strings                  | Shortening revert strings to fit in 32 `bytes`                                                                  | Optimization  | High          |
| 186 | safe-math-lib                        | Don't use `SafeMath` if use solidity version `>=0.8.0`                                                          | Optimization  | High          |
| 187 | slither-cache-array-length           | Detects `for` loops that use `length` member of some storage array in their loop condition and don't modify it. | Optimization  | High          |
| 188 | smaller-uint-int                     | Usage of `uints`/`ints` smaller than 32 bytes (256 bits) incurs overhead                                        | Optimization  | High          |
| 189 | state-should-be-constant             | State variables that could be declared constant                                                                 | Optimization  | High          |
| 190 | string-constants                     | `Bytes` constants are more efficient than `string` constants                                                    | Optimization  | High          |
| 191 | superfluous-fields-event             | Superfluous fields in event                                                                                     | Optimization  | High          |
| 192 | unchecked-in-loop                    | The increment `++i/i++` in `for-loop`/`while-loop` post condition can be made `unchecked{++i}/unchecked{i++}`   | Optimization  | High          |
| 193 | unindexed-event                      | Use indexed events for value types as they are less costly compared to non-indexed ones                         | Optimization  | High          |
| 194 | unnecessary-reentrancy-lock          | Unnecessary reentrancy lock in the function                                                                     | Optimization  | High          |
| 195 | unsigned-int-compare-zero            | `!= 0` is less gas than `> 0` for unsigned integers                                                             | Optimization  | High          |
| 196 | unused-error                         | Remove unused error definition                                                                                  | Optimization  | High          |
| 197 | unused-local-var                     | Remove unused local variables                                                                                   | Optimization  | High          |
| 198 | unused-named-return-variables        | Not using the named return variables anywhere in the function is confusing                                      | Optimization  | High          |
| 199 | unused-parameter                     | Remove unused parameter variables                                                                               | Optimization  | High          |
| 200 | unused-state-variables               | Remove or replace unused state variables                                                                        | Optimization  | High          |
| 201 | unused-struct                        | Remove unused struct declaration                                                                                | Optimization  | High          |
| 202 | use-assembly-balance                 | Use `balance(address)` instead of address.balance()                                                             | Optimization  | High          |
| 203 | use-concat-on-bytes                  | Use `bytes.concat()` on mixing bytes and strings instead of `abi.encodePacked()` to save gas                    | Optimization  | High          |
| 204 | use-concat-on-string                 | Use `string.concat()` on string instead of `abi.encodePacked()` to save gas                                     | Optimization  | High          |
| 205 | use-delete-statement                 | Use `delete` to Clear Variables                                                                                 | Optimization  | High          |
| 206 | use-self-balance                     | Use `selfbalance()` instead of `address(this).balance`                                                          | Optimization  | High          |
| 207 | var-read-using-this                  | Contract reads its own variable using `this`                                                                    | Optimization  | High          |
| 208 | zero-address-optimization            | Use assembly to check for `address(0)`                                                                          | Optimization  | High          |
| 209 | zero-check-with-transfer             | Amounts should be checked for `0` before calling a `transfer`                                                   | Optimization  | High          |
| 210 | zero-initialized-state-variable      | It costs more gas to initialize state variables to zero than to let the default of zero be applied              | Optimization  | High          |
