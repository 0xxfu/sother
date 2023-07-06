// SPDX-License-Identifier: MIT

contract RereadStateVariables {
    uint256 stateUint256;

    event StateEvent(uint256 state, uint256 a);

    function bad(uint256 x) external {
        uint256 a = stateUint256 + 1;
        uint256 b = stateUint256 + x;
        stateUint256 = a + b;
    }

    function bad2(uint256 x) external {
        uint256 a = stateUint256 + x;
        emit StateEvent(stateUint256, a);
    }

    function notBad(uint256 x) external {
        uint256 a = stateUint256 + 1;
        stateUint256 = x + 1;
        uint256 b = stateUint256 + x;
        stateUint256 = a + b;
    }

    function good(uint256 x) external {
        uint256 tmpState = stateUint256;
        uint256 a = tmpState + 1;
        uint256 b = tmpState + x;
        stateUint256 = a + b;
    }
}
