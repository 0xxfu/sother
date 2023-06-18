// SPDX-License-Identifier: MIT
contract StorageMemory {
    struct St {
        uint a;
    }

    uint[] arr;

    address testAddress;

    mapping(address => St) public userSt;

    function bad(uint testInt) external {
        St memory tmpSt = userSt[msg.sender];
        tmpSt.a = 1;
        userSt[msg.sender] = tmpSt;

        uint[] memory tmpArr = arr;
        tmpArr[0] = 1;
        arr = tmpArr;

        address tmpAddress = testAddress;
        tmpAddress = address(0);
        testAddress = tmpAddress;
    }

    function externalView(uint abc) external view returns (uint) {
        St memory tmpSt = userSt[msg.sender];
        return abc + tmpSt.a;
    }

    function externalPure(uint abc) external pure returns (uint) {
        // St memory tmpSt = userSt[msg.sender];
        return abc;
    }

    function internalView(uint abc) internal view returns (uint) {
        St memory tmpSt = userSt[msg.sender];
        return abc + tmpSt.a;
    }

    function good(uint testInt) external {
        userSt[msg.sender].a = 1;

        arr[0] = 0;
    }
}
