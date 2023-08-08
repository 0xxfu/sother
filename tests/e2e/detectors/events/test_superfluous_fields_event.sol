// SPDX-License-Identifier: MIT

contract SuperfluousFieldsEvent {
    event BlockTimestampEvent(uint256 blockTimestamp);
    event BlockNumberEvent(uint256 blockNumber);
    event GoodEvent(uint256 xyz);

    function bad(uint256 abc) external {
        abc = abc + 1;
        emit GoodEvent(abc);
        emit BlockNumberEvent(block.number);
        emit BlockTimestampEvent(block.timestamp);
    }

    function good(uint256 abc) external {
        abc = abc + 1;
        emit GoodEvent(abc);
        emit BlockNumberEvent(abc + 1);
        emit BlockTimestampEvent(abc + 1);
        emit GoodEvent(_timestampToWeek(block.timestamp));
    }

    function _timestampToWeek(
        uint256 timestamp
    ) internal view returns (uint256) {
        return timestamp + 1;
    }
}
