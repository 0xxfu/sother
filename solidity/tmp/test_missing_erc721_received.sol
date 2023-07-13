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

contract BadUnchecked {
    function deposit(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(
            address(this),
            msg.sender,
            tokenId,
            new bytes(32)
        );
    }

    function deposit2(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(address(this), msg.sender, tokenId);
    }

    function deposit3(IERC721 token, uint256 tokenId) external {
        token.transferFrom(address(this), msg.sender, tokenId);
    }
}

interface IERC721Receiver {
    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes calldata data
    ) external returns (bytes4);
}

contract NotBadChecked {
    function deposit(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(
            address(this),
            msg.sender,
            tokenId,
            new bytes(32)
        );
        try
            IERC721Receiver(msg.sender).onERC721Received(
                address(this),
                msg.sender,
                tokenId,
                ""
            )
        returns (bytes4 retval) {
            if (retval != IERC721Receiver.onERC721Received.selector) {
                revert("error");
            }
        } catch (bytes memory reason) {
            if (reason.length == 0) {
                revert("error");
            } else {
                /// @solidity memory-safe-assembly
                assembly {
                    revert(add(32, reason), mload(reason))
                }
            }
        }
    }

    function deposit2(IERC721 token, uint256 tokenId) external {
        token.safeTransferFrom(address(this), msg.sender, tokenId);
        if (!_checkOnERC721Received(address(this), msg.sender, tokenId, "")) {
            revert("error");
        }
    }

    function deposit3(IERC721 token, uint256 tokenId) external {
        token.transferFrom(address(this), msg.sender, tokenId);
        if (!_checkOnERC721Received(address(this), msg.sender, tokenId, "")) {
            revert("error");
        }
    }

    function _checkOnERC721Received(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) private returns (bool) {
        if (to.code.length > 0) {
            try
                IERC721Receiver(to).onERC721Received(
                    address(this),
                    from,
                    tokenId,
                    data
                )
            returns (bytes4 retval) {
                return retval == IERC721Receiver.onERC721Received.selector;
            } catch (bytes memory reason) {
                if (reason.length == 0) {
                    revert("error");
                } else {
                    assembly {
                        revert(add(32, reason), mload(reason))
                    }
                }
            }
        } else {
            return true;
        }
    }
}
