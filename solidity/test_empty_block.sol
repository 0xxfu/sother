contract EmptyBlock {
    uint256 a;

    constructor() {}

    receive() external payable {}

    function bad1() external virtual {}

    function bad2() external view virtual returns (uint256) {}

    function notBad() external pure returns (uint256) {
        return 1;
    }

    function notBad2() external {
        a = a + 1;
    }
}

abstract contract NotEmptyBlock {
    function notBad1() external virtual {}

    function notBad2() external view virtual returns (uint256) {}
}

abstract contract ExplicitAbstract{
    function f() virtual public;
}