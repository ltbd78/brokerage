class Account:
    def __init__(self, cash_balance, positions=None):
        self.cash_balance = cash_balance
        if positions is None:
            self.positions = dict() # example: {'btc': [1, 65000], 'eth':[-3, 4300]}
        else:
            self.positions = positions
        
        self.limit_orders = []
    
    @property
    def asset_balance(self):
        asset_balance = 0
        if len(self.positions.values()) != 0:
            for n, p in self.positions.values():
                asset_balance += n*p
        return asset_balance
    
    @property
    def total_balance(self):
        return self.cash_balance + self.asset_balance
    
    def update_position(self, id, n, p):
        if n == 'close':
            n = -self.positions[id][0]
        self.cash_balance -= n*p
        if id not in self.positions:
            self.positions[id] = [n, p]
        else:
            n0, p0 = self.positions[id]
            self.positions[id][1] = p
            self.positions[id][0] += n
        
        # Remove empty positions
        if self.positions[id][0] == 0: 
            self.positions.pop(id)
            
    def summary(self):
        print(f'Cash Balance: {self.cash_balance}')
        print(f'Asset Balance: {self.asset_balance}')
        print(f'Total Balance: {self.total_balance}')
        print(f'Positions: {self.positions}')