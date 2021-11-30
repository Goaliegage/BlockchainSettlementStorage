# Stores constants for project
import os
import time
import solcx
import Wallet_Manager
import json

# Config Options
configs = None

# Wallet
wallet = None

# Settlement Contract
settlement_interface = None

# Merchant Contract
merchant_interface = None

# Merchant_Indexes Contract
merchant_indexes_interface = None

# SettlementStorage Contract
settlement_storage_id = None
settlement_storage_interface = None

# #########################################################
output_filename = filename = f'ganache_output_{time.strftime("%m_%d_%Y_%M", time.localtime())}.txt'
out_file = None


def format_output(index='', total_time='', gas_used='', contract_name='', function_name='', parameter1='',
                  parameter2='', parameter3='', parameter4='', address=''):
    formatted_string = '|'
    output = [index, total_time, gas_used, contract_name, function_name, parameter1, parameter2, parameter3, parameter4, address]
    output_size = [6, 20, 20, 30, 30, 30, 30, 30, 30, 30]
    for (x, y) in zip(output, output_size):
        formatted_string += f'{x.center(y)} |'
    print(formatted_string)
#
#
# def program_output(output):
#     print(output)


def start_output_file():
    global out_file;
    out_file = open(output_filename, 'w+')


def close_output_file():
    out_file.close()


def compile_source_files(file_path):
    # solcx.install_solc()
    compiled_sol = solcx.compile_files([os.path.join(file_path, 'SettlementStorage.sol'),
                                        os.path.join(file_path, 'MerchantIndexes.sol'),
                                        os.path.join(file_path, 'Merchant.sol'),
                                        os.path.join(file_path, 'Settlement.sol')],
                                       output_values=['abi', 'bin'], solc_version='0.8.6')
    for x in range(4):
        contract_id, contract_interface = compiled_sol.popitem()
        load_abi_bytecode(contract_id, contract_interface)


def load_abi_bytecode(iD, interface):
    global settlement_storage_interface
    global merchant_indexes_interface
    global merchant_interface
    global settlement_interface
    if iD == 'Solidity/SettlementStorage.sol:SettlementStorage':
        settlement_storage_interface = interface
        print(f'{iD} compiled')
    elif iD == 'Solidity/MerchantIndexes.sol:MerchantIndexes':
        merchant_indexes_interface = interface
        print(f'{iD} compiled')
    elif iD == 'Solidity/Merchant.sol:Merchant':
        merchant_interface = interface
        print(f'{iD} compiled')
    elif iD == 'Solidity/Settlement.sol:Settlement':
        settlement_interface = interface
        print(f'{iD} compiled')
    else:
        print(f'Error unknown id: {iD}')


def create_settlement_storage_interface(compiled_source):
    global settlement_storage_id, settlement_storage_interface
    settlement_storage_id, settlement_storage_interface = compiled_source.popitem()


def load_configs(environment=''):
    with open(f'config_{environment}.txt') as c:
        global wallet
        global configs
        data = c.read()
        configs = json.loads(data)
        wallet.private_key = configs['private_key']


def save_config_option(option, value, environment=''):
    global configs
    configs.update({option: value})
    with open(f'config_{environment}.txt', 'w') as c:
        c.write(json.dumps(configs))
