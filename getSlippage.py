from utils import main

tests = [
    {
        'pair': 'USDC / WMATIC',
        'rpc_url':'https://polygon.drpc.org', # Polygon
        'contract': '0x0A6A1Beb7b0b3545578818f45f4e6219615d25aD', # Polygon
        'function': '0x3087bfd8', # Function signature
        'pool_id': '0x0297e37f1873d2dab4487aa67cd56b58e2f27875000100000000000000000002',
        'kind': '0x00',
        'token_a':'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', # USDC.e or Replace with the actual address of tokenA
        'token_b': '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',# WMATIC or Replace with the actual address of tokenB 
        'a_decimals': 6,
        'b_decimals': 18,
        'amount': 1_000_000_000,
        'sender': '0x8cE9Edd9FeE8bEbbF33d059602Fbd487fdEB3661', # any valid EVM address
        'feed_a': '0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7', # USDC/USD Replace with the actual address of Chainlink data feed for token A
        'feed_b': '0xAB594600376Ec9fD91F8e885dADF0CE036862dE0' # MATIC/USD Replace with the actual address of Chainlink data feed for token B
    },
    {
        'pair': 'USDC / WETH',
        'rpc_url':'https://polygon.drpc.org', # Polygon
        'contract': '0x0A6A1Beb7b0b3545578818f45f4e6219615d25aD', # Polygon
        'function': '0x3087bfd8', # Function signature
        'pool_id': '0x0297e37f1873d2dab4487aa67cd56b58e2f27875000100000000000000000002',
        'kind': '0x00',
        'token_a':'0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', # USDC
        'token_b': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619', # WETH
        'a_decimals': 6,
        'b_decimals': 18,
        'amount': 1_000_000_000,
        'sender': '0x8cE9Edd9FeE8bEbbF33d059602Fbd487fdEB3661', # any valid EVM address
        'feed_a': '0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7', # USDC/USD Replace with the actual address of Chainlink data feed for token A
        'feed_b': '0xF9680D99D6C9589e2a93a78A04A279e509205945' # WETH
    },
]



main(tests)