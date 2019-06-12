from yahoo_fin.stock_info import get_data
import numpy as np
import pandas as pd

bond_data = get_data('VBMFX', start_date = '01/01/2013', end_date = '01/01/2017')
btc_data = get_data('btc-usd', start_date = '01/01/2013', end_date = '01/01/2017')
spy_data = get_data('SPY', start_date = '01/01/2013', end_date = '01/01/2017')


#market_data = btc_data['close']
#market_data.join(bond_data['close'])
#market_data.join(spy_data['close'])

market_data = pd.concat([btc_data['close'], bond_data['close'], spy_data['close']], axis=1, sort=True)
market_data.columns = ['btc','bond','spy']
#market_data['spy'].fillna({c: market_data['spy'].close.shift() for c in market_data['spy']}).ffill()

market_data.fillna(method='pad',inplace=True, limit =10)

market_data = market_data.pct_change()

market_data.drop(market_data.index[0:3], inplace=True)

market_data = market_data + 1

bond_value = 300
btc_value = 10
spy_value = 690
portfolio_value = 1000

spy_list = []
bond_list = []
btc_list = []
portfolio_list = []

day_count = 0
for index, row in market_data.iterrows():
    if day_count % 90 == 0:
        btc_value = portfolio_value* 0.01
        spy_value = portfolio_value * 0.69
        bond_value = portfolio_value * 0.3

    bond_value= bond_value * row['bond']
    btc_value = btc_value * row['btc']
    spy_value = spy_value * row['spy']
    portfolio_value = bond_value + btc_value + spy_value

    bond_list.append(bond_value)
    spy_list.append(spy_value)
    btc_list.append(btc_value)
    portfolio_list.append(portfolio_value)

portfolio = pd.DataFrame(np.column_stack([btc_list,spy_list,bond_list,portfolio_list]), columns=['BTC Value','SPY Value','Bond Value','portfolio'])
portfolio.index = market_data.index

portfolio_returns = portfolio.pct_change()


print(portfolio.tail())












#btc_close =btc_data.loc[:,'close']
#fb_close = fb_data.loc[:, 'close']


#for index, row in fb_data.iterrows():
#    print(row['close'])

#stock_prices = [100]
#fb_returns = fb_close.pct_change()
#fb_returns = fb_returns.drop(fb_returns.index[0])

#fb_returns = fb_returns +1


#fb_returns.columns = ['returns']
#df = df.rename(columns={'oldName1': 'newName1', 'oldName2': 'newName2'})
#fb_returns['portfolio'] = Series(np.random.randn(sLength), index=fb_returns.index)

#print(fb_returns.columns[1])

#fb_returns['new'] = pd.Series([0 for x in range(len(fb_returns.index))], index=fb_returns.index)

#print(pd.DataFrame({'index':fb_returns.index, 'returns':fb_returns.values, 'new':fb_returns.values}))

#print(btc_data.head())
#print(btc_data.tail())
