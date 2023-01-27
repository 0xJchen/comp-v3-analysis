import pandas as pd
from utils import Direction, Token, TRANSACTION, WALLET


if __name__ == '__main__':

    txs = []

    with open("v3.txt", encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            if "TX" in line:
                if not "$" in line:
                    txs.append(line.rstrip())

    watchlist = ["0x74a0", "0xEC9E", "0xccFa"]
    wallet_list = [WALLET(addr) for addr in watchlist]


    for tx in txs:
        for wallet in wallet_list:
            if wallet.addr in tx:
                wallet.add_tx(tx)
                continue

    #dump to dataframe
    total_tx = []
    for wallet in wallet_list:
        total_tx += wallet.export_txs()
        wallet.statistics(show=True)
    
    print("total WETH borrowed： {0}, total cbETH supplied:{1} out of 7,000 supply cap".format(\
        sum([wallet.total_borrow for wallet in wallet_list]),\
            sum([wallet.total_supply for wallet in wallet_list]))
    )