contract UseConcat {
    function bad() external pure {
        // gas 384
        abi.encodePacked("a");
        // gas 783
        abi.encodePacked("a", new bytes(0));

        abi.encodePacked("a", bytes32(0));
    }

    function notBad() external pure {
        // 279
        string.concat("a");
        // gas 601
        bytes.concat(new bytes(0), new bytes(0));

        bytes.concat("a", new bytes(0));
    }

    function notBad2() external pure {
        abi.encodePacked(new bytes(0));
        abi.encodePacked(new bytes(0), new bytes(0));
    }
}
