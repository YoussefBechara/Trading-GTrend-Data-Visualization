from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

class visual_gtrend_trading:
    def __init__(self, symbol='AAPL') -> None:
        self.symbol = symbol
        gtrend_df = self.get_google_trend_data(symbol=self.symbol)
        ticker_df = self.get_ticker_historical_data(ticker=self.symbol)
        ticker_df.reset_index(drop=True, inplace=True)
        ticker_df.index = gtrend_df.index
        gtrend_df, ticker_df = gtrend_df[f'{symbol}'], ticker_df.Close
        plt.plot(gtrend_df, ticker_df)
        plt.show()
        
    def get_ticker_historical_data(self, ticker="TSLA", period="5y", interval="1wk"):
        ticker = yf.Ticker(ticker)     
        df = ticker.history(period=period, interval=interval)
        return df

    def get_google_trend_data(self, symbol):
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [symbol]
        today = datetime.today()
        past_5_years = today - timedelta(days=5*365)
        start, end = f'{today.year}-{today.month}-{today.day}' , f'{past_5_years.year}-{past_5_years.month}-{past_5_years.day}'
        pytrends.build_payload(kw_list, cat=0, timeframe=f'{end} {start}')
        return pytrends.interest_over_time()
        
    def show_correlation(self):
       pass
    
vz = visual_gtrend_trading()
