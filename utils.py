import re
import pandas as pd
from enum import Enum


from tabulate import tabulate
def ppdf(df):
    print(tabulate(df, headers='keys', tablefmt='psql'))
    
class Direction(Enum):
    BORROW="Borrow"
    SUPPLY="Supply"
    WITHDRAW="Withdraw"
    UNKNOWN=None
class Token(Enum):
    CBETH="cbETH"
    WSTETH="wSTETH"
    WETH="WETH"
    UNKNOWN=None
    
def parse_amount(s):
    amt=re.search(r'\d+(?:,\d+)? WETH',s)
    amt=amt.group()[:-5].replace(',','')
    amt=int(amt)
    return amt

def parse_address(s):
    addr=re.search("by .*",s).group()[3:]
    return addr

def parse_direction(s):
    direction=None
    for op in Direction:
        if op.value in s:
            direction=op
            break
    return direction.value

def parse_token(s):
    token=None
    for op in Token:
        if op.value in s:
            token=op
            break
    return token.value
            


class TRANSACTION():
    def __init__(self, tx_hash=None, amount=0, from_addr=None,
                 direction=Direction.UNKNOWN, token=Token.UNKNOWN):
        self.tx_hash = tx_hash
        self.amount = amount
        self.direction = direction
        self.from_addr = from_addr
        self.token = token


class WALLET():
    def __init__(self, addr):
        self.addr = addr
        self.txs = []
        self.amount = 0
        self.tx = TRANSACTION()
        self.total_borrow=0
        self.total_supply=0
        self.df=None

    def add_tx(self, s):
        amount = parse_amount(s)
        address = parse_address(s)
        direction = parse_direction(s)
        token = parse_token(s)
        tx = TRANSACTION(amount=amount, from_addr=address,
                         direction=direction, token=token)
        if Direction.WITHDRAW.value in s:
            print(s)
        self.txs.append(tx)

    def export_txs(self):
        return [tx.__dict__ for tx in self.txs]

    def isme(self, addr):
        return True if self.addr == addr else False

    def tx_len(self, show=False):
        if show:
            print(self.txs)
        return len(self.txs)
    
    def statistics(self,show=False):
        #find borrowed or supplied assets
        
        #counting for each asset
        self.df=pd.DataFrame(self.export_txs())
        if show==True:
            ppdf(self.df)
        self.total_borrow=self.df.loc[self.df['direction'] == Direction.BORROW.value, \
            "amount"].sum()
        self.total_supply=self.df.loc[self.df['direction'] == Direction.SUPPLY.value, \
            "amount"].sum()
        print("[address]: {0} | [total borrow]: {1} | [total supply]: {2}".format(self.addr,self.total_borrow,self.total_supply))
        
        