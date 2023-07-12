interface IERC165 {
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}

interface IERC721 is IERC165 {}

interface IERC721Metadata is IERC721 {}

abstract contract ERC165 is IERC165 {
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        returns (bool)
    {
        return interfaceId == type(IERC165).interfaceId;
    }
}

abstract contract AbstractERC721 {
    function ownerOf(uint256 tokenId) public view virtual returns (address) {
        return address(0);
    }

    function safeTransferFrom(
        address from,
        address to,
        uint256 tokenId
    ) public virtual {}
}

contract Bad721 is AbstractERC721, ERC165, IERC721 {}

contract Bad721_2 is ERC165, AbstractERC721, IERC721Metadata {
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC165, IERC165)
        returns (bool)
    {
        return
            interfaceId == type(IERC721Metadata).interfaceId ||
            super.supportsInterface(interfaceId);
    }
}

contract Bad721_3 is ERC165, AbstractERC721, IERC721Metadata {
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC165, IERC165)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}

contract NotBad721 is ERC165, AbstractERC721, IERC721Metadata {
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC165, IERC165)
        returns (bool)
    {
        return
            interfaceId == type(IERC721).interfaceId ||
            interfaceId == type(IERC721Metadata).interfaceId ||
            super.supportsInterface(interfaceId);
    }
}
