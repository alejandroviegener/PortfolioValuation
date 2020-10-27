"""This module contain classes that encapsule the assets (Bonds, Stocks, Cash) in a financial portfolio

    Assets have an id, a type, a purchase price, holding and purchase timestamp
    Assest of the same type and id can be added and substracted. 
    The Asset class needs to be initialized with a PricingSystem object

   Usage example:

    Asset.pricing_system = PricingSystem()

    cash_asset_1 = CashAsset("CA1", 200, Currency.Dollars, 0,8)
    cash_asset_2 = CashAsset("CA1", 200, Currency.Dollars, 0,8)
    bond_asset_1 = BondAsset("BA1", 20, Currency.Euros, 3)
    bond_asset_2 = BondAsset("BA1", 40, Currency.Euros, 4)
    
    print(cash_asset_1)
    print(bond_asset_1)
    print(cash_asset_1 + cash_asset_2)
    print(bond_asset_1 + bond_asset_2)
    print(cash_asset_1 == bond_asset_2)
"""

from enum import Enum, unique
from Currency import Currency


@unique
class AssetType(Enum):
    """Defines unique type of assets that are available"""

    Cash = "CASH"
    Bond = "BOND"
    Stock = "STOCK"


class Asset:
    """Financial asset. An asset is defined by:
            - its type (AssetType)
            - purchase currency (Currency)
            - a string that represents a unique asset id
            - unit price of the asset expressed in its currency
            - the holding (amount) of that particular asset
    """

    # Pricing system object to determine the current asset value
    # and to convert currency values
    pricing_system = None

    def __init__(self, asset_type, id, holding, currency = Currency.Dollars, unit_price = 0, timestamp = None):
        """Create a new asset

        Args:
            asset_type: AssetType object
            id: a unique identifier for the asset
            currency: Currency object
            unit_price: non negative asset unit price
            holding: ammount of this asset
            timestamp: timestamp identifying the purchse date

        Raises:
            ValueError: if holding is negative values
        """
        
        # Paramater checking
        if holding < 0:
            raise ValueError("holding must be a non negative value")
        if unit_price < 0:
            raise ValueError("holding must be a non negative value")
        
        # Assign attribute values
        self.type = asset_type
        self.id = id  
        self.currency = currency
        self.holding = holding
        self.unit_price = unit_price
        self.timestamp = timestamp

    def purchase_value( self, currency = None):
        """Gets the purchse value of the current holding in the specified currency∫"""

        if currency == None:
            currency = self.currency
        
        # Compute purchase value and convert currency if neccesary
        purchase_value = self.holding * self.unit_price
        if currency != self.currency:
            purchase_value =  self.pricing_system.convert_currency_value(purchase_value, self.currency, currency, self.timestamp)

        return purchase_value

    def current_value(self, currency = None):
        """Gets the current value of the asset in the specified currency"""

        if currency == None:
            currency = self.currency

        # Get the current value of the asset, its unit price
        current_unit_price = self.pricing_system.get_asset_sell_price(self.id, currency)
        return self.holding * current_unit_price

    def profit(self, currency = None):
        """Get the current profit of this asset in the specified currency"""

        if currency == None:
            currency = self.currency
        
        return self.current_value(currency) - self.purchase_value(currency)


    def __eq__(self, other):
        """Equal operator

        Two assets are equal if they are equal in all its attributes (timestamp is not considered)
        """

        if other == None:
            return False

        return ((self.currency == other.currency) and 
                (self.id == other.id) and 
                (self.type == other.type) and 
                (self.unit_price == other.unit_price) and
                (self.holding == other.holding))

    def __ne__(self, other):
        """Not equal operator"""
        return not self.__eq__(other)

    def __sub__(self, other):
        """ Overload of substract operator
        Assets must be of same type and id
        The resuting asset has a holding of (self.holding - other.holding) with no
        change in the other attributes

        Raises:
            ValueError: if operands not of the same type and id
        """

        if self.type != other.type or self.id != other.id:
            raise ValueError("Assest to substract must be of the same type and id")

        total_holding = self.holding - other.holding
        return Asset(self.type, self.id, total_holding, self.currency, self.unit_price, self.timestamp)

    def __add__(self, other):
        """Overloads add operator
        The assets must be of the same type, id
        Adds the two assets holdings and computes the new unit price.
        If both assets have been bought in different currencies, then the self currency
        is used and the other currency is converted.

        Raises: 
            ValueError: if summands not of the same type and id
        """

        if self.type != other.type or self.id != other.id:
            raise ValueError("Assest to add must be of the same type and id")
            
        # Compute the sum of the two assets
        # The other puschase value will be converted to self.currency if necessary
        total_holding = self.holding + other.holding
        total_purchase_value = self.purchase_value() + other.purchase_value(self.currency)
        unit_price = total_purchase_value / total_holding

        return Asset(self.type, self.id, total_holding, self.currency, unit_price, other.timestamp)

    def __str__(self):
        """String output"""
        return (f"Asset type: {self.type.name}, Unit price: {self.unit_price: .3f} {self.currency.name}, Holding: {self.holding}")


class CashAsset(Asset):
    """Constructs a chash asset"""

    def __init__(self, id, holding, currency = Currency.Dollars, unit_price = 0, timestamp = None):
        """Create new asset

        Args:
            id: a unique identifier for the asset
            currency: Currency object
            holding: ammount of this asset

        Raises:
            ValueError: if holding is negative values
        """
    
        super(CashAsset, self).__init__(AssetType.Cash, id, holding, currency, unit_price, timestamp)


class BondAsset(Asset):
    """Constructs a bond asset"""

    def __init__(self, id, holding, currency = Currency.Dollars, unit_price = 0, timestamp = None):
        """Create new asset

        Args:
            id: a unique identifier for the asset
            currency: Currency object
            unit_price: non negative asset unit price
            holding: ammount of this asset

        Raises:
            ValueError: if unit price or holding are negative values
        """
    
        super(BondAsset, self).__init__(AssetType.Bond, id, holding, currency, unit_price, timestamp)


class StockAsset(Asset):
    """Constructs a stock asset"""

    def __init__(self, id, holding, currency = Currency.Dollars, unit_price = 0, timestamp = None):
        """Create new asset

        Args:
            id: a unique identifier for the asset
            currency: Currency object
            unit_price: non negative asset unit price
            holding: ammount of this asset

        Raises:
            ValueError: if unit price or holding are negative values
        """
    
        super(StockAsset, self).__init__(AssetType.Stock, id, holding, currency, unit_price, timestamp)


if __name__ == "__main__":

    import MockPricingSystem
   
    Asset.pricing_system = MockPricingSystem.MockPricingSystem()

    cash_asset_1 = CashAsset("CA1", 350, Currency.Dollars, 0.8)
    print(cash_asset_1)

    cash_asset_2 = CashAsset("CA1", 200, Currency.Dollars, 0.9)
    print(cash_asset_2)

    bond_asset_1 = BondAsset("BA1", 20, Currency.Euros, 3)
    print(bond_asset_1)

    bond_asset_2 = BondAsset("BA1", 40, Currency.Dollars, 4)
    print(bond_asset_2)


    print(cash_asset_1 + cash_asset_2)
    print(cash_asset_1 - cash_asset_2)
    print(bond_asset_1 + bond_asset_2)

    print(cash_asset_1 == bond_asset_2)
