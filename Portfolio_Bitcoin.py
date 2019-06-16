from yahoo_fin.stock_info import get_data
import numpy as np
import pandas as pd


class portfolio:
    def __init__(self, tickers):
        self.tickers = tickers
        self.portfolio_data= pd.DataFrame(columns=self.tickers)
    def import_data(self,start_date, end_date):
        for ticker in self.tickers:
            
            self.portfolio_data[ticker] = get_data(ticker, start_date, end_date)['close']
             

        self.portfolio_data.fillna(method='pad',inplace=True, limit =10)

        self.portfolio_data = self.portfolio_data.pct_change()

        self.portfolio_data.drop(self.portfolio_data.index[0:3], inplace=True)

        self.portfolio_data = self.portfolio_data + 1

        print(self.portfolio_data.head())

    def backtest(self, allocation):

        day_count = 0
        portfolio_value = sum(allocation)
        weights = [x / portfolio_value for x in allocation]

        for ticker in self.tickers:
           self.portfolio_data[ticker + " value"] = self.portfolio_data[ticker].cumprod() 
           
        for index, row in self.portfolio_data.iterrows():
            if day_count % 90 == 0:
                portfolio_value = 0
                for ticker, value in zip(self.tickers,range(len(allocation))):
                    portfolio_value = allocation[value] * row[ticker + " value"] + portfolio_value
                for x , weight, ticker in zip(range(len(allocation)), weights, self.tickers):
                    allocation[x] = (portfolio_value*weight)/row[ticker + " value"]
            
            for ticker, value in zip(self.tickers,range(len(allocation))):
                row[ticker + " value"]= allocation[value] * row[ticker + " value"]

        for ticker in self.tickers:   
            self.portfolio_data["portfolio value"] = row[ticker + " value"] + self.portfolio_data["portfolio value"] 
                
                
#         btc_value = portfolio_value* 0.01
#         spy_value = portfolio_value * 0.69
#         bond_value = portfolio_value * 0.3

  



    def run_portfolio(self):
        pass


portfoliode = portfolio(['btc-usd','SPY'])

portfoliode.import_data(start_date = '01/01/2013', end_date = '01/01/2017')






