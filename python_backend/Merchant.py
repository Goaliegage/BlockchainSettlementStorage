import json
import sys
import os
from web3 import Web3
import time
import random
import Constants


class MerchantContract:
    address = None
    contract = None
    output_file = None
    abi = None
    bytecode = None
    web3 = None

    def __init__(self):
        pass

    def find(self, web3='', output_file='', address=''):
        self.address = address
        self.web3 = web3
        self.output_file = output_file
        self.abi = Constants.merchant_interface['abi']
        self.contract = self.web3.eth.contract(address=address, abi=self.abi)

    def start_new_settlement(self, timestamp):
        start = time.time()
        tx_hash = self.contract.functions.start_new_settlement(timestamp).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        log = self.contract.events.new_settlement_created().processReceipt(tx_receipt)
        print(f'Event: _settlement_address: {log[0]["args"]["_settlement"]}')
        return log[0]["args"]["_settlement"]

    def get_current_settlement(self):
        start = time.time()
        output = self.contract.functions.current_settlement().call()
        end = time.time()
        pass

    def view_settlements(self):
        pass

    def writeOutput(self, index='', total_time='', gas_used='', contract_name='Merchant', function_name='',
                    parameter1='', parameter2='', parameter3='', parameter4='', address=''):
        Constants.format_output(index=str(index), total_time=str(total_time), gas_used=str(gas_used),
                                contract_name=contract_name, function_name=function_name, parameter1=str(parameter1), parameter2=str(parameter2),
                                parameter3=str(parameter3), parameter4=str(parameter4), address=str(address))
        self.output_file.addGeneralRow(index=index, total_time=total_time, gas_used=gas_used,
                                       contract_name=contract_name, function_name=function_name, parameter1=parameter1,
                                       parameter2=parameter2, parameter3=parameter3, parameter4=parameter4,
                                       address=address)


def create_initial_merchant_contract(web3, filename):
    Merchant_Contract = web3.eth.contract(abi=Constants.merchant_abi, bytecode=Constants.merchant_bytecode)
    start = time.time()
    merchant_identifier = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    tx_hash = Merchant_Contract.constructor(web3.eth.accounts[0], merchant_identifier, web3.eth.accounts[0]).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    end = time.time()
    t = end - start
    Constants.format_output(['Index', 'Time', 'Gas Used', 'Contract', 'Function'], [6, 20, 20, 20, 20])
    contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=Constants.merchant_abi)
    Constants.format_output([str(0), str(t), str(tx_receipt['gasUsed']), 'Merchant', 'Constructor'], [6, 20, 20, 20, 20])


def contract_object(web3, add, ab):
    return web3.eth.contract(address=add, abi=ab)


def start_new_settlement(web3, filename, contract):
    contract(web3, 0x853Ee1d1075380A0Ee5c4e90f70C86fa65407b84, Constants.merchant_abi)
    start = time.time()
    tx_hash = contract.functions.start_new_settlement()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    end = time.time()
    t = end - start
