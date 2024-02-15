// Original license: SPDX_License_Identifier: GPL-3.0-or-later
pragma solidity >=0.7.0;

import { IVault } from "./interfaces/IVault.sol";
import { IAsset } from "./interfaces/IAsset.sol";
import { AggregatorV3Interface } from "./interfaces/AggregatorV3Interface.sol";

contract SlipageRequester {
    address public balancerAddress;

    constructor() {
        balancerAddress = address(0xE39B5e3B6D74016b2F6A9673D7d7493B6DF549d5);
    }

    /**
     * @dev Fetches the slippage
     * @param poolId_ the unique identifier of the requested token pool
     * @param kind_ ∈ {GIVEN_IN, GIVEN_OUT}
     * @param tokenA_ the address of the firs token in the pair
     * @param tokenB_ the address of the second token
     * @param amount_ the sum x token decimals
     * @param sender_ a valid EOA's address
     * @param dataFeedA_ the address of the Chainlink data feed for token A
     * @param dataFeedB_ the address of the Chainlink data feed for token B
     * @return USD equivalent
     */
    function getSlippage(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_,
        address dataFeedA_,
        address dataFeedB_
    )
        external
        returns (
            int256,
            int256,
            int256
        )
    {
        uint256 returnValue = _getSwapValue(
            poolId_,
            kind_,
            tokenA_,
            tokenB_,
            amount_,
            sender_
        );

        // Get the token prices
        int256 tokenAPrice = _getChainlinkPrice(dataFeedA_);
        int256 tokenBPrice = _getChainlinkPrice(dataFeedB_);

        // Calculate the expected and observed values in USD
        uint256 expected = (amount_ * uint256(tokenAPrice)) /
            (10**AggregatorV3Interface(dataFeedA_).decimals());
        uint256 actual = (returnValue * uint256(tokenBPrice)) /
            (10**AggregatorV3Interface(dataFeedB_).decimals());

        // Return the slippage
        return (tokenAPrice, tokenBPrice, int256(actual) - int256(expected));
    }

    function calculateFunctionSelector() external pure returns (bytes4) {
        return this.getSlippage.selector;
    }

    function _getChainlinkPrice(address dataFeed_)
        private
        view
        returns (int256)
    {
        (
            ,
            /* uint80 roundID */
            int256 answer, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = AggregatorV3Interface(dataFeed_).latestRoundData();

        return answer;
    }

    function _populateSingleSwap(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_
    ) private pure returns (IVault.SingleSwap memory) {
        return
            IVault.SingleSwap({
                poolId: poolId_,
                kind: kind_,
                assetIn: IAsset(tokenA_),
                assetOut: IAsset(tokenB_),
                amount: amount_,
                userData: bytes("")
            });
    }

    function _populateFundManagement(address sender_)
        private
        pure
        returns (IVault.FundManagement memory)
    {
        return
            IVault.FundManagement({
                sender: sender_,
                fromInternalBalance: false, // ignored
                recipient: payable(sender_),
                toInternalBalance: true // ignored
            });
    }

    function _getSwapValue(
        bytes32 poolId_,
        IVault.SwapKind kind_,
        address tokenA_,
        address tokenB_,
        uint256 amount_,
        address sender_
    ) private returns (uint256) {
        // Call querySwap with params
        bytes memory callData = abi.encodeWithSignature(
            "querySwap((bytes32, uint8, address, address, uint256, bytes),(address, bool, address, bool))",
            _populateSingleSwap(poolId_, kind_, tokenA_, tokenB_, amount_),
            _populateFundManagement(sender_)
        );

        (bool success, bytes memory data) = balancerAddress.call(callData);

        // Check success or revert
        require(success, "Call failed");

        // Convert the return value to uint256
        uint256 returnValue;
        assembly {
            returnValue := mload(add(data, 32))
        }

        return returnValue;
    }
}
