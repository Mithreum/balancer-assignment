import requests
import json

def encode_data(contract_address, function_signature, pool_id, kind, token_a, token_b, amount, sender, data_feed_a, data_feed_b):
    '''Converts the input params to an Ethereum API request body'''
    return {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [
            {
                "to": contract_address,
                "data": function_signature 
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


def get_slippage(url, data, token_a_decimals, token_b_decimals) -> tuple:
    '''Querries the contract & parses its output'''

    try:

        # 1. Execute the request
        response = requests.post(url, json=data)

        # 2. Parse the response
        result_hex = json.loads(response.text)['result']

        print('result_hex', result_hex)

        # 3. Parse the hexadecimal string into respective components
        token_a_price = int(result_hex[2:66], 16)
        token_b_price = int(result_hex[66:130], 16)
        # contract_slippage = int(result_hex[130:194], 16) # Ignore
        token_a_price_decimals = int(result_hex[194:258], 16)
        token_b_price_decimals = int(result_hex[258:], 16)

        print('token_a_price', token_a_price, 'token_b_price', token_b_price, token_a_price_decimals, token_b_price_decimals)

        expected = token_a_price / 10 ** (token_a_price_decimals + token_a_decimals)
        actual = token_b_price / 10 ** (token_b_price_decimals + token_b_decimals)
        slippage = expected - actual
        slip_percent = slippage / expected * 100

        return expected, actual, slippage, slip_percent

    except:
        print('Check the RPC URL, pool_id, contract or feed addresses')
        return 'error', 'error', 'error', 'error'
    
def main(tests):

    for test in tests:

        try:

            # 1. Prepare the data
            request_data = encode_data(test['contract'], test['function'], test['pool_id'], test['kind'], test['token_a'], test['token_b'], test['amount'], test['sender'], test['feed_a'], test['feed_b'])

            # 2. 
            [expected, actual, slippage, slip_percent] = get_slippage(test['rpc_url'], request_data, test['a_decimals'], test['b_decimals'])

            # 3. Output the result (NB. divide each token by 10 ** decimals)
            print(f"{test['pair']}\n Expected($):\t", expected, '\n', "Actual  ($):\t", actual, '\n', "Slippage($):\t", slippage, '\n', f"Slippage(%): \t{" {:.2f}%".format(slip_percent)}")

        except Exception as e:
            print('An error occured', e)