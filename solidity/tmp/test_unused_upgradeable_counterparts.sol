abstract contract Initializable {}

contract ERC20 {}

abstract contract ERC20Upgradeable is Initializable {}

contract BadUpgradeable is Initializable, ERC20 {}

contract NotBadUpgradeable is Initializable, ERC20Upgradeable {}
