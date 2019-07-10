import time
from web3 import Web3
import provider_benchmark
import config

def logTest(web3, company):
    repetitionInconsitency = 0
    methodInconsitency = 0
    getLogByHashFailure = 0
    getLogByFromToFailure = 0
    latestBlockFailure = 0
    logsDic = {}
    
    for i in range(config.ITERATIONS):
        latestBlock = web3.eth.getBlock('latest')
        if latestBlock is None:
            latestBlockFailure += 1
            if config.VERBOSE: print (company, "couldn't get latest block")
        else:
            latestBlockHash = latestBlock.hash.hex()
            try:
                logByHash = web3.eth.getLogs({'blockHash': latestBlockHash})
            except Exception as e:
                if config.VERBOSE: print (company, "gave the following error when trying to find logs for the latest block", latestBlock.number, "by blockHash:", e)
                getLogByHashFailure += 1
                time.sleep(config.DELAY)
                continue
            try:
                logByFromTo = web3.eth.getLogs({'fromBlock': latestBlock.number, 'toBlock': latestBlock.number})
            except Exception as e:
                if config.VERBOSE: print (company, "gave the following error when trying to find logs for the latest block", latestBlock.number, "by fromBlock and toBlock:", e)
                getLogByFromToFailure += 1
                time.sleep(config.DELAY)
                continue

            if logByHash != logByFromTo:
                repetitionInconsitency += 1
                if config.VERBOSE: print (company, "gave inconsistent logs for the latest block when queried by blockHash vs fromBlock and toBlock")
                time.sleep(config.DELAY)
                continue
            
            if latestBlockHash in logsDic:
                if logsDic[latestBlockHash] != logByHash:
                    methodInconsitency += 1
                    if config.VERBOSE: print (company, "gave a different log than previously reported for block", latestBlock)
                    time.sleep(config.DELAY)
                    continue
            else:
                logsDic[latestBlockHash] = logByHash
            
            if config.VERBOSE: print (company, "successfully found a log with", len(logByHash), "events for the latest block", latestBlock.number)
        time.sleep(config.DELAY)
    
    print (company, "returned a different log for the same latest block:", methodInconsitency/config.ITERATIONS * 100, "%")
    print (company, "returned a different log based on querying by blockHash vs fromBlock and toBlock:", repetitionInconsitency/config.ITERATIONS * 100, "%")
    print (company, "failed to return the latest block:", latestBlockFailure/config.ITERATIONS * 100, "%")
    print (company, "failed to getLogs on the latest block queried by blockHash:", getLogByHashFailure/config.ITERATIONS * 100, "%")
    print (company, "failed to getLogs on the latest block queried by fromBlock and toBlock:", getLogByFromToFailure/config.ITERATIONS * 100, "%")
