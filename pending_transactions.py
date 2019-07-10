import time
import random
import urllib, json
from web3 import Web3
from multiprocessing import Process
import provider_benchmark
import eth_accountz
import os
import sys
import config


def transactionsTest(web3, company):
    transactionNotFound = 0
    config.LOCK.acquire()
    sys.stdin = os.fdopen(config.STDIN)
    sendAddress = input("Enter an address to send transaction through " + company + " (must be distinct, do not repeat accross tests): ")
    sendPrivateKey = input("Enter the private key for that address: ")
    recieveAddress = input("Enter an address to recieve transaction through " + company + " (must be distinct, do not repeat accross tests): ")
    recievePrivateKey = input("Enter the private key for that address: ")
    config.LOCK.release()
    
    sendAccount = eth_accountz.Account(sendAddress, sendPrivateKey)
    recieveAccount = eth_accountz.Account(recieveAddress, recievePrivateKey)
    nonce = web3.eth.getTransactionCount(sendAccount.address)
    for i in range(config.ITERATIONS):
        signed_txn = web3.eth.account.signTransaction({
                        'to': recieveAccount.address,
                        'gasPrice':web3.eth.gasPrice,
                        'nonce': nonce + i + 1,
                        'gas': 100000,
                    },
                    sendAccount.privateKey) 

        try: 
            txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            receipt = web3.eth.getTransaction(txn)
        except Exception as e:
            if config.VERBOSE: print (company, "gave the following error when sending then getting a transaction:", e)
            time.sleep(config.DELAY)
            continue

        if receipt is None:
            transactionNotFound += 1
        if config.VERBOSE: print (company, "returned the following reciept:", receipt)

        time.sleep(config.DELAY)

    print (company, "failed to find pending transactions:", transactionNotFound/config.ITERATIONS * 100, "%")


