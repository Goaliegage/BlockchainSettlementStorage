# Project Automation & Testing
import argparse
import time
import datetime
import os
import json

import dateutil

import Merchant
import Constants
import random
import Settlement
import SettlementStorage
import WriteToExcel
import MerchantIndexes
import Wallet_Manager
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account

WEB3_INFURA_PROJECT_ID = '73a11e7c9fbf4adbbf29f828479b76bc'
WEB3_INFURA_API_SECRET = '975ad6a41f18410ca79bbf1d6e190e2a'


class Driver:
    web3 = None
    environment = None
    runs_merchant = None
    runs_settlement = None
    runs_transaction = None
    wallet = None
    excel_output = None

    def __init__(self, wallet):
        self.wallet = wallet
        self.environment = self.wallet.environment
        self.wallet.account = Account.privateKeyToAccount(self.wallet.private_key)
        self.wallet.setOutputLocation(
            f'{self.environment}_log_output_{time.strftime("%m_%d_%Y_%M", time.localtime())}.txt')
        initiate_contracts()
        self.web3 = start_connection(self.wallet.url, self.environment)
        self.web3.eth.default_account = self.wallet.account.address
        self.web3.middleware_onion.add(construct_sign_and_send_raw_middleware(self.wallet.account))
        print_contract_methods(self.web3)
        self.excel_output = WriteToExcel.OutputFile(self.environment)

    def run_tests(self, r_merchant=0, r_settlement=0, r_transaction=0):
        self.runs_merchant = r_merchant
        self.runs_settlement = r_settlement
        self.runs_transaction = r_transaction
        self.create_test_contracts()
        pass

    def create_test_contracts(self):
        self.create_settlement_storage()
        index = self.loadMerchantIndexes()
        self.createTestMerchants(index)

    def check_test_contracts(self):
        pass

    def create_settlement_storage(self):
        s_storage = SettlementStorage.SettlementStorageContract()
        s_storage.start(self.web3, self.excel_output, self.environment, self.wallet)
        self.wallet.initial_contract_address = s_storage.runConstructor()
        self.wallet.saveInitialContractAddress(self.wallet.initial_contract_address)

    def loadMerchantIndexes(self):
        s_storage = SettlementStorage.SettlementStorageContract()
        s_storage.load(self.web3, self.excel_output, self.wallet)
        address = s_storage.runGetMerchantIndexAddress()
        m_index = MerchantIndexes.MerchantIndex()
        m_index.find(self.web3, self.excel_output, address)
        return m_index

    def createTestMerchants(self, m_index):
        merchant_contracts = []
        print(f'Creating Test Merchants...')
        for x in range(self.runs):
            address = self.addMerchantToIndex(m_index, f'Test Merchant {str(x)}')
            merchant_contract = self.loadMerchantContract(address)
            merchant_contracts.append(merchant_contract)
            print(f'Merchant: \'Test Merchant {x}\' created')
            self.createTestSettlements(merchant_contract)
        return merchant_contracts

    def createTestSettlements(self, merchant_contract):
        settlements = []
        print(f'Creating Test Settlements...')
        for x in range(self.runs):
            # date = f'11/{1 + x}/2021'
            timestamp = dateutil.parser.parse(f'11/{1 + x}/2021', dayfirst=True).timestamp()
            s_address = self.addSettlementToMerchant(merchant_contract, timestamp)
            s_contract = Settlement.SettlementContract()
            s_contract.load(self.web3, self.excel_output, s_address)
            settlements.append(s_contract)
            print(f'Settlement {x} created')
            self.createTestTransactions(s_contract)

    def createTestTransactions(self, settlement_contract):
        transactions = []
        print(f'Creating Test Transactions...')
        random.seed()
        for x in range(self.runs):
            transaction = {'t_type': random.randint(0, 1),
                           't_amount': random.randrange(1, 100000000),
                           't_time': random.randrange(1, 100000),
                           't_digits': random.randint(1000, 9999)}
            transactions.append(transaction)
            if transaction['t_type'] == 0:
                settlement_contract.add_sale_transaction(transaction['t_time'], transaction['t_amount'],
                                                         transaction['t_digits'], index=x)
            elif transaction['t_type'] == 1:
                settlement_contract.add_return_transaction(transaction['t_time'], transaction['t_amount'],
                                                           transaction['t_digits'], index=x)
        settlement_contract.settleTransactions(s_time=time.time())

    def addSettlementToMerchant(self, merchant_contract, time):
        return merchant_contract.start_new_settlement(int(time))

    def addSaleTransactionToSettlement(self, settlement_contract, time, amount, digits, index=''):
        settlement_contract.add_sale_transaction(time, amount, digits, index=index)

    def addReturnTransactionToSettlement(self, settlement_contract, time, amount, digits, index=''):
        settlement_contract.add_return_transaction(time, amount, digits, index=index)

    def addMerchantToIndex(self, m_index, identifier):
        return m_index.addNewMerchant(identifier)

    def loadMerchantContract(self, address):
        merchant_contract = Merchant.MerchantContract()
        merchant_contract.find(self.web3, self.excel_output, address=address)
        return merchant_contract


# class TestDriver:
#     web3 = None
#     environment = None
#     runs = None
#     wallet = None
#
#     def __init__(self, wallet, runs=0):
#         self.environment = 'infura'
#         self.runs = runs
#         self.wallet = wallet
#         initiate_contracts()
#         self.web3 = start_connection(self.wallet.testnet_url)
#         print_contract_methods(self.web3)
#
#     def run_tests(self):
#         pass


# class MainDriver:
#     web3 = None
#     environment = None
#     runs = None
#     wallet = None
#
#     def __init__(self, wallet):
#         self.environment = 'main'
#         self.wallet = wallet
#         initiate_contracts()
#         self.web3 = start_connection(self.wallet.mainnet_url)
#         print_contract_methods(self.web3)
#
#     def run_tests(self):
#         pass
#
#     def create_test_contracts(self):
#         pass
#
#     def check_test_contracts(self):
#         pass


def start_connection(url, environment):
    # Create the ganache connection
    web3 = Web3(Web3.HTTPProvider(url))
    if web3.isConnected():
        print(f'{environment} connection established using {url}')
    else:
        print(f'Error: {environment} connection to {url} not established. Exiting...')
        exit(0)
    # # provide default account from which to run transactions
    # web3.eth.defaultAccount = web3.eth.accounts[1]
    return web3


# def start_testnet_connection():
#     ropsten_url = 'https://ropsten.infura.io/v3/73a11e7c9fbf4adbbf29f828479b76bc'
#     web3 = Web3(Web3.HTTPProvider(ropsten_url))
#     if web3.isConnected():
#         print(f'Connected: {web3.isConnected()}')
#         return web3
#     else:
#         print(f'Connected: False')
#         print(f'Connection Not Established. Exiting...')
#         exit(0)

# Compile the contracts and get abi and bytecode
def initiate_contracts():
    Constants.compile_source_files('Solidity')


# Will print the all current contract methods
def print_contract_methods(web3):
    print(f'Current Contract Methods:')
    print(
        f'SettlementStorage: {web3.eth.contract(abi=Constants.settlement_storage_interface["abi"], bytecode=Constants.settlement_storage_interface["bin"]).all_functions()}')
    print(
        f'MerchantIndexes: {web3.eth.contract(abi=Constants.merchant_indexes_interface["abi"], bytecode=Constants.merchant_indexes_interface["bin"]).all_functions()}')
    print(
        f'Merchant: {web3.eth.contract(abi=Constants.merchant_interface["abi"], bytecode=Constants.merchant_interface["bin"]).all_functions()}')
    print(
        f'Settlement: {web3.eth.contract(abi=Constants.settlement_interface["abi"], bytecode=Constants.settlement_interface["bin"]).all_functions()}')


# def test_settlement(web3):
#     Settlement.create_local_ganache_connection(web3, 10)
#     pass
#
#
# def stress_test_settlement(web3):
#     Settlement.start_stress_test()
#
#
# def test_merchant_creation(web3, file, address, number):
#     # Merchant.create_initial_merchant_contract(web3, Constants.output_filename)
#     print('Creating Merchant Indexes...')
#     merch_index = MerchantIndexes.MerchantIndex()
#     merch_index.find(web3, file, address)
#     merchants = []
#     print('Creating Merchants...')
#     for x in range(number):
#         print(f'Merchant: \'Test Merchant {x}\' created')
#         merchants.append(Merchant.MerchantContract())
#         address = merch_index.addNewMerchant(f'Test Merchant {str(x)}')
#         # address_alt = merch_index.getMerchantAddress(f'Test Merchant{str(x)}')
#         merchants[x].find(web3=web3, output_file=file, address=address)
#     return merchants
#
#
# def test_settlementstorage_creation(web3, file, environment):
#     s_storage = SettlementStorage.SettlementStorageContract()
#     s_storage.start(web3, file, environment)
#     if environment == 'local':
#         return s_storage.create()
#     elif environment == 'infura':
#         return s_storage.create_infura()
#     elif environment == 'production':
#         return None


# prints conversions of common denominations to wei
def printConversions():
    print(f'One Ether = {Web3.toWei(1, "ether")} Wei')
    print(f'One Kwei = {Web3.toWei(1, "kwei")} Wei')
    print(f'One Babbage = {Web3.toWei(1, "babbage")} Wei')
    print(f'One Femtoether = {Web3.toWei(1, "femtoether")} Wei')
    print(f'One Mwei = {Web3.toWei(1, "mwei")} Wei')
    print(f'One Lovelace = {Web3.toWei(1, "lovelace")} Wei')
    print(f'One Picoether = {Web3.toWei(1, "picoether")} Wei')
    print(f'One Gwei = {Web3.toWei(1, "gwei")} Wei')


# create the excel document with the correct environment name and time as the filename
def initiate_output_file(environment=''):
    file = WriteToExcel.OutputFile(environment)
    return file


# def run_tests(web3, out_file, number, environment):
#     # Test flow:
#     # Create SettlementStorage; Returns MerchantIndex address
#     merchant_index_address = test_settlementstorage_creation(web3, out_file, environment)
#     # merchants = test_merchant_creation(web3, out_file, merchant_index_address, number)
#     # print(f'Testing settlements...')
#     # for m in merchants:
#     #     set_address = m.start_new_settlement()
#     #     set_contract = Settlement.SettlementContract()
#     #     set_contract.load(web3, out_file, set_address)
#     #     print(f'Settlement: {m}')
#     #     for x in range(number):
#     #         random.seed()
#     #         t_type = random.randint(0, 1)
#     #         t_amount = random.randrange(1, 100000000)
#     #         t_time = random.randrange(1, 100000)
#     #         t_digits = random.randint(1000, 9999)
#     #         if t_type == 0:
#     #             set_contract.add_sale_transaction(t_time, t_amount, t_digits, index=x)
#     #         elif t_type == 1:
#     #             set_contract.add_return_transaction(t_time, t_amount, t_digits, index=x)
#     #     set_contract.view_transactions()
#     #     set_contract.settleTransactions(s_time=time.time())
#     # find MerchantIndex address from before
#     # add merchants to index
#     # add transactions to merchant;
#     # settle
#     # test overflow
#     #
#     pass


# checks if a config file exists in the current directory; if not creates it with blank options.
def check_for_config_file():
    if not os.path.exists('configs.txt'):
        print(f'\'config.txt\' not found. Generating... ')
        configs = {'local_account': '',
                   'local_private_key': '',
                   'local_url': '',
                   'local_initial_contract_address': '',
                   'testnet_account': '',
                   'testnet_private_key': '',
                   'testnet_url': '',
                   'testnet_initial_contract_address': '',
                   'mainnet_account': '',
                   'mainnet_private_key': '',
                   'mainnet_url': '',
                   'mainnet_initial_contract_address': ''}
        with open('configs.txt', 'w') as c:
            c.write('{')
            for keys, value in configs.items():
                c.write(f'\"{str(keys)}\": \"{str(value)}\",\n')
            c.write('}')
            print(f'Config file generated. Set options and rerun. Exiting...')
            exit(0)
    else:
        return True


# def run_local_tests(number):
#     # initiate_contracts()
#     # web3 = start_local_connection()
#     out_file = initiate_output_file('Ganache')
#     run_tests(web3, out_file, number, 'local')
#     out_file.writeToFile()
#
#
# def run_testnet_tests(number):
#     initiate_contracts()
#     web3 = start_testnet_connection()
#     out_file = initiate_output_file('Ropsten')
#     run_tests(web3, out_file, number, 'infura')
#     out_file.writeToFile()


# Todo: code cleanup; function to pull all settlements from specific merchant and display;
# will autogenerate random contracts with the given # of merchants, settlements per merchant, and transactions per settlement
# Note: This will run at least (runs_merchant*runs_settlement*runs_transactions) number of times on the given chains.
def run_autogenerate(local=False, test=False, main=False, runs_merchant=0, runs_settlement=0, runs_transaction=0):
    check_for_config_file()
    if local:
        out_file = initiate_output_file('local')
        wallet = Wallet_Manager.Wallet('local')
        driver = Driver(wallet)
        driver.run_tests(runs_merchants=runs_merchant, runs_settlements=runs_settlement, runs_transactions=runs_transaction)
        out_file.writeToFile()
    elif test:
        out_file = initiate_output_file('testnet')
        wallet = Wallet_Manager.Wallet('testnet')
        driver = Driver(wallet)
        driver.run_tests(runs_merchants=runs_merchant, runs_settlements=runs_settlement, runs_transactions=runs_transaction)
        out_file.writeToFile()
    elif main:
        out_file = initiate_output_file('mainnet')
        wallet = Wallet_Manager.Wallet('mainnet')
        driver = Driver(wallet)
        driver.run_tests(runs_merchants=runs_merchant, runs_settlements=runs_settlement, runs_transactions=runs_transaction)
        out_file.writeToFile()


# initialize command line arguments;
parser = argparse.ArgumentParser(description='Program to run transactions on the ethereum blockchain. '
                                             'Can be a local chain, a test chain, or the main Ethereum chain.')
parser.add_argument('-l', '--local', action='store_true', help='Run on local chain')
parser.add_argument('-t', '--testnet', action='store_true', help='Run on Ropsten test chain')
parser.add_argument('-m', '--mainnet', action='store_true', help='Run on main Ethereum chain')
parser.add_argument('-a', '--auto_generate', action='store_true', help='Will autogenerate with the specified numbers using '
                                                  '--runs_merchants, --runs_settlements, --runs_transactions')
parser.add_argument('--runs_merchants', action='store', help='Number of merchants to autogenerate per merchant_index.')
parser.add_argument('--runs_settlements', help='Number of settlements to autogenerate per merchant.')
parser.add_argument('--runs_transactions', help='Number of transactions to autogenerate per settlement.')
parser.add_argument('--initialize', action='store_true', help='Use this the first time you are running on a given chain.')
# Todo: change action to append and create a list of merchants and etc to add per run;
parser.add_argument('--addNewMerchant', action='store', help='')
parser.add_argument('--createNewSettlementForMerchant', action='store', help='')
parser.add_argument('--addTransactionToSettlementForMerchant', action='store', help='')
parser.add_argument('--finalizeSettlement', action='store', help='')

# get command line arguments
args = parser.parse_args()

# run with any of local, testnet, or mainnet
if args.auto_generate:
    run_autogenerate(args.local, args.testnet, args.mainnet)

if args.addNewMerchant:

    pass