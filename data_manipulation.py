import pandas as pd

df = pd.read_csv('./Data.csv',encoding="ISO-8859-1")
print(df.head())
print(df.dtypes)
#0 = negative, 1 = positive

