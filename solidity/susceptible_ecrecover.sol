contract SusceptibleEcrecover {
    function bad(
        bytes32 digest,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        return ecrecover(digest, v, r, s);
    }

    function bad2(
        bytes32 digest,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        address result = ecrecover(digest, v, r, s);
        return result;
    }

    function notBad(
        bytes32 digest,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        address result = ecrecover(digest, v, r, s);
        require(result != address(0), "address err");
        return result;
    }

    function notBad2(
        bytes32 digest,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public pure returns (address) {
        address result = ecrecover(digest, v, r, s);
        if (result == address(0)) {
            revert("addr err");
        }
        return result;
    }
}
