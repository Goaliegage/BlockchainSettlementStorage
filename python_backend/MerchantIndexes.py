import json
import sys
import os

from web3 import Web3
from web3.logs import IGNORE, DISCARD, WARN
import time
import random
import Constants


class MerchantIndex:
    address = None
    contract = None
    output_file = None
    abi = None
    bytecode = None
    web3 = None

    def find(self, web3, output_file, address):
        self.abi = Constants.merchant_indexes_interface['abi']
        self.address = web3.toChecksumAddress(address)
        self.output_file = output_file
        self.web3 = web3
        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)
        # print(f'Functions{self.contract.all_functions()}')

    def addNewMerchant(self, name):
        start = time.time()
        tx_hash = self.contract.functions.addNewMerchant(name).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        # self.address = tx_receipt.contractAddress
        log = self.contract.events.MerchantAdded().processReceipt(tx_receipt)
        # print(f'Event: _merchant_address: {log[0]["args"]["_merchant_address"]}')
        self.writeOutput(index=0, total_time=t, gas_used=tx_receipt['gasUsed'],
                         function_name='addNewMerchant', parameter1=name, address=self.address)
        print(log)
        return log[0]['args']["_merchant_address"]

    def getMerchantAddress(self, name):
        start = time.time()
        output = self.contract.functions.getMerchantAddress(name).call()
        # tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        print(output)
        return output
        #self.writeOutput(index=0, total_time=t, gas_used=tx_receipt['gasUsed'],
        #                 function_name='getMerchantAddress', parameter1=name, address=self.address)

        pass

    def writeOutput(self, index='', total_time='', gas_used='', contract_name='MerchantIndexes', function_name='',
                    parameter1='', parameter2='', parameter3='', parameter4='', address=''):
        Constants.format_output(index=str(index), total_time=str(total_time), gas_used=str(gas_used),
                                contract_name=contract_name, function_name=function_name, parameter1=str(parameter1), parameter2=str(parameter2),
                                parameter3=str(parameter3), parameter4=str(parameter4), address=str(address))
        self.output_file.addGeneralRow(index=index, total_time=total_time, gas_used=gas_used,
                                       contract_name=contract_name, function_name=function_name, parameter1=parameter1,
                                       parameter2=parameter2, parameter3=parameter3, parameter4=parameter4,
                                       address=address)

