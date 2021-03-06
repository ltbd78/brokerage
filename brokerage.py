from typing import List

import pandas as pd

from account import Account
from datastream import *


class Brokerage:
    def __init__(self, datastream: DataStream, accounts: List[Account]):
        self.datastream = datastream
        self.accounts = accounts
        self.orders = dict()
    
    def __next__(self):
        data = next(self.datastream)
        for id_account, account in self.accounts.items():
            for id_asset in self.datastream.ids_asset:
                # gets current price
                price = data[id_asset]
                
                # process orders if exists
                if (id_account, id_asset) in self.orders:
                    orders = self.orders[id_account, id_asset]
                    id_orders = list(self.orders[id_account, id_asset].keys()) # to allow dictionary del operation during iteration
                    for id_order in id_orders:
                        if orders[id_order]['type'] == 'market':
                            n = orders[id_order]['n']
                            self.remove_order(id_account, id_asset, id_order)
                        elif orders[id_order]['type'] == 'limit':
                            if orders[id_order]['n'] > 0 and price < orders[id_order]['price']: # limit buy
                                n = orders[id_order]['n']
                                self.remove_order(id_account, id_asset, id_order)
                            elif orders[id_order]['n'] < 0 and price > orders[id_order]['price']: # limit sell
                                n = orders[id_order]['n']
                                self.remove_order(id_account, id_asset, id_order)
                            else:
                                n = 0
                else:
                    n = 0 # just updates current asset price if no orders
                
                # updates account
                account.update_position(id_asset, n, price)
    
    def add_order(self, id_account, id_asset, id_order, type, n, price=None):
        if type == 'limit':
            assert price is not None
        if (id_account, id_asset) not in self.orders:
            self.orders[(id_account, id_asset)] = dict()
        self.orders[(id_account, id_asset)][id_order] = {
            'n': n,
            'price': price,
            'type': type}
    
    def remove_order(self, id_account, id_asset, id_order):
        del self.orders[(id_account, id_asset)][id_order]