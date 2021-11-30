import os
import json
from web3 import Web3


class Wallet:
    options = ''
    account = ''
    account_address = ''
    private_key = ''
    url = ''
    environment = ''
    initial_contract_address = ''
    local_account_address = ''
    testnet_account_address = ''
    mainnet_account_address = ''
    local_private_key = ''
    testnet_private_key = ''
    mainnet_private_key = ''
    output_location = ''
    local_url = ''
    testnet_url = ''
    mainnet_url = ''
    local_initial_contract_address = ''
    testnet_initial_contract_address = ''
    mainnet_initial_contract_address = ''

    # environment must be one of {'local', 'testnet', 'mainnet'}
    def __init__(self, environment):
        self.load_configs()
        self.environment = environment
        with open('configs.txt') as c:
            data = c.read()
            self.options = json.loads(data)
            # print(f'Options: {self.options}')
            self.account_address = self.options[f'{environment}_account']
            self.private_key = self.options[f'{environment}_private_key']
            self.url = self.options[f'{environment}_url']
            self.initial_contract_address = self.options[f'{environment}_initial_contract_address']

            # if environment == 'local':
            #     self.account_address = self.options[f'{environment}_account']
            #     self.private_key = self.options[f'{environment}_private_key']
            #     self.url = self.options[f'{environment}_url']
            #     self.initial_contract_address = self.options[f'{environment}_initial_contract_address']
            #     pass
            # elif environment == 'testnet':
            #     self.account_address =
            #     self.private_key =
            #     self.url =
            #     self.initial_contract_address =
            # elif environment == 'mainnet':
            #     self.account_address =
            #     self.private_key =
            #     self.url =
            #     self.initial_contract_address =
            # pass

        # Local
        self.setLocalAccountAddress()
        self.setLocalPrivateKey()
        self.setLocalInitialContractAddress()
        self.setLocalURL()
        # Testnet
        self.setTestnetAccountAddress()
        self.setTestnetPrivateKey()
        self.setTestnetInitialContractAddress()
        self.setTestnetURL()
        # Mainnet
        self.setMainnetAccountAddress()
        self.setMainnetPrivateKey()
        self.setMainnetInitialContractAddress()
        self.setMainnetURL()

    def setLocalAccountAddress(self):
        self.local_account = self.options['local_account']

    def setTestnetAccountAddress(self):
        self.testnet_account = self.options['testnet_account']

    def setMainnetAccountAddress(self):
        self.mainnet_account = self.options['mainnet_account']

    def setOutputLocation(self, location):
        self.output_location = location

    def setLocalPrivateKey(self):
        self.local_private_key = self.options['local_private_key']

    def setTestnetPrivateKey(self):
        self.testnet_private_key = self.options['testnet_private_key']

    def setMainnetPrivateKey(self):
        self.mainnet_private_key = self.options['mainnet_private_key']

    def setLocalURL(self):
        self.local_url = self.options['local_url']

    def setTestnetURL(self):
        self.testnet_url = self.options['testnet_url']

    def setMainnetURL(self):
        self.mainnet_url = self.options['mainnet_url']

    def setLocalInitialContractAddress(self):
        self.local_initial_contract_address = self.options['local_initial_contract_address']

    def setTestnetInitialContractAddress(self):
        self.testnet_initial_contract_address = self.options['testnet_initial_contract_address']

    def setMainnetInitialContractAddress(self):
        self.mainnet_initial_contract_address = self.options['mainnet_initial_contract_address']

    def load_configs(self):
        with open('configs.txt') as c:
            data = c.read()
            self.options = json.loads(data)
            print(f'Options: {self.options}')

    def saveInitialContractAddress(self, address):
        self.options[f'{self.environment}_initial_contract_address'] = address
        # if self.environment == 'local':
        #     self.options[f'{self.environment}_initial_contract_address'] = address
        # elif self.environment == 'testnet':
        #     self.options.update({'testnet_initial_contract_address', address})
        # elif self.environment == 'mainnet':
        #     self.options.update({'mainnet_initial_contract_address', address})
        with open('configs.txt', 'w') as c:
            c.write(json.dumps(self.options))

    def saveLocalInitialContractAddress(self, address):
        with open('configs.txt', 'w') as c:
            self.options
            pass

    def saveTestnetInitialContractAddress(self, address):
        with open('configs.txt', 'w') as c:
            pass

    def saveMainnetInitialContractAddress(self, address):
        with open('configs.txt', 'w') as c:
            pass