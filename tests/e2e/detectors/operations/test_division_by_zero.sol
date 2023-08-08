contract DivisionByZero {
    uint256 constant x = 1;

    function bad0(uint256 a, uint256 b) external pure {
        10 / a;

        f0() / a;

        10 / (a * b);

        10 / (f0() * a);
    }

    function notBad0(uint256 a, uint256 b) external pure {
        if (a == 0) {
            revert();
        }
        if (b == 0) {
            revert();
        }
        10 / a;

        f0() / a;

        10 / (a * b);

        10 / (f0() * a);

        a / x;
    }

    function notBad1(uint256 a, uint256 b) external pure {
        require(a != 0);
        require(b != 0);
        10 / a;

        f0() / a;

        10 / (a * b);

        10 / (f0() * a);
    }

    function notBad2(uint256 a, uint256 b) external pure {
        10 / (a + 1);

        f0() / a - 1;

        10 / (a * b + 1);

        10 / (f0() * a - 100);

        a / 1;

        a / (b + 1);
    }

    function f0() internal pure returns (uint256) {
        return 10;
    }
}
