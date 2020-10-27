"""Tests for the Portfolio module"""

import sys
sys.path.append("../")

import unittest
from Currency import Currency
from  Asset import Asset, CashAsset, BondAsset, StockAsset 
import MockPricingSystem
from Portfolio import Portfolio

transactions_list = [ 
                        (CashAsset("DOL", 1000, Currency.Dollars, 1), None),                        # Initial investment
                        (CashAsset("EU", 1000, Currency.Euros, 1), None),                           # Initial investment
                        (BondAsset("BOND1", 50, Currency.Dollars, 3.2), CashAsset("DOL", 160)),     # Buy Bond
                        (BondAsset("STOCK1", 60, Currency.Euros, 2.1), CashAsset("EU", 126)),       # Buy Stock
                        (CashAsset("DOL", 240, Currency.Dollars, 1), BondAsset("BOND1", 40)),       # Sell Bond
                    ]

class TestPortfolio(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup only once at class level"""

        Asset.pricing_system = MockPricingSystem.MockPricingSystem()
        Asset.pricing_system = MockPricingSystem.MockPricingSystem()
        
    def setUp(self):
        self.portfolio = Portfolio() 
        self.portfolio.transactions(transactions_list)

    def test_current_value(self):
        """Test current value of portfolio in differenct currencuies"""

        # Dollars 5988.800
        # Euros 6049.000
        self.assertEqual(self.portfolio.get_current_value(Currency.Euros), 6049.0)
        self.assertEqual(self.portfolio.get_current_value(Currency.Dollars), 5988.8)

    def test_profit(self):
        """Test profit computation of asset in different currencies"""
        profits_euros = [3996, 0, 19.4, 144]
        for i, asset in enumerate(self.portfolio):
            self.assertEqual(asset.profit(Currency.Euros), profits_euros[i])
    

if __name__ == "__main__":
    unittest.main()
   