import pandas as pd
import numpy as np
import json
from multinb import prediction,training
from ast import literal_eval
from sklearn.model_selection import KFold

data = pd.read_csv('./cleaned_strings.csv', encoding="ISO-8859-1")

kf = KFold(n_splits=10,shuffle=True, random_state=42)
folds = list(kf.split(data))

results = []

for i,(train_index,val_index) in enumerate(folds):
    print(f"Fold {i+1}")
    
    train_data = data.iloc[train_index]
    val_data = data.iloc[val_index]
    
    train_list = train_data.apply(lambda x:[x['Date'],x['Label'],x['Headline']],axis=1).tolist()
    
    print(train_list[:5])
    
    try:
        model = training(train_list)
    except TypeError as e:
        print(f"Error: {e}")
        break
    

    prob_conditional_word_dict = {
        "positive": model["positive_conditional"],
        "negative": model["negative_conditional"]
    }
    prob_class_dict = {
        "positive": model["positive_probability"],
        "negative": model["negative_probability"]
    }
    
    correct_predictions = 0
    for _, row in val_data.iterrows():
        prediction_label, _ = prediction(row['headline'], prob_conditional_word_dict, prob_class_dict)
        if prediction_label == row['label']:
            correct_predictions += 1
    
    # Store the accuracy for this fold
    accuracy = correct_predictions / len(val_data)
    results.append(accuracy)
    
average_accuracy = np.mean(results)
print(f"Average Accuracy: {average_accuracy}")

