import pandas as pd
import io

# data = pd.read_csv('./Data.csv',encoding="ISO-8859-1")
# print(df.head())
# print(df.dtypes)
#0 = negative, 1 = positive

import pandas as pd
import io

# Read the data into a pandas DataFrame
data = pd.read_csv('./Data.csv', encoding="ISO-8859-1")

# Create an empty list to hold the new rows
new_rows = []

# Iterate over each row in the original DataFrame
for index, row in data.iterrows():
    date = row['Date']
    label = row['Label']
    for i in range(1, 26):
        headline = row[f'Top{i}']
        new_rows.append([date, label, headline])

# Create a new DataFrame from the new rows
new_df = pd.DataFrame(new_rows, columns=['Date', 'Label', 'Headline'])

# Write the new DataFrame to a CSV file
new_df.to_csv('transformed_data.csv', index=False)

# Print the new DataFrame for verification
print(new_df)
