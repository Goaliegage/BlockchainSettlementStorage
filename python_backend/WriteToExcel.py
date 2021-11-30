import pandas as pd
import openpyxl
import time


class OutputFile:
    filename = ''
    headers = ['Index', 'Time', 'Gas Used', 'Contract', 'Function', 'Parameter 1', 'Parameter 2', 'Parameter 3', 'Parameter 4']
    writer = None
    line_number = 0
    d_frame = None

    def __init__(self, environment):
        self.filename = f'{environment}_output_{time.strftime("%m_%d_%Y_%H_%M", time.localtime())}.xlsx'
        self.writer = pd.ExcelWriter(self.filename)
        self.d_frame = pd.DataFrame(columns=['Index', 'Time', 'Gas Cost', 'Contract', 'Function', 'Parameter 1', 'Parameter 2', 'Parameter 3', 'Parameter 4', 'Address'])

    def writeToFile(self):
        with pd.ExcelWriter(self.filename) as writer:
            self.d_frame.to_excel(writer, header=True)

    def addGeneralRow(self, index='', total_time='', gas_used='', contract_name='', function_name='', parameter1='', parameter2='', parameter3='', parameter4='', address=''):
        self.d_frame.loc[self.line_number, 'Index'] = index
        self.d_frame.loc[self.line_number, 'Time'] = total_time
        self.d_frame.loc[self.line_number, 'Gas Cost'] = gas_used
        self.d_frame.loc[self.line_number, 'Contract'] = contract_name
        self.d_frame.loc[self.line_number, 'Function'] = function_name
        self.d_frame.loc[self.line_number, 'Parameter 1'] = parameter1
        self.d_frame.loc[self.line_number, 'Parameter 2'] = parameter2
        self.d_frame.loc[self.line_number, 'Parameter 3'] = parameter3
        self.d_frame.loc[self.line_number, 'Parameter 4'] = parameter4
        self.d_frame.loc[self.line_number, 'Address'] = address
        self.line_number += 1

    def writeContractRow(self):
        pass
