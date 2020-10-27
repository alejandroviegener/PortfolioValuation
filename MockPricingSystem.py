"""Defines a mock pricing system -  used to test other modulees that need a pricing system

Defines a system to convert currencies and to get sell/buy prices of assets
"""


from Currency import Currency

class MockPricingSystem():
    """This is just a Mock Class of the pricing system"""

    def convert_currency_value(self, value, input_currency, output_currency, timestamp = None):
        """ Returns the value in input currency converted as output currency according to the timestamp
            The value returned is the value in output currency that has the same acquisition capacity
            If timestamp is None, tthen current is used
        """
        if input_currency == output_currency:
            return value

        return 0.8 * value 

    def get_asset_sell_price(self, asset_id, currency, timestamp = None):
        """Returns the sell unit price of the asset in the given currency
        If timestamp is None then current is uded
        """

        if asset_id == "DOL" and currency == Currency.Dollars:
            return 1
        if asset_id == "EU" and currency == Currency.Euros:
            return 1
        
        return 4.5 if currency == Currency.Euros else 5.2

