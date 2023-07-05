contract UnsignedIntCompareZero {
    function bad(uint256 a) external pure {
        if (a > 0) {
            revert("err");
        }
    }

    function bad2(uint256 a) external pure {
        require(a > 0, "err");
    }

    function bad3(uint32 a) external pure {
        require(a > 0, "err");
    }

    function notBad(uint256 a) external pure {
        if (a != 0) {
            revert("err");
        }
    }

    function notBad2(uint256 a) external pure {
        require(a != 0, "err");
    }
}
