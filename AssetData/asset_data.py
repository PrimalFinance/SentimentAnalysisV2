import os 

# Yahoo Finance imports
import yfinance as yf 

# Pandas imports 
import pandas as pd


cwd = os.getcwd()

# Path to storage folder.
storage_folder = f"{cwd}\\AssetData\\Storage"


class AssetData:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
    
    '''-----------------------------------'''
    '''-----------------------------------'''
    def get_price_data(self) -> pd.DataFrame:
        csv_file_path = f"{storage_folder}\\{self.ticker}.csv"

        try:
            df = pd.read_csv(csv_file_path)
            print(f"[Price Data] Price data retrieved from local csv file: {csv_file_path}")
        except FileNotFoundError:
            print(f"[Price Data] Price data retrieved from Yahoo Finance.")
            df = yf.download(self.ticker, period="max")
            # In this case we want to write the index, because Yahoo Finance dataframes put the date as the index. And we want to write the date. 
            df.to_csv(csv_file_path, index=True)
            # Reset the index, so that the df will be returned in a similar state to as if it was read from the csv. 
            df = df.reset_index()
        return df
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''