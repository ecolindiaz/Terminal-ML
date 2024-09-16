
import pandas as pd
from pandas import json_normalize
import numpy as np
import glob
import os
import json
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

directories = ['C:/Users/emawe/OneDrive/Documents/C1GamesStarterKit-master/scripts/batch_0']

big_dfs = []


# Function to process a single file
def process_file(file):
    print(f"Processing file: {file}")
    with open(file) as f:
        try:
            json_big_data = json.load(f)

            # Collect data items
            for data in json_big_data[1:]:

                for key, value in data.items():
                    df = pd.DataFrame({key: [value] if not isinstance(value, list) else [str(value)]})
                    big_dfs.append(df)

        except Exception as e:
            print(f"Error processing file {file}: {e}")


# Process each directory
for directory in directories:
    print(f"Processing directory: {directory}")
    for file in glob.glob(os.path.join(directory, '*.json')):
        process_file(file)

# Convert the collected data items to a DataFrame
big_df = pd.concat(big_dfs, ignore_index=True)
big_df = big_df.reset_index(drop=True)



print(big_df.head())



'''with open('C:/Users/emawe/OneDrive/Documents/C1GamesStarterKit-master/algov1-4-3/replays.json') as json_file:
    json_data = json.load(json_file)
dfs = []
for data in json_data[1:]:

    data = data[1:]

    for item in data:
        for key, value in item.items():
            df = pd.DataFrame({key: [value] if not isinstance(value, list) else [str(value)]})
            dfs.append(df)

directory = 'path/to/json/files'

big_df = pd.DataFrame()

for file in glob.glob(directory + '/*.json'):
    json = pd.read_json(file)

    for data in json[1:]:


    big_df = pd.concat([big_df, df], ignore_index=True)


df = pd.concat(dfs, axis=0, ignore_index=True)
df = df.reset_index(drop=True)

print(df.columns)

print(df['endStats'])

non_nan_indices = df[~df['endStats'].isna()].index.tolist()

print(non_nan_indices)

print(len(df))

print(df.head(1723))


data = {
    'p2Units': [],
    'p1Units': [],
    'endStats': []
}

endStats_array = np.array([df['endStats'].iloc[index] for index in non_nan_indices])

data['p2Units'].append(df.loc[6, 'p2Units'])
data['p1Units'].append(df.loc[9, 'p1Units'])
data['endStats'].append(endStats_array[0])

for index in non_nan_indices:
    if index + 13 < len(df):
        data['p2Units'].append(df.loc[index + 10, 'p2Units'])
        data['p1Units'].append(df.loc[index + 13, 'p1Units'])
        data['endStats'].append(endStats_array[1:])

match_data = pd.DataFrame(data)

print(new_df.head())


X = match_data
y = match_data

rf = RandomForestClassifier()



X = features
y = df[['p1Units', 'p2Units']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)


'''