import json
import sys
import os

from web3 import Web3
import time
import random
import Constants


class SettlementContract:
    address = None
    contract = None
    output_file = None
    abi = None
    bytecode = None
    web3 = None
    settlement_total = 0

    def __init__(self):
        pass

    def load(self, web3, output_file, address):
        self.address = address
        self.output_file = output_file
        self.web3 = web3
        self.abi = Constants.settlement_interface['abi']
        self.contract = web3.eth.contract(address=self.address, abi=self.abi)

    def add_sale_transaction(self, t_time, t_amount, t_digits, index=0):
        start = time.time()
        tx_hash = self.contract.functions.addSaleTransaction(t_time, t_amount, t_digits).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        self.settlement_total += t_amount
        self.writeOutput(index=index, total_time=t, gas_used=tx_receipt['gasUsed'], function_name='addSaleTransaction', parameter1=0, parameter2=t_time, parameter3=t_amount, parameter4=t_digits)

    def add_return_transaction(self, t_time, t_amount, t_digits, index=0):
        start = time.time()
        tx_hash = self.contract.functions.addSaleTransaction(t_time, t_amount, t_digits).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        self.settlement_total -= t_amount
        self.writeOutput(index=index, total_time=t, gas_used=tx_receipt['gasUsed'], function_name='addReturnTransaction', parameter1=1, parameter2=t_time,
                         parameter3=t_amount, parameter4=t_digits)

    def settleTransactions(self, s_time='', payout=settlement_total):
        start = time.time()
        tx_hash = self.contract.functions.settleTransactions(int(s_time), payout).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        end = time.time()
        t = end - start
        self.writeOutput(index=0, total_time=t, gas_used=tx_receipt['gasUsed'],
                         function_name='settleTransactions', parameter1=int(s_time), parameter2=payout)

    def view_transactions(self):
        start = time.time()
        output = self.contract.functions.viewTransactions().call()
        # tx_receipt = self.web3.eth.waitForTransactionReceipt(output)
        end = time.time()
        t = end - start
        self.writeOutput(index=0, total_time=t, gas_used=0, function_name='viewTransactions')
        print(output)

        pass

    def writeOutput(self, index='', total_time='', gas_used='', contract_name='Settlement', function_name='',
                    parameter1='', parameter2='', parameter3='', parameter4='', address=''):
        Constants.format_output(index=str(index), total_time=str(total_time), gas_used=str(gas_used),
                                contract_name=contract_name, function_name=function_name, parameter1=str(parameter1), parameter2=str(parameter2),
                                parameter3=str(parameter3), parameter4=str(parameter4), address=str(address))
        self.output_file.addGeneralRow(index=index, total_time=total_time, gas_used=gas_used,
                                       contract_name=contract_name, function_name=function_name, parameter1=parameter1,
                                       parameter2=parameter2, parameter3=parameter3, parameter4=parameter4,
                                       address=address)


# def get_params(contract):
#     filename = 'Settlement.txt'
#     with open(filename, 'r', encoding='utf-8', newline='') as f:
#         parameters = f.read().split(',')
#         a, b = int(parameters[0]), int(parameters[1])
#         start = time.time()
#         # call the function method of the contract, the call the solidity
#         # function then transact
#         get_params = contract.functions.getparams(a, b).transact()
#         # get the receipt of the transaction
#         get_params_tx_receipt = Web3.eth.waitForTransactionReceipt(get_params)
#         end = time.time()
#         t = end - start
#         # open output file and save time spent and gas used
#         f = open(filename, "a")
#         print(t, '\t', get_params_tx_receipt['gasUsed'])
#
#
# def create_local_ganache_connection(web3, amount):
#     web3.eth.defaultAccount = web3.eth.accounts[0]
#     # create the contract
#     Settlement_Contract = web3.eth.contract(abi=Constants.settlement_abi, bytecode=Constants.settlement_bytecode)
#     start = time.time()
#     tx_hash = Settlement_Contract.constructor(web3.eth.accounts[0], web3.eth.accounts[0]).transact()
#     tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
#     end = time.time()
#     t = end - start
#     f = open(filename, "w")
#     original = sys.stdout
#     sys.stdout = Save(sys.stdout, f)
#     print("Time \t\t\t Gas Used")
#     # heading1, heading2, heading3, heading4, heading5 = 'Index', 'Time', 'Gas Used', 'Type', 'Amount'
#     # print(f'{heading1.rjust(heading1_size)} | {heading2.rjust(heading2_size)} | {heading3.rjust(heading3_size)} | {heading4.rjust(heading4_size)} | {heading5.rjust(heading5_size)}')
#     # print(f'{str("").rjust(heading1_size)} | {str(t).rjust(heading2_size)} | {str(tx_receipt["gasUsed"]).rjust(heading3_size)}')
#
#     contract = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#     start_automation_test(contract, web3)
#     # start_stress_test(contract, web3)
#     # print(f'all done \n*********Check output file in directory: {os.getcwd()}*********')
#     f.close()
#
#
# def add_transaction_test(contract, web3, index):
#     random.seed()
#     t_type = random.randint(0, 1)
#     t_amount = random.randrange(1, 100000000)
#     t_time = random.randrange(1, 100000)
#     t_digits = random.randint(1000, 9999)
#     start = time.time()
#     addTransactionHash = contract.functions.addTransaction(t_type, t_time, t_amount, t_digits).transact()
#     addTransaction_tx_receipt = web3.eth.waitForTransactionReceipt(addTransactionHash)
#     end = time.time()
#     t = end - start
#     f = open(filename, "a")
#     output = [str(index), str(t), str(addTransaction_tx_receipt['gasUsed']), 'Settlement', 'addTransaction', str(t_type), str(t_amount), str(t_time), str(t_digits)]
#     # output_size = [heading1_size, heading2_size, heading3_size, heading4_size, heading5_size, heading6_size, heading7_size, heading8_size, heading9_size]
#     Constants.format_output(output, output_size)
#     # print(index, ':', t, '\t', addTransaction_tx_receipt['gasUsed'], '\t')
#     # print(f'{str(index).rjust(heading1_size)} | {str(t).rjust(heading2_size)} | {str(t_type).rjust(heading3_size)} |')
#
#
# def add_transactions_test(contract, web3, index, count):
#     t_type = []
#     t_amount = []
#     t_time = []
#     t_digits = []
#     random.seed()
#
#     for x in range(count):
#         t_type.append(random.randint(0, 1))
#         t_amount.append(random.randrange(1, 100000000))
#         t_time.append(random.randrange(1, 100000))
#         t_digits.append(random.randint(1000, 9999))
#
#     start = time.time()
#     addTransactionsHash = contract.functions.addTransactions(t_type, t_time, t_amount, t_digits, count).transact()
#     # addTransactionsHash = contract.functions.addTransactions(t_type, t_time, t_amount, t_digits, count).transact()
#     addTransactions_tx_receipt = web3.eth.waitForTransactionReceipt(addTransactionsHash)
#     end = time.time()
#     t = end - start
#     f = open(filename, "a")
#     output = [str(index), str(t), str(addTransactions_tx_receipt['gasUsed']), 'Settlement', 'addTransaction', str(t_type), str(t_amount), str(t_time), str(t_digits)]
#     Constants.format_output(output, output_size)
#
#
# def print_view_transactions(contract):
#     output = contract.functions.viewTransactions().call()
#     print(f'{output}')
#     for index, x in output:
#         print(f'{index}: {x}')
#
#
# def start_automation_test(contract, web3):
#     for index, x in enumerate(range(0, 10000)):
#         add_transaction_test(contract, web3, index)
#     print_view_transactions(contract)
#
#
# def start_stress_test(contract, web3):
#     for index, x in enumerate(range(0, 20)):
#         add_transactions_test(contract, web3, index, 1000)
#     print_view_transactions(contract)
# # create_local_ganache_connection()
