"""Tests for the Asset module"""

import sys
sys.path.append("../")

import unittest
from Currency import Currency
from  Asset import Asset, CashAsset, BondAsset, StockAsset 
import MockPricingSystem

class TestAsset(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup only once at class level"""
        Asset.pricing_system = MockPricingSystem.MockPricingSystem()

    def setUp(self):
        """Create assets for later use in the tests"""

        # Cash assets
        self.cash_asset_1 = CashAsset("CA1", 100, Currency.Dollars, 1)
        self.cash_asset_2 = CashAsset("CA1", 200, Currency.Dollars, 1)
        self.cash_asset_3 = CashAsset("CA1", 100, Currency.Dollars, 1)
        self.cash_asset_sum_1_2 = CashAsset("CA1", 300, Currency.Dollars, 1)

        # Bond assets
        self.bond_asset_1 = BondAsset("BA1", 20, Currency.Euros, 3)
        self.bond_asset_2 = BondAsset("BA1", 40, Currency.Euros, 4)
        self.bond_asset_sum_1_2 = BondAsset("BA1", 60, Currency.Euros, (3*20 + 4*40)/60)

        # Stock assets
        self.stock_asset_1 = StockAsset("SA1", 100, Currency.Dollars, 3.8)
        self.stock_asset_2 = StockAsset("SA1", 50, Currency.Dollars, 4)
        self.stock_asset_3 = StockAsset("SA2", 50, Currency.Euros, 2)
        self.stock_asset_4 = StockAsset("SA1", 120, Currency.Euros, 4.5)

        sum_unit_price = (100 * 3.8 + 120 * Asset.pricing_system.convert_currency_value( 4.5, Currency.Euros, Currency.Dollars)) / 220
        self.stock_asset_sum_1_4 = StockAsset("SA1", 220, Currency.Dollars, sum_unit_price)
        self.stock_asset_sub_4_1 = StockAsset("SA1", 20, Currency.Euros, 4.5)

    def test_creation(self):
        """Test exceptions on creation"""

        # Should raise excption if holding is negative
        with self.assertRaises(ValueError):
            obj = CashAsset("CA1", -1, Currency.Dollars, 1)

        # Should raise exception if unit price negative
        with self.assertRaises(ValueError):
            obj = BondAsset("BA1", 20, Currency.Euros, -5)


    def test_equal(self):
        """Test equal method overload"""

        # Check equal
        self.assertEqual(self.cash_asset_1, self.cash_asset_3)
        
        # Check not equal
        self.assertNotEqual(self.bond_asset_1, self.bond_asset_2)
        self.assertNotEqual(self.stock_asset_1, self.stock_asset_2)
        self.assertNotEqual(self.cash_asset_1, self.bond_asset_1)
        self.assertNotEqual(self.stock_asset_1, self.stock_asset_3)

    def test_add(self):
        "Test add overload method"

        # Check asset addition is OK
        self.assertEqual(self.cash_asset_1 + self.cash_asset_2, self.cash_asset_sum_1_2)
        self.assertEqual(self.bond_asset_1 + self.bond_asset_2, self.bond_asset_sum_1_2)
        self.assertEqual(self.stock_asset_1 + self.stock_asset_4, self.stock_asset_sum_1_4)

        # Check asset addition raises an exception when adding different types
        with self.assertRaises(ValueError):
            s = self.cash_asset_1 + self.bond_asset_1

        with self.assertRaises(ValueError):
            s = self.cash_asset_1 + self.stock_asset_1

    def test_sub(self):
        """Test substraction overload method"""

        # Check asset substraction is Ok
        self.assertEqual(self.stock_asset_4 - self.stock_asset_1, self.stock_asset_sub_4_1)
        
        # Check negative values are not allowed
        with self.assertRaises(ValueError):
            s = self.stock_asset_1 - self.stock_asset_4

    def test_purchase_value(self):
        """Test purchase value computation in different currencies"""

        self.assertEqual(self.stock_asset_1.purchase_value(), 380)
        self.assertEqual(self.stock_asset_1.purchase_value(Currency.Euros), 304)
        self.assertEqual(self.stock_asset_1.purchase_value(Currency.Dollars), 380)

    def test_current_value(self):
        """Test current asset value computation in differente currencies"""

        self.assertEqual(self.stock_asset_1.current_value(), 520.0)
        self.assertEqual(self.stock_asset_1.current_value(Currency.Euros), 450.0)
        self.assertEqual(self.stock_asset_1.current_value(Currency.Dollars), 520.0)

    def test_profit(self):
        """Test profit computation of asset in different currencies"""

        self.assertEqual(self.stock_asset_1.profit(), 140)
        self.assertEqual(self.stock_asset_1.profit(Currency.Euros), 146)
        self.assertEqual(self.stock_asset_1.profit(Currency.Dollars), 140)
    

if __name__ == "__main__":
    unittest.main()
   