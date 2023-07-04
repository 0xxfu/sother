contract PrePlusPlus {
    function bad(uint256 a) external pure {
        a++;
    }

    function bad2(uint256 a) external pure {
        a--;
    }

    function bad3(uint256 a) external pure {
        a += 1;
    }

    function bad4(uint256 a) external pure {
        a -= 1;
    }

    function bad5(uint256 a) external pure {
        for (uint256 i; i < a; i++) {
            a -= 1;
        }
    }

    function bad6(uint256 a) external pure {
        for (uint256 i = 1; i > 1; i--) {
            a += 1;
        }
    }

    function notBad(uint256 a) external pure {
        ++a;
    }

    function notBad2(uint256 a) external pure {
        --a;
    }
}
