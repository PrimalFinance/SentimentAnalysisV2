


# Pandas imports
import pandas as pd

import ast

# Graph imports 
import matplotlib.pyplot as plt
import mplfinance as mpf



class DataGraphs:
    def __init__(self, ticker: str):
        self.ticker = ticker 

    
    '---------------------------------- Finance ----------------------------------'
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def plot_sentiment(self, df: pd.DataFrame):
        
        # --- Preprocessing Data ---
        # Create a separate dataframe with open, high, low, close (ohlcv) data. 
        ohlcv = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        #ohlc = pd.to_datetime(ohlc["Date"]) # Convert column of dates to datetime object. 
        ohlcv.set_index("Date", inplace=True)
        # Create mpl candlestick object. 
        #candlestick_ohlcv = mpl.candlestick_ohlc(ax, ohlc, width=0.6, colorup="green", colordown="red")

        #plt.plot(df["Date"], new_df["compound"], marker="o", linestyle="-")

        
        # Create the subplot objects
        sentiment_subplot_ylabel = "Sentiment Score"
        neg_sentiment_subplot = mpf.make_addplot(df["bodyNeg"], panel=2, secondary_y=True, ylabel=sentiment_subplot_ylabel, color="red")
        neu_sentiment_subplot = mpf.make_addplot(df["bodyNeu"], panel=2, secondary_y=True, ylabel=sentiment_subplot_ylabel, color="yellow") 
        pos_sentiment_subplot = mpf.make_addplot(df["bodyPos"], panel=2, secondary_y=True, ylabel=sentiment_subplot_ylabel, color="green")
        compound_sentiment_subplot = mpf.make_addplot(df["bodyComp"], panel=3, secondary_y=False, ylabel="Compound Score")
        
        
        df.set_index("Date", inplace=True)
       # Create a candlestick chart
        mpf.plot(df, type='candle', title=f'{self.ticker} Chart', addplot=[neg_sentiment_subplot, neu_sentiment_subplot, pos_sentiment_subplot, compound_sentiment_subplot],volume=True, 
                style='yahoo')

        # Combine the financial chart and the stacked bar charts
        plt.show()
    '''-----------------------------------'''
    def make_sentiment_bars(self, ax, data: pd.DataFrame):
        width = 0.2
        ax.bar(data.index, data['neg'], width=width, label='Negative', color='red', alpha=0.7)
        ax.bar(data.index, data['neu'], width=width, label='Neutral', color='yellow', alpha=0.7, bottom=data['neg'])
        ax.bar(data.index, data['pos'], width=width, label='Positive', color='green', alpha=0.7, bottom=data['neg'] + data['neu'])
        ax.set_ylabel('Sentiment Scores')
        ax.legend(loc='upper left')
    '''-----------------------------------'''
    '''-----------------------------------'''
