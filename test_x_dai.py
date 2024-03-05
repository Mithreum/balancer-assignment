from utils import main

# https://docs.balancer.fi/reference/contracts/deployment-addresses/gnosis.html

#TESTS

tests = [
    {
        'pair': 'WETH / USDC',
        'rpc_url':'https://gnosis.drpc.org', # xDai
        'contract': '0x6b30f76CecE9F92D27f0e9Ad78312E77709E74A5', # xDai
        'function': '0x3087bfd8', # Function signature
        'pool_id': '0x4d7adc5e362a97b5ba1b02bc0447249ac81e76ad00010000000000000000003e',
        'kind': '0x00',
        'token_a':'0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1', # WETH
        'token_b': '0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83',# USDC
        'a_decimals': 18,
        'b_decimals': 6,
        'amount': 1_000_000_000_000_000,
        'sender': '0xC523433AC1Cc396fA58698739b3B0531Fe6C4268', # any valid EVM address
        'feed_a': '0xa767f745331D267c7751297D982b050c93985627', # ETH/USD Replace with the actual address of Chainlink data feed for token A
        'feed_b': '0x26C31ac71010aF62E6B486D1132E266D6298857D' # USDC/USD Replace with the actual address of Chainlink data feed for token B
    }

]

main(tests)