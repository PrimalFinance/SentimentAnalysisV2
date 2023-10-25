import os

import pprint

# Date & Time imports 
import datetime as dt

import pandas as pd


# NOTE: To properly install this library, you may need to downgrade your "feedparser" library to version 58. This is the command: pip install "setuptools<58.0"
from pygooglenews import GoogleNews

# Import articles related 
from newspaper import Article
from newspaper.article import ArticleException

# Import sentitment model. 
import Model.sentiment_analysis


# Paths to folders. 
google_news_folder = "D:\Datasets\ArticleHeadlines\GoogleNews"


class GoogleNewsScraper:
    def __init__(self, language: str = "en", country: str = "US"):
        self.gn = GoogleNews(lang=language, country=country)
        self.sentiment_model = Model.sentiment_analysis.SentimentModel()
    '''-----------------------------------'''
    def query_topic_headlines(self, topic: str = "business"):
        """
        :param topic: The topic to search the top headlines for. 
        Accepted topics are: WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SCIENCE, SPORTS, HEALTH    

        Description: Query google news and get the top stories for the topic. 
        """


        topic_headlines = self.gn.topic_headlines(topic)

        pprint.pprint(topic_headlines)
    '''-----------------------------------'''
    def query_search(self, search_term: str, exclude_term: str = "", time_frame: str = "6m"):
        """
        :param search_term: Used to determine the subject of articles to return. 
        :param exclude_term: Used to determine if an article should be excluded do to it containing a specific term. 
        :param time_frame: Determine how far back articles should be collected. 
        """
        # No terms to exclude. 
        if exclude_term == "":
            search = self.gn.search(f"{search_term}", when=time_frame)
        else:
            search = self.gn.search(f"{search_term} -{exclude_term}", when=time_frame)

        csv_file_path = f"{google_news_folder}\\{search_term}"

        if not os.path.exists(csv_file_path):
            # Create a directory for the search term. 
            os.mkdir(csv_file_path)
        csv_file_path += f"\\{search_term}_gn_headlines.csv"

        articles_collected = []
        for result in search["entries"]:

            #print(f"Result: {result}")
            title = result["title"]
            link = result["link"]
            # Access the content of the article.
            try: 
                article = Article(link)
                article.download()
                article.parse()

                # Get the date and time the article was published. 
                publish_date = result["published"]

                # Get the summary of the article. 
                article_summary = article.summary

                # Convert the date string to a datetime object
                date_object = dt.datetime.strptime(publish_date, "%a, %d %b %Y %H:%M:%S %Z")
                # Convert the datetime object to the desired format and set the timezone to UTC
                formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S UTC")
                formatted_date = date_object.strptime(formatted_date, "%Y-%m-%d %H:%M:%S %Z")


                body = article.text.replace("\n", "")
                article_data = {
                    "title": title,
                    "publishDate": formatted_date.date(),
                    "publishTime": formatted_date.time(),
                    "body": f'"{body}"',
                    "summary": f'"{article_summary}"',
                    "url": link
                }

                articles_collected.append(article_data)
            except ArticleException:
                pass
           

        df = pd.DataFrame(articles_collected)
        return df

    '''-----------------------------------'''
    def calculate_article_sentiment(self, article) -> dict:

        # Get the sentiment score for each piece of the article. 
        title_score = self.sentiment_model.analyze_text(article["title"])
        body_score = self.sentiment_model.analyze_text(article["body"])

        # Dictionary to hold the basic data and sentiment score data. 
        article_data = {
                "publishDate": article["publishDate"],
                "title": article["title"],
                "titleNeg": title_score["neg"],
                "titleNeu": title_score["neu"],
                "titlePos": title_score["pos"],
                "titleComp": title_score["compound"],
                "body": article["body"],
                "bodyNeg": body_score["neg"],
                "bodyNeu": body_score["neu"],
                "bodyPos": body_score["pos"],
                "bodyComp": body_score["compound"],
                "url": article["url"]
        }
        return article_data

    '''-----------------------------------'''
    def get_total_subject_sentiment(self, article_subject: str):

        
        article_csv_path = f"{google_news_folder}\\{article_subject}\\{article_subject}_gn_headlines.csv"
        articles_df = pd.read_csv(article_csv_path)

        # Order by date column. 
        articles_df = articles_df.sort_values(by="publishDate", ascending=True)
        articles_df = articles_df.reset_index(drop=True)

        sentiment_collected = []
        for i in articles_df.iterrows():
            article_sentiment_data = self.calculate_article_sentiment(article=i[1])
            sentiment_collected.append(article_sentiment_data)
        sentiment_df = pd.DataFrame(sentiment_collected)
        return sentiment_df
    '''-----------------------------------'''
    def get_articles(self, search_term: str, custom_path: str = ""):

        if custom_path == "":
            csv_file_path = f"{google_news_folder}\\{search_term}\\{search_term}_gn_headlines.csv"
        else:
            csv_file_path = custom_path

        # Try to read the articles into the dataframe. 
        try:
            articles_df = pd.read_csv(csv_file_path)
        # If the file does not exist, query it from the GoogleNews class. 
        except FileNotFoundError:
            articles_df = self.query_search(search_term)
            articles_df = articles_df.sort_values(by="publishDate", ascending=True)
            articles_df.reset_index(drop=True, inplace=True)
            articles_df.to_csv(csv_file_path, index=False)
        
        return articles_df

    '''-----------------------------------'''
    def get_articles_sentiment(self, search_term: str, custom_path: str = ""):
        if custom_path == "":
            csv_file_path = f"{google_news_folder}\\{search_term}\\{search_term}_sentiment_data.csv"
        else:
            csv_file_path = custom_path
        
        # Try to read the articles from the dataframe. 
        try:
            sentiment_df = pd.read_csv(csv_file_path)
        # If the file does not exist, query it from the internal class function. 
        except FileNotFoundError:
            sentiment_df = self.get_total_subject_sentiment(article_subject=search_term)
            sentiment_df.to_csv(csv_file_path)
        
        return sentiment_df
    '''-----------------------------------'''