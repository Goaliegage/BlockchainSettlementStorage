import json
import sys
import os

from web3 import Web3
from web3.contract import ConciseContract
import time
import random
import Constants
from web3.middleware import construct_sign_and_send_raw_middleware
from web3 import exceptions
from eth_account import Account


class SettlementStorageContract:
    address = None
    contract = None
    output_file = None
    abi = None
    bytecode = None
    web3 = None
    constructor = None
    environment = None
    filter = None
    wallet = None

    def load(self, web3, output_file, wallet):
        self.abi = Constants.settlement_storage_interface['abi']
        self.bytecode = Constants.settlement_storage_interface['bin']
        self.wallet = wallet
        self.output_file = output_file
        self.web3 = web3
        self.contract = self.web3.eth.contract(abi=self.abi, address=self.wallet.initial_contract_address)
        # print(f'Contract: {self.contract}')
        # self.filter = self.contract.events.StorageInitialized.createFilter(fromBlock="latest")

    def start(self, web3, output_file, environment, wallet):
        self.abi = Constants.settlement_storage_interface['abi']
        self.bytecode = Constants.settlement_storage_interface['bin']
        self.wallet = wallet
        self.output_file = output_file
        self.web3 = web3
        self.environment = environment
        self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        self.filter = self.contract.events.StorageInitialized.createFilter(fromBlock="latest")
        self.constructor = self.contract.constructor()
        if self.environment == 'local':
            # self.create()
            pass
        elif self.environment == 'infura':
            # self.create_infura()
            pass

    def runConstructor(self):
        print(f'Account Balance: {self.web3.eth.getBalance(self.wallet.account.address)}')
        next_nonce = self.web3.eth.get_transaction_count(self.wallet.account.address)
        start = time.time()
        try:
            txn_hash = self.contract.constructor().transact()
            receipt = self.web3.eth.waitForTransactionReceipt(txn_hash, timeout=300)
        except (exceptions.TimeExhausted, exceptions.InvalidTransaction, exceptions.InvalidAddress, exceptions.ValidationError) as error:
            print(f'Error: {error}')
            return '0x0000000000000000000000000000000000000000'
        end = time.time()
        t = end - start
        print(f'Time: {t} seconds')
        print(f'Contract Address: {receipt.contractAddress}')
        return receipt.contractAddress

    def runGetMerchantIndexAddress(self):
        next_nonce = self.web3.eth.get_transaction_count(self.wallet.account.address)
        start = time.time()
        try:
            address = self.contract.functions.getMerchantIndexAddress().call()
        except (exceptions.TimeExhausted, exceptions.InvalidTransaction, exceptions.InvalidAddress, exceptions.ValidationError) as error:
            print(f'Error: {error}')
            return '0x0000000000000000000000000000000000000000'
        end = time.time()
        t = end - start
        print(f'Time: {t} seconds')
        print(f'Address: {address}')
        return address

    def create_infura(self):
        acct = Account.privateKeyToAccount('505d0d5a94520013b278f5795c4e6d3ebccbae356269ecd6221d06c370e52c8a')
        self.web3.eth.default_account = acct.address
        self.web3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
        print(f'Default: {acct.address}')
        account1 = '0xFF9e3FbB25482b1AF76B1bd1E07352e13dBCf8ac'
        account2 = '0xC53f9d42206bD7c9e50B78d937Dd13956CD37050'
        print(f'Account2: {account2}')
        print(f"Account Balance: {self.web3.eth.getBalance(account1)}")
        next_nonce = self.web3.eth.get_transaction_count(account1)
        # gas * price + value
        print(f'Latest Block Number: {self.web3.eth.blockNumber}')
        print(f'Gas Price1: {5000000 * self.web3.toWei(250, "gwei") + 22}')
        print(f'Gas Price2: {self.web3.eth.gasPrice}')

        # txn = self.constructor.buildTransaction({'gas': 5000000,
        #                                          'maxFeePerGas': self.web3.toWei(250, 'gwei'),
        #                                          'maxPriorityFeePerGas': self.web3.toWei(20, 'gwei'),
        #                                          'from': acct.address,
        #                                          'nonce': next_nonce})
        # print(f'Gas Estimate: {self.web3.eth.generate_gas_price(txn)}')
        # print(f'Gas Estimate: {self.web3.eth.estimate_gas(txn)}')
        # print(f'Txn: {txn}')
        # txn.pop('gasPrice', None)
        # TODO: Add encrypted private key to be read in and decrypted
        # encrypted_key = open(location).read()
        # private_key = self.web3.eth.account.decrypt(encrypted_key, '')
        # signed_txn = self.web3.eth.account.sign_transaction(txn, private_key2)
        start = time.time()
        try:
            txn_hash = self.contract.constructor().transact()
            receipt = self.web3.eth.waitForTransactionReceipt(txn_hash, timeout=300)
            logs = self.filter.get_new_entries()
            pass
        except (exceptions.TimeExhausted, exceptions.InvalidTransaction, exceptions.ValidationError, exceptions.SolidityError, exceptions.BlockNumberOutofRange, exceptions.CannotHandleRequest, exceptions.ManifestValidationError) as error:
            print(f'Error: {error}')
            return '0x0000000000000000000000000000000000000000'
        print(f'Hash: {self.web3.toHex(txn_hash)}')
        print(f'Logs: {logs}')
        end = time.time()
        t = end - start
        print(f'Time: {t} seconds')
        print(receipt)
        log = self.contract.events.StorageInitialized().processReceipt(receipt)
        print(f'Log: {log}')
        self.writeOutput(index=0, total_time=t, gas_used=receipt['gasUsed'],
                         function_name='Constructor', address=self.address)
        # return log[0]["args"]["_merchant_indexes"]
        return '0x0000000000000000000000000000000000000000'

    def create(self):
        # self.abi = Constants.settlement_storage_abi
        # self.bytecode = Constants.settlement_storage_bytecode
        # self.abi = Constants.settlement_storage_interface['abi']
        # self.bytecode = Constants.settlement_storage_interface['bin']
        # self.output_file = output_file
        # self.web3 = web3
        # self.contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        # print(f'Functions{self.contract.all_functions()}')
        start = time.time()
        tx_hash = self.constructor.transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        self.address = tx_receipt.contractAddress
        log = self.contract.events.StorageInitialized().processReceipt(tx_receipt)
        print(f'Receipt: {tx_receipt}')
        print(f'Log: {log}')
        # print(f'Event: _merchant_indexes: {log[0]["args"]["_merchant_indexes"]}')
        self.writeOutput(index=0, total_time=t, gas_used=tx_receipt['gasUsed'],
                         function_name='Constructor', address=self.address)
        return log[0]["args"]["_merchant_indexes"]

    # def sign_transaction(self, txn):
    #     print(f'Accounts: {self.web3.eth.get_accounts()}')
    #     next_nonce = self.web3.eth.get_transaction_count('0xCf0158DA2bebcf568d4990bc5a4D0729F6Ecb6e8')
    #     # print(f'txn: {txn}')
    #     # Sign Transaction
    #     # TODO: Add encrypted private key to be read in and decrypted
    #     # encrypted_key = open(location).read()
    #     # private_key = self.web3.eth.account.decrypt(encrypted_key, '')
    #     private_key = '5ba10a7fd0817f52aea7d584f24410b0691dadfcd3bb470f305b92f1cb42cbc2'
    #     signable_transaction = txn
    #     signable_transaction.update({'gas': 1000, 'nonce': next_nonce, 'maxFeePerGas': 3000000000, 'maxPriorityFeePerGas': 2000000000})
    #     # signable_transaction = dict(txn, maxFeePerGas=3000000000, maxPriorityFeePerGas=2000000000, gas=100000, nonce=next_nonce)
    #     signature_info = self.web3.eth.account.sign_transaction(signable_transaction, private_key)
    #     # print(f'Signature_info.raw: {signature_info.rawTransaction}')
    #     # print(f'Signature_info: {signature_info}')
    #     txn_hash = self.web3.eth.send_raw_transaction(signature_info.rawTransaction)
    #     receipt = self.web3.eth.waitForTransactionReceipt(txn_hash)
    #
    #     return receipt

    def writeOutput(self, index='', total_time='', gas_used='', contract_name='SettlementStorage', function_name='', parameter1='', parameter2='', parameter3='', parameter4='', address=''):
        Constants.format_output(index=str(index), total_time=str(total_time), gas_used=str(gas_used), contract_name=contract_name, function_name=function_name, parameter1=str(parameter1), parameter2=str(parameter2), parameter3=str(parameter3), parameter4=str(parameter4), address=str(address))
        self.output_file.addGeneralRow(index=index, total_time=total_time, gas_used=gas_used, contract_name=contract_name, function_name=function_name, parameter1=parameter1, parameter2=parameter2, parameter3=parameter3, parameter4=parameter4, address=address)


def create_initial_contract(web3):
    Settlement_storage_contract = web3.eth.contract(abi=Constants.settlement_storage_abi,
                                                    bytecode=Constants.settlement_storage_bytecode)
    start = time.time()
    tx_hash = Settlement_storage_contract.constructor().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    end = time.time()
    t = end - start
    Constants.format_output(['Index', 'Time', 'Gas Used', 'Contract', 'Function'], [6, 20, 20, 20, 30])
    Constants.format_output([str(0), str(t), str(tx_receipt['gasUsed']), 'SettlementStorage', 'Constructor'],
                            [6, 20, 20, 20, 20])
    contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=Constants.settlement_storage_abi)

    return contract


def start_merchant_index(web3, contract):
    Settlement_contract = contract
    start = time.time()
    tx_hash = Settlement_contract.startMerchantIndexStorage().transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    end = time.time()
    t = end - start
    # Constants.format_output(['Index', 'Time', 'Gas Used', 'Contract', 'Function'], [6, 20, 20, 20, 30])
    Constants.format_output(
        [str(0), str(t), str(tx_receipt['gasUsed']), 'SettlementStorage', 'startMerchantIndexStorage'],
        [6, 20, 20, 20, 20])
