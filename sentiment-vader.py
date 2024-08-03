from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def get_compound_info(df,ticker_list):
    
    ticker_compounds = dict()
    total_compound = 0
    count_compound = 0
    ticker_index = 0
    next_ticker = False
    
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
        
        total_compound = ticker_compounds[ticker][0]
        count_compound = ticker_compounds[ticker][1]
        
        if count_compound == 0:
            print("Company: " + ticker + ", No news today\n")
        else:
            print(f"Company: {ticker}, Total: {total_compound}, Count: {count_compound}, Average: {total_compound/count_compound}\n")

finviz_url = 'https://finviz.com/quote.ashx?t='

ticker_list = ['AMZN', 'GOOG', 'META','NVDA', 'AMD', 'MMM', 'GEN']

news_tables = dict()
for ticker in ticker_list:
    url = finviz_url + ticker
    
    req = Request(url=url, headers={'user-agent':'my-app'})
    res = urlopen(req)
    
    html = BeautifulSoup(res, 'html')
    
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

df['date'] = pd.to_datetime(df.date).dt.date

# get_compound_info(df,ticker_list)

# plt.figure(figsize=(10,8))

mean_df = df.groupby(['ticker','date']).mean(numeric_only=True)
mean_df = mean_df.unstack()
mean_df = mean_df.xs('compound',axis='columns').transpose()

# mean_df.plot(kind='bar')
# plt.show()
# plt.savefig('compound_info.png')
print(mean_df)
choice = ''
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