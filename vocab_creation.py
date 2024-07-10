import pandas as pd
from ast import literal_eval
import json

df = pd.read_csv('./cleaned_strings.csv', encoding="ISO-8859-1")

# with open ('vocab.json', 'r') as json_file:
#     model = json.load(json_file)

df['Headline'] = df['Headline'].apply(literal_eval)

vocab = dict()

for headline in df['Headline']:
    for word in headline:
        if word not in vocab:
            vocab[word] = 0

# with open('vocab.json', 'w') as json_file:
#     json.dump(vocab, json_file)

