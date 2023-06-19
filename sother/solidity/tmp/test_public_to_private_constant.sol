// SPDX-License-Identifier: MIT

contract PublicToPrivateConstant {
    uint256 public constant pUint256 = 123456789;
    address public constant pAddress = address(0);
    bytes public constant pBytes = "Hello,World";
    uint256 private constant priUint256 = 123456789;
    address private constant priAddress = address(0);
    bytes private constant priBytes = "Hello,World";
}
