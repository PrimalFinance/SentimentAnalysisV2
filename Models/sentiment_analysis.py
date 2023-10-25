# Transformer imports
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

# Math related
import pandas as pd



class SentimentModel:
    neutral_weight_default = 4
    def __init__(self):
        # Pretrained model from a pipeline. 
        MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        self.max_section_size = 514
        
       
    '''-----------------------------------'''
    def analyze_text(self, text: str, neutral_weight: int = neutral_weight_default):
        
        # Check if the text is too big for the model's input layer. This will turn the text variable into a list of strings. 
        if len(text) > self.max_section_size:
            text = self.split_text(text)

        if isinstance(text, str):
            encoded_text = self.tokenizer(text, return_tensors="pt") # Means it will return a "PyTorch" tensor. 
            output = self.model(**encoded_text)
            # Convert from a tensor to numpy. 
            scores = output[0][0].detach().numpy()
            # Apply softmax function. 
            scores = softmax(scores)
            scores_dict = {
                "neg": scores[0],
                "neu": scores[1],
                "pos": scores[2] 
            }

            scores_dict["compound"] = self.calculate_compound_score(scores_dict, neutral_weight=neutral_weight)

            return scores_dict
        # If the text variable is of the datatype list. 
        elif isinstance(text, list):
            text_section_scores = []
            for i in text:
                encoded_text = self.tokenizer(i, return_tensors="pt") # Means it will return a "PyTorch" tensor. 
                output = self.model(**encoded_text)
                # Convert from a tensor to numpy. 
                scores = output[0][0].detach().numpy()
                # Apply softmax function. 
                scores = softmax(scores)
                scores_dict = {
                    "neg": scores[0],
                    "neu": scores[1],
                    "pos": scores[2] 
                }
                text_section_scores.append(scores_dict)
            # Variables to hold the sum of the text sections. 
            section_neg_sum = 0
            section_neu_sum = 0
            section_pos_sum = 0

            for score in text_section_scores:
                section_neg_sum += score["neg"]
                section_neu_sum += score["neu"]
                section_pos_sum += score["pos"]
                

            # Variables to hold the averages of the text section. 
            section_neg_avg = section_neg_sum / len(text_section_scores)
            section_neu_avg = section_neu_sum / len(text_section_scores)
            section_pos_avg = section_pos_sum / len(text_section_scores)
            

            average_section_score = {
                "neg": section_neg_avg,
                "neu": section_neu_avg,
                "pos": section_pos_avg
            }
            average_section_score["compound"] = self.calculate_compound_score(score=average_section_score, neutral_weight=neutral_weight)
            return average_section_score
    '''-----------------------------------'''
    def calculate_compound_score(self, score: dict, neutral_weight: int = neutral_weight_default):
        """
        :param score: Dictionary holding the sentiment score for {"neg","neu","pos"}
        :param neutral_weight: Controls how much to include the neutral score into the compound score. 
                               A higher weight is a higher inclusion. The weight range is 1-5. 

        :returns: Float of the compounded score. 

        Description: This function will take the 3 values from the sentiment score, and create a single-value compound score.
        """ 

        # Logic for weight.
        weighing = 0  
        if neutral_weight >= 5:
            weighing = 1
        elif neutral_weight == 4:
            weighing = 2
        elif neutral_weight == 3:
            weighing = 3
        elif neutral_weight == 2:
            weighing = 4
        elif neutral_weight == 1:
            weighing = 5

        # First we divide the "neu" (neutral) field by 2, to decrease it's weighing.
        try:
            neu_formatted = score["neu"] / weighing
        # If "neu" is already 0. 
        except ZeroDivisionError:
            neu_formatted = 0

        # Get the sum of the positive and negative values. 
        score_sum = score["pos"] + neu_formatted

        # Since our number scale is -1 to 1, if the sum exceeds 1, set it to 1. 
        if score_sum > 1:
            score_sum = 1

        # Subtract the negative field from the score_sum. This way, if a piece of text leans negative, the compount score will be reflected with a lower/ negative score. 
        compound_score = score_sum - score["neg"]
        # For similar reasons to score_sum, we want to keep the score within ranges of -1 to 1. So we want to make sure the score does not exceed -1 (in this case being less than).
        if compound_score < -1:
            compound_score = -1

        return compound_score

    '''-----------------------------------'''
    def display_score(self, score: dict, format_decimals: bool = True, leading_decimals: int = 2):

        if format_decimals:
           return f"Positive: {'{:{width},.{precision}f}'.format(score['pos'], width=leading_decimals, precision=leading_decimals)} \
           \nNeutral: {'{:{width},.{precision}f}'.format(score['neu'], width=leading_decimals, precision=leading_decimals)} \
           \nNegative: {'{:{width},.{precision}f}'.format(score['neg'], width=leading_decimals, precision=leading_decimals)} \
           \nCompound: {'{:{width},.{precision}f}'.format(score['compound'], width=leading_decimals, precision=leading_decimals)}"
        else:
            return f"Positive: {score['pos']}\nNeutral: {score['neu']}\nNegative: {score['neg']}\nCompound: {score['compound']}"

    '''-----------------------------------'''
    def split_text(self, text: str) -> list:
        """
        :param text: The string of text to split. 
        :returns: A list containing separate sections of the text. Each sections size is determined by "max_section_size". 
        """ 
        text_sections = []
        for i in range(0, len(text), self.max_section_size):
                            section = text[i:i+self.max_section_size]
                            text_sections.append(section)
        
        return text_sections
    '''-----------------------------------'''
    def merge_price_sentiment(self, articles_df: pd.DataFrame, price_df: pd.DataFrame):
        """
        :param articles_df: A dataframe full of articles. *Should* have sentiment data included. 
        :param price_df: A dataframe with closing and volume data for an asset. 

        :returns: A merged dataframe with price and sentiment data. As well as data related to the article. 

        Description: This function takes an article dataframe(df) and price dataframe(df). It will then use publishing dates
                     from the article df and search for the closing prices on those days. As noted, the articles df should also include
                     sentiment data. Refer to "get_articles_sentiment" on how to get articles with sentiment data. 
        
        """


        # List to hold data points where an article is published on a trading day. 
        data_points = []



        # Convert to datetime. 
        articles_df["publishDate"] = pd.to_datetime(articles_df["publishDate"])
        price_df["Date"] = pd.to_datetime(price_df["Date"])


        #date_search = price_df.loc[price_df['Date'] == '2016-09-19']

        merged_df = pd.merge(articles_df, price_df, left_on="publishDate", right_on="Date", how="inner")

        return merged_df
    '''-----------------------------------'''
    def is_ascending(self, df: pd.DataFrame, column: str = "Date", date_sort: bool = True) -> bool:
        """
        :param df: Dataframe containing any data. 
        :param column: The column to check within the dataframe. 

        :returns: Boolean. True is the data is in ascending order. 
        """

        # Convert columns to datetime object if we are sorting dates. 
        if date_sort:
            df[column] = pd.to_datetime(df[column])

        # Check if the value of the first row is greater than the last row. 
        if df[column].iloc[0] > df[column].iloc[-1]:
            return True
        else:
            return False

    