import pandas as pd
import re

def clean_headline(headline):
    headline = headline.lower()
    headline = re.sub(r'[^a-z0-9 ]', '', headline)
    words = headline.split()
    cleaned_words = [word for word in words if word not in irrelevant_word]
    return cleaned_words

df = pd.read_csv('./cleaned_data.csv', encoding="ISO-8859-1")

irrelevant_word = {'a': 1, 'the' : 1, 'to' : 1, 'and' : 1, 'or' : 1, 'so' : 1, 'is' : 1, 'an' : 1, 'this' : 1, 'that' : 1, 'these' : 1, 'those' : 1, 'in': 1, 'as':1, 'also':1, 'i' : 1, 'of' : 1}

df['Headline'] = df['Headline'].apply(clean_headline)

df.to_csv('cleaned_strings.csv',index=False)