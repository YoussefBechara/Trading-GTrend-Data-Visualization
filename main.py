from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import yfinance as yf

class visual_gtrend_trading:
    def __init__(self, symbol='AAPL') -> None:
        self.symbol = symbol
        gtrend_df = self.get_google_trend_data(symbol=self.symbol)
        ticker_df = self.get_ticker_historical_data(ticker=self.symbol,)
        print(gtrend_df, ticker_df)
        # plt.plot(gtrend_df)
        # plt.show()
        
    def get_ticker_historical_data(self, ticker="TSLA", period="2y", interval="1h"):
        ticker = yf.Ticker(ticker)     
        df = ticker.history(period=period, interval=interval)
        return df

    def get_google_trend_data(self, symbol):
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [symbol]
        pytrends.build_payload(kw_list, cat=0, timeframe='today 2-y', geo='', gprop='')
        return pytrends.interest_over_time()
        
    def show_correlation(self):
       pass
    
vz = visual_gtrend_trading()
