
interface IERC721 {
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;

    function transferFrom(
        address from,
        address to,
        uint256 tokenId
    ) external;
}

contract ERC721 {
    function _safeMint(address to, uint256 tokenId) internal virtual {
        _safeMint(to, tokenId, "");
    }

    function _safeMint(
        address to,
        uint256 tokenId,
        bytes memory _data
    ) internal virtual {
        _mint(to, tokenId);
    }

    function _mint(address to, uint256 tokenId) internal virtual {
        require(to != address(0), "ERC721: mint to the zero address");
    }

    function ownerOf(uint256 tokenId) public view virtual returns (address) {
        return address(0);
    }
}

contract UnsafeErc721Mint is ERC721 {
    function mintBuggy(address to, uint256 tokenId) external {
        _mint(to, tokenId);
    }

    function goodMint(address to, uint256 tokenId) external {
        _safeMint(to, tokenId);
    }
}
