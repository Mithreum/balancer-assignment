import requests
import json

def encode_data(contract_address, pool_id, kind, token_a, token_b, amount, sender, data_feed_a, data_feed_b):
    '''Converts the input params to an Ethereum API request body'''
    return {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": '0xdba9f93c'
                + pool_id[2:] 
                + format(int(kind, 16), '064x')
                + token_a[2:].rjust(64, '0')
                + token_b[2:].rjust(64, '0')
                + format(amount, '064x')
                + sender[2:].rjust(64, '0')
                + data_feed_a[2:].rjust(64, '0')
                + data_feed_b[2:].rjust(64, '0')
            },
            "latest"],
        "id": 1
    }

def get_slippage(url, data) -> tuple:
    '''Querries the contract & parses its output'''

    try:
        # 1. Execute the request
        response = requests.post(url, json=data)

        # 2. Parse the response
        result_hex = json.loads(response.text)['result']

        # print('result_hex', result_hex)

        # 3. Parse the hexadecimal string into respective components
        step = 64 # 32 bytes * 2 chars representation
        start = 2 # 0x prefix
        stop = start + step

        swapAmount = contract_slippage = int(result_hex[start:stop], 16)

        return swapAmount
    
    except:
        print('Check the RPC URL, pool_id, contract or feed addresses')

def main(test):
    try:
        request_data = encode_data(test['contract'], test['pool_id'], test['kind'], test['token_a'], test['token_b'], test['amount'], test['sender'], test['feed_a'], test['feed_b'])

        print('request_data', request_data)

        swapAmount = get_slippage(test['rpc_url'], request_data)

        print("swapAmount:", swapAmount)
    except Exception as e:
            print('An error occured', e)

main({
     'pair': 'USDC / WMATIC',
        'rpc_url':'https://polygon.drpc.org', # Polygon
        'contract': '0x0A6A1Beb7b0b3545578818f45f4e6219615d25aD', # Polygon
        # 'function': '0x3087bfd8', # Function signature
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
})