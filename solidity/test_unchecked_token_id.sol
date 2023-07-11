contract Bad {
    mapping(uint256 => address) private _owners;

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        returns (string memory)
    {
        string memory baseURI = "";
        return bytes(baseURI).length > 0 ? string.concat(baseURI, "") : "";
    }
}

contract NotBad0 {
    mapping(uint256 => address) private _owners;

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        returns (string memory)
    {
        if (_owners[tokenId] == address(0)) {
            revert("err");
        }

        string memory baseURI = "";
        return bytes(baseURI).length > 0 ? string.concat(baseURI, "") : "";
    }
}

contract NotBad1 {
    mapping(uint256 => address) private _owners;

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        returns (string memory)
    {
        _requireMinted(tokenId);

        string memory baseURI = "";
        return bytes(baseURI).length > 0 ? string.concat(baseURI, "") : "";
    }

    function _requireMinted(uint256 tokenId) internal view virtual {
        if (_owners[tokenId] == address(0)) {
            revert("err");
        }
    }
}
