from urllib.error import URLError,HTTPError
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime
import time as tm
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_ticker_sentiment',methods=['POST'])
def get_ticker_sentiment():
    data = request.json
    ticker = data.get('ticker','').upper()
    
    if not ticker:
        return jsonify({'error':'No ticker provided'}),400
    
    finviz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = dict()
    url = finviz_url + ticker
    
    try:
        req = Request(url=url, headers={'user-agent': 'my-app'})
        res = urlopen(req)
        html = BeautifulSoup(res, 'html.parser')
        news_table = html.find(id='news-table')
        
        if news_table is None:
            return jsonify({'error':'No news found'}),404
        
        news_tables[ticker] = news_table
        
    except HTTPError as e:
        return jsonify({'error': f'HTTP error occurred: {e}'}), 500
    except URLError as e:
        return jsonify({'error': f'URL error occurred: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500 
    
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
    
    if mean_df.empty:
        return jsonify({'error': 'No data available'}), 404
    
    latest = float(mean_df.iloc[mean_df_shape[0]-1,0])
    
    # print(mean_df.iloc[mean_df_shape[0]-1,0])
    # float(mean_df.iloc[mean_df_shape[0]-1,0])
    
    return jsonify(result=latest)
# start = tm.time()
# print(get_ticker_sentiment("AAPL"))
# stop = tm.time()
# print(stop-start)

if __name__ == '__main__':
    app.run(debug=True,port=5000)