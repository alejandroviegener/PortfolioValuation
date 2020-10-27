""" Get the info of a portfolio loading its transaction history

Usage:
    From the console, go to the directory where this file is located ($ROOT_DIR):

        cd $ROOT_DIR
    
    and execute this script

        python portfolio_info.py <transaction_history_file.json> <DOL|EUR>

    Example: 
        python portfolio_info.py FILE.json DOL
    
    Important! for the purpuse of this excersise, the transactions file is ignored and a fixed set of transactions is loaded

"""

import sys
import Portfolio
from Currency import Currency
from Asset import BondAsset, StockAsset, CashAsset, AssetType, Asset
import MockPricingSystem 
import time
import datetime

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Error: Expecting 2 parameters ")
        print(" - Usage: python portfolio_info.py <transaction_history_file.json> <DOL|EUR>")
        exit()

    # Define currency, pricing system (MOCK), and create empy portfolio
    currency = Currency.Dollars if sys.argv[2] == "DOL" else Currency.Euros
    Asset.pricing_system = MockPricingSystem.MockPricingSystem()
    portfolio = Portfolio.Portfolio()

    # This transaction list should have been loaded from the imput file 
    ts1 = time.mktime(datetime.datetime.strptime("01/01/2020", "%d/%m/%Y").timetuple())
    ts2 = time.mktime(datetime.datetime.strptime("14/02/2020", "%d/%m/%Y").timetuple())
    ts3 = time.mktime(datetime.datetime.strptime("15/03/2020", "%d/%m/%Y").timetuple())
    transactions_list = [ 
                            (CashAsset("DOL", 1000, Currency.Dollars, 1, ts1), None),                        # Initial investment
                            (CashAsset("EU", 1000, Currency.Euros, 1, ts1), None),                           # Initial investment
                            (BondAsset("BOND1", 50, Currency.Dollars, 3.2, ts2), CashAsset("DOL", 160)),     # Buy Bond
                            (BondAsset("STOCK1", 60, Currency.Euros, 2.1, ts2), CashAsset("EU", 126)),       # Buy Stock
                            (CashAsset("DOL", 240, Currency.Dollars, 1, ts3), BondAsset("BOND1", 40)),       # Sell Bond
                        ]

    # Register transaction history of the portfolio
    portfolio.transactions(transactions_list)

    # Get the current value and assets ot the portfolio
    current_value = portfolio.get_current_value(currency)
    
    # Print portfolio info, value and individual profits
    print("\r\n#########################################################\r\n")
    print(f"Portfolio value: {current_value: .3f} {currency.name}")
    for asset in portfolio:
        asset_id = asset.id
        asset_type = asset.type
        asset_holding = asset.holding
        asset_profit = asset.profit(currency)
        asset_value = asset.current_value(currency)
        print(f"   - Asset id: {asset_id}, Asset type: {asset_type.name}, Asset holding: {asset_holding}, ", end = "" )
        print(f"Current Value: {asset_value: .3f} {currency.name}, Asset profit: {asset_profit: .3f} {currency.name}")

    print("\r\n#########################################################\r\n")


