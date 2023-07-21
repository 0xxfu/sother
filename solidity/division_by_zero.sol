contract DivisionByZero {
    function bad0(uint256 a, uint256 b) external pure {
        10 / a;

        f0() / a;

        10 / (a * b);

        10 / (f0() * a);
    }

    function notBad0(uint256 a, uint256 b) external pure {
        10 / a + 1;

        f0() / a - 1;

        10 / (a * b + 1);

        10 / (f0() * a - 100);
    }

    function f0() internal pure returns (uint256) {
        return 10;
    }
}
