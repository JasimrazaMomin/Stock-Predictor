from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
import time as tm

def get_ticker_sentiment(ticker):
    finviz_url = 'https://finviz.com/quote.ashx?t='
    
    news_tables = dict()
    
    url = finviz_url + ticker
    req = Request(url=url, headers={'user-agent': 'my-app'})
    res = urlopen(req)
    html = BeautifulSoup(res, 'html.parser')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    

    parsed_data = []

    for ticker, news_table in news_tables.items():
        
        for row in news_table.findAll('tr'):
            
            headline = row.a.text
            timestamp = row.td.text.strip().split(" ")
            
            if len(timestamp) == 1:
                time = timestamp[0]
            else:
                date = timestamp[0]
                time = timestamp[1]
                
            parsed_data.append([ticker, date, time, headline])

    df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'headline'])
    vader = SentimentIntensityAnalyzer()
    today = datetime.today().date()
    todays_date = datetime.today().strftime("%b-%d-%y")

    df['compound'] = df['headline'].apply(lambda x : vader.polarity_scores(x)['compound'])
    df['date'] = df['date'].apply(lambda x : todays_date if x == 'Today' else x)

    df['date'] = pd.to_datetime(df.date,format="%b-%d-%y").dt.date
    # print(df.shape)
    # get_compound_info(df,ticker_list) 

    # plt.figure(figsize=(10,8))

    mean_df = df.groupby(['ticker','date']).mean(numeric_only=True)
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound',axis='columns').transpose()

    # mean_df.plot(kind='bar')
    # plt.show()
    # print(mean_df.index,mean_df.index.dtype)
    # print(mean_df.columns,mean_df.columns.dtype)
    mean_df_shape = mean_df.shape
    
    # print(mean_df.iloc[mean_df_shape[0]-1,0])
    return (mean_df,float(mean_df.iloc[mean_df_shape[0]-1,0]))
start = tm.time()
print(get_ticker_sentiment("AAPL"))
stop = tm.time()
print(stop-start)