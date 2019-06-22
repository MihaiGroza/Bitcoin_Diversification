from yahoo_fin.stock_info import get_data
import numpy as np
import pandas as pd
import io

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

        day_count = 1
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
            day_count = day_count +1

        print(allocation)
        self.portfolio_data["portfolio value"] = 0
        for ticker in self.tickers:
            self.portfolio_data["portfolio value"] = self.portfolio_data[ticker + " value"] + self.portfolio_data["portfolio value"]

        #print(self.portfolio_data.head())
        #print(self.portfolio_data.tail())
        self.portfolio_data['portfolio value'] = self.portfolio_data.pct_change()
        self.portfolio_data['portfolio value'] = self.portfolio_data +1 
        self.portfolio_data['portfolio value'].iloc[0] = 1
        
 

        
        self.portfolio_data.index = pd.to_datetime(self.portfolio_data.index)
        print(self.portfolio_data.groupby(pd.Grouper(freq="M"))["portfolio value"].std())
        #print(self.portfolio_data)
        

portfoliode = portfolio(['btc-usd','SPY',"VBMFX"])


portfoliode.import_data(start_date = '01/01/2015', end_date = '01/01/2017')
portfoliode.backtest([10,690,300])



port = portfolio(['SPY',"VBMFX"])

port.import_data(start_date = '01/01/2015', end_date = '01/01/2017')

port.backtest([700,300])





