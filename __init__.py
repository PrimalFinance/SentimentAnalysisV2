# Operating System imports
import os
from dotenv import load_dotenv
load_dotenv()


import time

from Model.sentiment_analysis import SentimentModel

import pandas as pd

# Import scrapers 
from Scrapers.reddit import RedditScraper
from Scrapers.googlenews import GoogleNewsScraper

# Import Graph
from Graphing.graphs import DataGraphs

# Import Asset data
from AssetData.asset_data import AssetData

import pprint

# Paths to folders. 
google_news_folder = "D:\Datasets\ArticleHeadlines\GoogleNews"



'---------------------------------- Google ----------------------------------'


def update_googlenews_dataset(search_term: str):
    google = GoogleNewsScraper()
    articles = google.query_search(search_term, time_frame="1y")

    csv_file_path = f"{google_news_folder}\\{search_term}\\{search_term}_gn_headlines.csv"
    articles.to_csv(csv_file_path, index=False)

def google_article_staging(search_term: str):
    google = GoogleNewsScraper()
    #
    article_df = google.get_articles(search_term)

def google_article_sentiment_staging(search_term: str):
    
    google = GoogleNewsScraper()
    google.get_articles_sentiment(search_term)
    #sentiment_df = google.get_total_subject_sentiment(article_subject=search_term)


'---------------------------------- Reddit ----------------------------------'


'---------------------------------- Graphs ----------------------------------'
def plot_sentiment(ticker: str):
    graph = DataGraphs(ticker)
    google = GoogleNewsScraper()
    asset = AssetData(ticker)

    # Get price data. 
    price_df = asset.get_price_data()

    # Get the articles and their sentiment scores. 
    articles_df = google.get_articles_sentiment(search_term=ticker)

    # Create a merged dataframe that contains price points on days where a news article was published. 
    merged_df = google.sentiment_model.merge_price_sentiment(articles_df, price_df)

    
    graph.plot_sentiment(df=merged_df)






'---------------------------------- Other ----------------------------------'

'''-----------------------------------'''
def text_comparison(text1, text2):

    sentiment = SentimentModel()

    text1_score = sentiment.analyze_text(text1, neutral_weight=4)
    text2_score = sentiment.analyze_text(text2, neutral_weight=4)


    print(f"""
----------------------------------
Text 1: {text1}
[Score 1]
{sentiment.display_score(text1_score)}

Text 2: {text2}
[Score 2]
{sentiment.display_score(text2_score)}

""")



google_menu = """
=======================
1. Add new articles 
2. Get articles sentiment

"""










if __name__ == "__main__":

    start = time.time()
    ticker = "META"
    #r = RedditScraper()
    #google = GoogleNewsScraper()
    #ticker = "META"
    #articles = google.query_search(ticker, time_frame="1y")

    inp = 1
    choice = 3
    # ---------------------------------- Google ----------------------------------
    if choice == 1:
        if inp == 1:
            # Create an articles csv file for the search term if there is not one already. 
            google_article_staging(ticker)
        elif inp == 2:
            google_article_sentiment_staging(ticker)
        elif inp == 3: 
            text_comparison(text1="Life is work", text2="Work is life")

    # ---------------------------------- Reddit ----------------------------------
    elif choice == 2: 
        pass

    # ---------------------------------- Graphs ----------------------------------
    elif choice == 3:
        if inp == 1:
            # Plot sentiment data. 
            plot_sentiment(ticker)

    elif choice == 4:

        df1 = pd.DataFrame({   })
    #google.get_total_subject_sentiment(ticker)
    #update_googlenews_dataset(search_term=ticker,df=articles)
    #r.get_top_posts("Cryptocurrency", 5, include_comments=True)
    #headlines_df = pd.read_csv(crypto_headlines_sentiment_file)





    end = time.time()

    elapse = end - start

    print(f"Elapse: {elapse}")
    # for i in headlines_df["headline"]:

     #   score = model.analyze_text(i)

    '''  print(f"""
        ----------------------------------------
        Headline "{i}" 
        Positive: {'{:,.2f}'.format(score['pos'])}
        Neutral: {'{:,.2f}'.format(score['neu'])}
        Negative: {'{:,.2f}'.format(score['neg'])}""")
'''
