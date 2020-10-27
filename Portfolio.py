"""Defines a Portfolio class as a collection of Assets."""

from Currency import Currency
from Asset import BondAsset, StockAsset, CashAsset, AssetType, Asset

class Portfolio:
    """
    A Portfolio is a collection of Assets. Transaction history define the current portfolio state.
    A transaction is defined as an asset coming in the portfolio and an asset coming out. 
    Initial investments are defined as a transaction with only an input asset.

    """

    def __init__(self):
        self.assets = {}


    def _add(self, input_asset):
        """Adds an asset to the profile"""
    
        # If the asset is allready in the portfilio, add it the exixting one
        # else, add it to the porfolio
        if input_asset.id in self.assets:
            self.assets[input_asset.id] += input_asset
        else:
            self.assets[input_asset.id] = input_asset

    
    def _remove(self, output_asset):
        """Remove the asset from the porfolio

        Raises:
            ValueError: if not enough asset in portfolio to be removed
                        (no short positions are allowed)
        """
        
        if output_asset == None or output_asset.holding == 0:
            return
        if (output_asset.id not in self.assets) or (self.assets[output_asset.id].holding < output_asset.holding):
            raise ValueError("No short potitions are allowed")

        self.assets[output_asset.id] -= output_asset
        return

    def transactions(self, transaction_list):
        """Adds a list of transactions to the portfolio
        Each transaction in the list is a tuple (input_asset, output_asset)

        """

        for transaction in transaction_list:
            self.transaction(transaction[0], transaction[1])
        return

    def transaction(self, input_asset, output_asset = None):
        """Adds and removes an asset in a transaction
        
        ouput_asset can be None, representing an investment

        Raises:
            ValueError: if output_asset to be removed is greater than portfolio holding
                        (no short positions are allowed)
        """

        self._remove(output_asset)
        self._add(input_asset)
        return

    def get_asset_ids(self):
        """Return all ids of the portfolio assets"""

        return self.assets.keys()

    def get_current_value(self, currency):
        """Get the total portfolio value in the specified currency"""

        value = 0
        for asset_id, asset in self.assets.items():
            value += asset.current_value(currency)
        
        return value
    
    def get_asset_profit(self, asset_id, currency):
        """Gets the profit of a specifief asset id int the specified currency"""

        if asset_id not in self.assets:
            return None
        
        return self.assets[asset_id].profit(currency)

    def __iter__(self):
        return (asset for asset_id, asset in self.assets.items())
    
        
if __name__ == "__main__":

    import MockPricingSystem

    Asset.pricing_system = MockPricingSystem.MockPricingSystem()
    portfolio = Portfolio()
    currency = Currency.Euros

    transactions_list = [ 
                            (CashAsset("DOL", 1000, Currency.Dollars, 1), None),                        # Initial investment
                            (CashAsset("EU", 1000, Currency.Euros, 1), None),                           # Initial investment
                            (BondAsset("BOND1", 50, Currency.Dollars, 3.2), CashAsset("DOL", 160)),     # Buy Bond
                            (BondAsset("STOCK1", 60, Currency.Euros, 2.1), CashAsset("EU", 126)),       # Buy Stock
                            (CashAsset("DOL", 240, Currency.Dollars, 1), BondAsset("BOND1", 40)),       # Sell Bond
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