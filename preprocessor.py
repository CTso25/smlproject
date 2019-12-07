import pandas as pd
import numpy as np
from sklearn import linear_model as lin_model, preprocessing
from sklearn.model_selection import train_test_split

# read in data and drop unnamed, start/end date columns
renfedata = pd.read_csv("input/cleaned_data.csv")

# keeping sample data in here for easy processing/debugging --> to remove later
renfedata = renfedata.sample(n=50000, random_state=1)

renfedata = renfedata.drop(columns=['Unnamed: 0','start_date', 'end_date'], axis=1)

# sort data by insert data ascending to get have records in chronological order for train/test split
renfedata = renfedata.sort_values('insert_date')

# function to return train, test splits of data for direct use in modeling
def prepare_data():
    # Define explanatory variables (features) and response variable (price)
    features = renfedata.drop(columns=['price'], axis=1)
    response = renfedata[['price']]

    # split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, response, train_size=0.75, shuffle=False)

    # verify that training and testing are separated in time correctly
    print('Train data(range):')
    print(X_train['insert_date'].min())
    print(X_train['insert_date'].max())
    print('Test data(range):')
    print(X_test['insert_date'].min())
    print(X_test['insert_date'].max())

    # remove time stamps once data has been split correctly
    X_train = X_train.drop(columns=['insert_date'], axis=1)
    X_test = X_test.drop(columns=['insert_date'], axis=1)

    # standardize X_train and X_test
    std_scaler = preprocessing.StandardScaler().fit(X_train)
    X_train_scaled = std_scaler.transform(X_train)
    X_test_scaled = std_scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test


# function to return all features in a list
def get_features():
    features = renfedata.drop(columns=['price', 'insert_date'], axis=1)
    return list(features.columns)


# function to compute upper bound for response variable
def get_upper_bounds(y, percent):
    float_percent = percent/100
    upper_bound = y + (y * float_percent)
    return upper_bound


# function to compute lower bound for response variable
def get_lower_bounds(y, percent):
    float_percent = percent/100
    lower_bound = y - (y * float_percent)
    return lower_bound