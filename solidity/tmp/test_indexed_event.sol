// SPDX-License-Identifier: MIT

contract IndexedEvent {
    event IntEvent(uint256 x);
    event IndexedIntEvent(uint256 indexed x);

    event IntsEvent(uint256 indexed x, uint256 y, uint256 z);
    event IndexedIntsEvent(
        uint256 indexed x,
        uint256 indexed y,
        uint256 indexed z
    );

    event IndexedMoreIntsEvent(
        uint256 indexed x,
        uint256 indexed y,
        uint256 indexed z,
        uint256 a
    );

    event AddrEvent(address x);
    event IndexedAddrEvent(address indexed x);

    event BoolEvent(bool x);
    event IndexedBoolEvent(bool indexed x);

    event BytesEvent(bytes x);
    event IndexedBytesEvent(bytes indexed x);

    event StrEvent(string x);
    event IndexedStrEvent(string indexed x);

    struct ABC {
        uint256 x;
    }

    event StructEvent(ABC x);
    event IndexedStructEvent(ABC indexed x);

    event ArrayEvent(uint256[] x);
    event IndexedArrayEvent(uint256[] x);

    // gas: 1465
    function emitIntEvent() external {
        emit IntEvent(1);
    }

    // gas: 1344 save: 121
    function emitIndexedIntEvent() external {
        emit IndexedIntEvent(1);
    }

    // gas: 2287
    function emitIntsEvent() external {
        emit IntsEvent(1, 1, 1);
    }

    // gas: 2121 save: 166
    function emitIndexedIntsEvent() external {
        emit IndexedIntsEvent(1, 1, 1);
    }

    // gas: 1450
    function emitAddrEvent() external {
        emit AddrEvent(msg.sender);
    }

    // gas: 1370 save: 80
    function emitIndexedAddrEvent() external {
        emit IndexedAddrEvent(msg.sender);
    }

    // gas: 1363
    function emitBoolEvent() external {
        emit BoolEvent(true);
    }

    // gas: 1328 save: 35
    function emitIndexedBoolEvent() external {
        emit IndexedBoolEvent(true);
    }

    // gas: 2035
    function emitBytesEvent() external {
        emit BytesEvent("hello");
    }

    // gas: 1653 save: 382
    function emitIndexedBytesEvent() external {
        emit IndexedBytesEvent("hello");
    }

    // gas: 1946
    function emitStrEvent() external {
        emit StrEvent("hello");
    }

    // gas: 1609 save: 337
    function emitIndexedStrEvent() external {
        emit IndexedStrEvent("hello");
    }

    // gas: 1481
    function emitStructEvent() external {
        emit StructEvent(ABC({x: 1}));
    }

    // gas: 1696 cost more: 215
    function emitIndexedStructEvent() external {
        emit IndexedStructEvent(ABC({x: 1}));
    }
}
