import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from pytrends.request import TrendReq
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt 

class VisualGTrendTrading:
    def __init__(self, symbol='AAPL',stock_or_forex='stock') -> None:
        self.symbol = symbol
        gtrend_df = self.get_google_trend_data(symbol=self.symbol)
        if stock_or_forex.lower() == 'stock':
            ticker_df = self.get_ticker_historical_data(ticker=self.symbol)
        elif stock_or_forex.lower() == 'forex':
            ticker_df = self.get_ticker_historical_data(ticker=f'{self.symbol}=X')
        ticker_df.reset_index(drop=True, inplace=True)
        ticker_df.index = gtrend_df.index
        gtrend_df, ticker_df = gtrend_df[symbol], ticker_df.Close
        price_series = self.calc_profitloss_percentage(ticker_df)
        self.scaled_gtrend_df = self.scale_series(gtrend_df)
        self.scaled_price_series = self.scale_series(price_series)
        self.plot_chart(self.scaled_gtrend_df, self.scaled_price_series)
        
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
    
    def scale_series(self, series):
        min_val = series.min()
        max_val = series.max()
        scaled_series = (series - min_val) / (max_val - min_val)
        return scaled_series
                
    def calc_profitloss_percentage(self,series):
        profit_loss_list = []
        for i in range(len(series)):
            if i == 0:
                profit_loss_list.append(0)
                continue
            else:
                curr_price, prev_price = series[i],series[i-1]
                if prev_price > curr_price: #loss
                    percentage_loss = -((prev_price-curr_price)/prev_price)*100
                    profit_loss_list.append(percentage_loss)
                elif prev_price < curr_price: #profit
                    percentage_profit = ((curr_price-prev_price)/prev_price)*100
                    profit_loss_list.append(percentage_profit)
                else:
                    profit_loss_list.append(0)
        pdseries = pd.Series(profit_loss_list, index=series.index)
        return pdseries    
    
    def plot_chart(self, trend_series, price_series, ax=None):
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            fig = ax.figure

        trend_series.plot(marker='', linestyle='-', color='b', label='Trend Value', ax=ax)
        price_series.plot(marker='', linestyle='-', color='r', label='Prices', ax=ax)
        ax.set_title(f'Correlation between price and google trends for {self.symbol}')
        ax.set_xlabel('Date Time')
        ax.set_ylabel('Values')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        ax.legend()

        if ax is None:
            plt.show()
        else:
            fig.tight_layout()

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Google Trend Trading")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input section
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter symbol (e.g., AAPL)")
        input_layout.addWidget(QLabel("Symbol:"))
        input_layout.addWidget(self.symbol_input)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["stock", "forex"])
        input_layout.addWidget(QLabel("Type:"))
        input_layout.addWidget(self.type_combo)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_data)
        input_layout.addWidget(self.plot_button)

        # Matplotlib canvas
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)

    def plot_data(self):
        symbol = self.symbol_input.text()
        stock_or_forex = self.type_combo.currentText()

        if not symbol:
            QMessageBox.warning(self, "Input Error", "Please enter a symbol.")
            return

        try:
            vgt = VisualGTrendTrading(symbol=symbol, stock_or_forex=stock_or_forex)
            self.canvas.axes.clear()
            vgt.plot_chart(vgt.scaled_gtrend_df, vgt.scaled_price_series, ax=self.canvas.axes)
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())