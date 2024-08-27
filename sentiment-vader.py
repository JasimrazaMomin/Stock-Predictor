from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
import requests
import time as tm

def get_sp500(): #change . to -
    URL = "https://stockanalysis.com/list/sp-500-stocks/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.findAll(class_="sym svelte-eurwtr")

    stock_list = []
    print("Entering loop for ticker finder")
    for result in results:
        children = result.findChildren("a", recursive=False)
        for child in children:
            stock_list.append(child.get_text().replace('.','-'))
        print("Finished one loop cycle")
    print("Finished ticker finder")
    return stock_list

def get_compound_info(df,ticker_list):
    
    ticker_compounds = dict()
    total_compound = 0
    count_compound = 0
    ticker_index = 0
    next_ticker = False
    today = datetime.today().date()
    
    for index in df.index:
        
        if df.at[index,'date'] != today:
            next_ticker = True
            continue
        
        if next_ticker:
            ticker_compounds[ticker_list[ticker_index]] = [total_compound,count_compound]
            ticker_index += 1
            total_compound = 0
            count_compound = 0
            next_ticker = False
            
        total_compound += df.at[index,'compound']
        count_compound += 1
    ticker_compounds[ticker_list[ticker_index]] = [total_compound,count_compound]
    # 1 is very positive, -1 is very negative
    for ticker in ticker_list:
        if ticker not in ticker_compounds:
            continue
        total_compound = ticker_compounds[ticker][0]
        count_compound = ticker_compounds[ticker][1]
        
        if count_compound == 0:
            print("Company: " + ticker + ", No news today\n")
        else:
            print(f"Company: {ticker}, Total: {total_compound}, Count: {count_compound}, Average: {total_compound/count_compound}\n")

def get_sentiment_sp500():
    print("In main function")
    finviz_url = 'https://finviz.com/quote.ashx?t='

    ticker_list = get_sp500()

    news_tables = dict()
    for ticker in ticker_list:
        url = finviz_url + ticker
        print(ticker)
        for _ in range(5):  # Retry up to 5 times
            try:
                req = Request(url=url, headers={'user-agent': 'my-app'})
                res = urlopen(req)
                html = BeautifulSoup(res, 'html.parser')
                news_table = html.find(id='news-table')
                news_tables[ticker] = news_table
                # tm.sleep(1)  # Delay between requests to avoid rate limit
                break
            except HTTPError as e:
                if e.code == 429:  # Too Many Requests
                    print(f"HTTP Error 429 for ticker {ticker}: {e}. Retrying in 1 second...")
                    tm.sleep(1)  # Wait for 30 seconds before retrying
                else:
                    print(f"HTTP Error for ticker {ticker}: {e}")
                    break
            except URLError as e:
                print(f"URL Error for ticker {ticker}: {e}")
                break

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
    print(df.shape)
    get_compound_info(df,ticker_list) 

    # plt.figure(figsize=(10,8))

    mean_df = df.groupby(['ticker','date']).mean(numeric_only=True)
    mean_df = mean_df.unstack()
    mean_df = mean_df.xs('compound',axis='columns').transpose()

    # mean_df.plot(kind='bar')
    # plt.show()
    return (mean_df,df)

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
print("Started get_ticker_sentiment")
start = tm.time()
print(get_ticker_sentiment("AAPL"))
stop = tm.time()

start1 = tm.time()
print("Started get_sentiment_sp500")
print(get_sentiment_sp500())
stop1 = tm.time()

print("Started get_sp500")
start2 = tm.time()
print(get_sp500())
stop2 = tm.time()

print(stop-start) #0.1654 s - faster to execute specific ticker searches
print(stop1-start1) #164.1693 s (2 mins 44.1693 s) - good if i want to just load a bunch of tickers at once but other two work much faster (<1s)
print(stop2-start2) #0.5646 s - faster to get a list of all tickers
# #plotting will get expensive really quickly so might just make a nice looking scale to show the current sentiment (might add drop down showing previous entries)
# plt.savefig('compound_info.png')
# print(mean_df)
# choice = ''
# while True:
#     print('COMPOUND - Get compound info\nXXXXX - Enter ticker to get ticker info\nEXIT - Exit figure selection')
#     choice = input('>>> ')
#     print()
#     choice = choice.upper()
#     if choice == 'EXIT':
#         break
#     elif choice == 'COMPOUND':
#         mean_df.plot(kind='bar')
#         plt.show()
#     else:
#         ticker = choice
#         ticker_dates = []
#         ticker_compound = []
#         pass_ticker = False
#         for index in df.index:
#             if df.at[index,'ticker'] == ticker:
#                 pass_ticker = True
#                 ticker_dates.append(df.at[index,'date'])
#                 ticker_compound.append(df.at[index,'compound'])
#             elif pass_ticker:
#                 break
#         if len(ticker_dates) == 0 or len(ticker_compound) == 0:
#             print('No info found, please try again later or double check the selection')
#         else:
#             plt.bar(ticker_dates,ticker_compound)
#             plt.show()