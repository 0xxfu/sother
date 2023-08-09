contract RevertLongString {
    error NotBadRevert();

    function bad(uint256 a) external pure {
        if (a != 0) {
            revert("long long long long long long long");
        }
    }

    function bad2(uint256 a) external pure {
        require(a != 0, "long long long long long long long");
    }

    function notBad(uint256 a) external pure {
        if (a != 0) {
            revert("long long");
        }
    }

    function notBad2(uint256 a) external pure {
        require(a != 0, "long long");
    }

    function notBad3(uint256 a) external pure {
        if (a != 0) {
            revert NotBadRevert();
        }
    }

    function notBad4(uint256 a) external pure {
        require(a != 0);
    }
}
