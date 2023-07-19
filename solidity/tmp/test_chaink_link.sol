interface AggregatorInterface {
    function latestAnswer() external view returns (int256);

    function latestTimestamp() external view returns (uint256);

    function latestRound() external view returns (uint256);

    function getAnswer(uint256 roundId) external view returns (int256);

    function getTimestamp(uint256 roundId) external view returns (uint256);

    event AnswerUpdated(
        int256 indexed current,
        uint256 indexed roundId,
        uint256 updatedAt
    );

    event NewRound(
        uint256 indexed roundId,
        address indexed startedBy,
        uint256 startedAt
    );
}

interface AggregatorV3Interface {
    function decimals() external view returns (uint8);

    function description() external view returns (string memory);

    function version() external view returns (uint256);

    function getRoundData(uint80 _roundId)
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );

    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

contract AggregatorFacade is AggregatorInterface, AggregatorV3Interface {
    AggregatorInterface public aggregator;
    uint8 public override decimals;
    string public override description;

    uint256 public constant override version = 2;

    // An error specific to the Aggregator V3 Interface, to prevent possible
    // confusion around accidentally reading unset values as reported values.
    string private constant V3_NO_DATA_ERROR = "No data present";

    constructor(
        address _aggregator,
        uint8 _decimals,
        string memory _description
    ) public {
        aggregator = AggregatorInterface(_aggregator);
        decimals = _decimals;
        description = _description;
    }

    /**
     * @notice get the latest completed round where the answer was updated
     * @dev #[deprecated]. Use latestRoundData instead. This does not error if no
     * answer has been reached, it will simply return 0. Either wait to point to
     * an already answered Aggregator or use the recommended latestRoundData
     * instead which includes better verification information.
     */
    function latestRound() external view virtual override returns (uint256) {
        return aggregator.latestRound();
    }

    /**
     * @notice Reads the current answer from aggregator delegated to.
     *
     * @dev #[deprecated] Use latestRoundData instead. This does not error if no
     * answer has been reached, it will simply return 0. Either wait to point to
     * an already answered Aggregator or use the recommended latestRoundData
     * instead which includes better verification information.
     */
    function latestAnswer() external view virtual override returns (int256) {
        return aggregator.latestAnswer();
    }

    /**
     * @notice Reads the last updated height from aggregator delegated to.
     *
     * @dev #[deprecated] Use latestRoundData instead. This does not error if no
     * answer has been reached, it will simply return 0. Either wait to point to
     * an already answered Aggregator or use the recommended latestRoundData
     * instead which includes better verification information.
     */
    function latestTimestamp()
        external
        view
        virtual
        override
        returns (uint256)
    {
        return aggregator.latestTimestamp();
    }

    /**
     * @notice get data about the latest round. Consumers are encouraged to check
     * that they're receiving fresh data by inspecting the updatedAt value.
     * @return roundId is the round ID for which data was retrieved
     * @return answer is the answer for the given round
     * @return startedAt is always equal to updatedAt because the underlying
     * Aggregator contract does not expose this information.
     * @return updatedAt is the timestamp when the round last was updated (i.e.
     * answer was last computed)
     * @return answeredInRound is always equal to roundId because the underlying
     * Aggregator contract does not expose this information.
     * @dev Note that for rounds that haven't yet received responses from all
     * oracles, answer and updatedAt may change between queries.
     */
    function latestRoundData()
        external
        view
        virtual
        override
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        )
    {
        return _getRoundData(uint80(aggregator.latestRound()));
    }

    /**
     * @notice get past rounds answers
     * @param _roundId the answer number to retrieve the answer for
     *
     * @dev #[deprecated] Use getRoundData instead. This does not error if no
     * answer has been reached, it will simply return 0. Either wait to point to
     * an already answered Aggregator or use the recommended getRoundData
     * instead which includes better verification information.
     */
    function getAnswer(uint256 _roundId)
        external
        view
        virtual
        override
        returns (int256)
    {
        return aggregator.getAnswer(_roundId);
    }

    /**
     * @notice get block timestamp when an answer was last updated
     * @param _roundId the answer number to retrieve the updated timestamp for
     *
     * @dev #[deprecated] Use getRoundData instead. This does not error if no
     * answer has been reached, it will simply return 0. Either wait to point to
     * an already answered Aggregator or use the recommended getRoundData
     * instead which includes better verification information.
     */
    function getTimestamp(uint256 _roundId)
        external
        view
        virtual
        override
        returns (uint256)
    {
        return aggregator.getTimestamp(_roundId);
    }

    /**
     * @notice get data about a round. Consumers are encouraged to check
     * that they're receiving fresh data by inspecting the updatedAt value.
     * @param _roundId the round ID to retrieve the round data for
     * @return roundId is the round ID for which data was retrieved
     * @return answer is the answer for the given round
     * @return startedAt is always equal to updatedAt because the underlying
     * Aggregator contract does not expose this information.
     * @return updatedAt is the timestamp when the round last was updated (i.e.
     * answer was last computed)
     * @return answeredInRound is always equal to roundId because the underlying
     * Aggregator contract does not expose this information.
     * @dev Note that for rounds that haven't yet received responses from all
     * oracles, answer and updatedAt may change between queries.
     */
    function getRoundData(uint80 _roundId)
        external
        view
        virtual
        override
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        )
    {
        return _getRoundData(_roundId);
    }

    /*
     * Internal
     */

    function _getRoundData(uint80 _roundId)
        internal
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        )
    {
        answer = aggregator.getAnswer(_roundId);
        updatedAt = uint64(aggregator.getTimestamp(_roundId));

        require(updatedAt > 0, V3_NO_DATA_ERROR);

        return (_roundId, answer, updatedAt, updatedAt, _roundId);
    }
}

contract UncheckedReturns {
    AggregatorV3Interface public aggregator;

    uint256 private constant maxDelayTime = 10;

    function bad() external view returns (int256, bool) {
        (uint80 roundId, int256 price, , , uint80 answeredInRound) = aggregator
            .latestRoundData();
        bool valid = price > 0 && answeredInRound == roundId;

        return (price, valid);
    }

    function bad2() external view returns (int256, bool) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = aggregator.latestRoundData();
        bool valid = price > 0 && answeredInRound == roundId;

        return (price, valid);
    }

    function bad3() external view returns (int256, bool) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = aggregator.latestRoundData();

        bool valid = price > 0 &&
            answeredInRound == roundId &&
            ((block.timestamp - updatedAt) <= 10);

        return (price, valid);
    }

    function good1() external view returns (int256) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = aggregator.latestRoundData();

        if (updatedAt < roundId) {
            revert("Stale price");
        }
        if (answeredInRound < roundId) {
            revert("answer is being carried over");
        }
        if (startedAt == 0) {
            revert("Round not complete");
        }
        if (price == 0) {
            revert("answer reporting 0");
        }

        if (updatedAt < block.timestamp - maxDelayTime) {
            revert("time err");
        }

        return price;
    }

    function good2() external view returns (int256) {
        (
            uint80 roundId,
            int256 price,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = aggregator.latestRoundData();
        checkChainlink(roundId, price, startedAt, updatedAt, answeredInRound);
        return price;
    }

    function checkChainlink(
        uint80 roundId,
        int256 price,
        uint256 startedAt,
        uint256 updatedAt,
        uint80 answeredInRound
    ) internal view {
        if (updatedAt < roundId) {
            revert("Stale price");
        }
        if (answeredInRound < roundId) {
            revert("answer is being carried over");
        }
        if (startedAt == 0) {
            revert("Round not complete");
        }
        if (price == 0) {
            revert("answer reporting 0");
        }

        if (updatedAt < block.timestamp - maxDelayTime) {
            revert("time err");
        }
    }
}
