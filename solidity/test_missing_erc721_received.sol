interface IERC721 {
    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        bytes calldata data
    ) external;

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

contract BadMissReceived {
    function deposit(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(
            msg.sender,
            address(this),
            tokenId,
            new bytes(32)
        );
    }

    function deposit2(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(msg.sender, address(this), tokenId);
    }

    function deposit3(IERC721 token, uint256 tokenId) external {
        token.transferFrom(msg.sender, address(this), tokenId);
    }
}

contract NotBad {
    function deposit(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(
            msg.sender,
            address(this),
            tokenId,
            new bytes(32)
        );
    }

    function deposit2(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(msg.sender, address(this), tokenId);
    }

    function deposit3(IERC721 token, uint256 tokenId) external {
        token.transferFrom(msg.sender, address(this), tokenId);
    }

    function onERC721Received(
        address,
        address,
        uint256,
        bytes calldata
    ) external pure returns (bytes4) {
        return this.onERC721Received.selector;
    }
}
