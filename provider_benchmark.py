from multiprocessing import Process
from web3 import Web3
import argparse
import log_consistency
import pending_transactions
import sys
import config


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='infura_api_key',
                        help='test Infura with your unique API key')
    parser.add_argument('-a', action='store', dest='alchemy_api_key',
                        help="test Alchemy with your unique API key")
    parser.add_argument('-c', '--cloudflare',
                        action='store_true', help="test Cloudflare")
    parser.add_argument('-n', action='store', dest='node_http_instance',
                        help="test a specific node with an http instance")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="display progess of tests")
    net = parser.add_mutually_exclusive_group(required=True)
    net.add_argument('-mainnet', action='store_true', help="test on Mainnet")
    net.add_argument('-ropsten', action='store_true', help="test on Ropsten")
    connection = parser.add_mutually_exclusive_group(required=True)
    connection.add_argument(
        '-websocket', action='store_true', help="test websocket")
    connection.add_argument('-http', action='store_true', help="test http")
    test = parser.add_mutually_exclusive_group(required=True)
    test.add_argument('-1', '--log_consistency',
                      action='store_true', help="run test for log consistency")
    test.add_argument('-2', '--pending_transactions',
                      action='store_true', help="run test for pending transactions")
    return parser.parse_args()


def runTests(web3, company, tests):
    for test in tests:
        test(web3, company)


def alchemy(tests, args):
    if args.websocket:
        if args.mainnet:
            web3 = Web3(Web3.WebsocketProvider(
                "wss://eth-mainnet.g.alchemy.com/v2/" + args.alchemy_api_key))
        else:
            web3 = Web3(Web3.WebsocketProvider(
                "wss://eth-mainnet.g.alchemy.com/v2/" + args.alchemy_api_key))
    else:
        if args.mainnet:
            web3 = Web3(Web3.HTTPProvider(
                "https://eth-sepolia.g.alchemy.com/v2/" + args.alchemy_api_key))
        else:
            web3 = Web3(Web3.HTTPProvider(
                "https://eth-sepolia.g.alchemy.com/v2/" + args.alchemy_api_key))
    runTests(web3, "Alchemy", tests)


def infura(tests, args):
    if args.websocket:
        if args.mainnet:
            web3 = Web3(Web3.WebsocketProvider(
                "wss://mainnet.infura.io/ws/v3/" + args.infura_api_key))
        else:
            web3 = Web3(Web3.WebsocketProvider(
                "wss://sepolia.infura.io/ws/v3/" + args.infura_api_key))
    else:
        if args.mainnet:
            web3 = Web3(Web3.HTTPProvider(
                "https://mainnet.infura.io/v3/" + args.infura_api_key))
        else:
            web3 = Web3(Web3.HTTPProvider(
                "https://sepolia.infura.io/v3/" + args.infura_api_key))
    runTests(web3, "Infura", tests)


def cloudflare(tests, args):
    if args.mainnet and args.http:
        web3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com"))
        runTests(web3, "Cloudflare", tests)


def node(tests, args):
    if not args.websocket:
        web3 = Web3(Web3.HTTPProvider(args.node_http_instance))
        runTests(web3, "ETH Node", tests)


if __name__ == '__main__':
    args = parseArgs()

    config.VERBOSE = args.verbose

    if args.infura_api_key is None and args.alchemy_api_key is None and not args.cloudflare and args.node_http_instance is None:
        print(
            "provider_benchmark.py: error: must specify companies to test, use -h for help")
        sys.exit()

    tests = []
    if args.log_consistency:
        tests.append(log_consistency.logTest)
    if args.pending_transactions:
        tests.append(pending_transactions.transactionsTest)

    threads = []
    if args.infura_api_key:
        threads.append(Process(target=infura, args=(tests, args)))
    if args.alchemy_api_key:
        threads.append(Process(target=alchemy, args=(tests, args)))
    if args.cloudflare:
        threads.append(Process(target=cloudflare, args=(tests, args)))
    if args.node_http_instance:
        threads.append(Process(target=node, args=(tests, args)))

    for t in threads:
        t.start()
    for t in threads:
        t.join()
