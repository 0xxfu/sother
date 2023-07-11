library Strings {
    function toString(uint256 value) internal pure returns (string memory) {
        unchecked {}
    }
}

contract UnprotectedNFTFork {
    using Strings for uint256;
    string baseURI;

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        returns (string memory)
    {
        return
            bytes(baseURI).length > 0
                ? string.concat(baseURI, tokenId.toString())
                : "";
    }
}

contract ProtectedNFTFork {
    using Strings for uint256;
    string baseURI;

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        returns (string memory)
    {
        require(1 == block.chainid);
        return
            bytes(baseURI).length > 0
                ? string.concat(baseURI, tokenId.toString())
                : "";
    }
}
