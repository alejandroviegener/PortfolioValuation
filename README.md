# PortfolioValuation / Software Challenge

System that gives value to an investment portfolio


Requirements
-------------

A Bank is interested in implementing a system that can value an investment portfolio.

Their portfolios can be made up of stocks, bonds and cash in US Dollars and Euros.

The prices for each of these instruments is determined by a separate pricing system which you will need to interact with (no need to implement this system, you can assume a valid price is always available).

Please use an object oriented language of your choice to implement a system that allows the Bank to:

1) Build up the portfolio from their transaction history (buy and sell transactions where a certain number of each instrument can be bought or sold on a given date)

2) Calculate the current value of the portfolio either in US Dollars or in Euros.  The value of each instrument held is simply the amount currently held multiplied by the current price.

3) Calculate the profit and loss of each of the investments in the portfolio assuming it can be calculated simply by:
	PnL = current holding * (current price - purchase price)

4) No "short" positions are to be allowed in the system


Usage:
------

    From the console, go to the project root directory ($ROOT_DIR):

        cd $ROOT_DIR
    
     Execute the portfolio_test.py script

        python portfolio_info.py <transaction_history_file.json> <Currency>
            - transaction_history_file.json: file that contains the transaction history of the portfolio
            - Currency: EUR or DOL 

    Example: 
        python portfolio_info.py FILE.json DOL
    
    Important! for the purpuse of this excersise, the transactions file is ignored and a fixed set of transactions is loaded 


To run the tests:
    From the console, go to the tests directory ($ROOT_DIR)/tests:

        cd $ROOT_DIR/tests
    
    Execute the tests:

        python -m unittest -v


