import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler



def split_data(df, strat_by, rand_st=123):
    '''
    Takes in: a pd.DataFrame()
          and a column to stratify by  ;dtype(str)
          and a random state           ;if no random state is specifed defaults to [123]
          
      return: train, validate, test    ;subset dataframes
    '''
    # split the training and validation data off from the test data
    # the test data will be .2 of the dataset
    train, test = train_test_split(df, test_size=.2, 
                               random_state=rand_st, stratify=df[strat_by])
    train, validate = train_test_split(train, test_size=.25, 
                 random_state=rand_st, stratify=train[strat_by])
    print(f'Prepared df: {df.shape}')
    print()
    print(f'Train: {train.shape}')
    print(f'Validate: {validate.shape}')
    print(f'Test: {test.shape}')


    return train, validate, test

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<  X_y_split  >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def X_y_split(dataframe:pd.DataFrame, target:str):
    '''
    Takes in a DataFrame and the name of the target column to split from the data

    Returns an X_frame with all the feature data
    and     a y_array with the target values
    '''
    # Get all the columns in the dataframe and cast as a list
    X_cols = dataframe.columns.to_list()
    # remove the target column name from the list
    X_cols.remove(target)
    # set the X_frame as the dataframe with the list of feature columns
    X_frame = dataframe[X_cols]
    # set the y_array as the target column
    y_array = dataframe[target]

    return X_frame, y_array


#~~~~~~~~~~~~~~~~~~~~~~~~~<  get_dummies  >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def get_dummies(X_train: pd.DataFrame, X_validate: pd.DataFrame, X_test: pd.DataFrame):
    cols_list, drops = [], []

    for x in X_train:
        if X_train[x].values.dtype != 'O':
            continue
        else:
            cols_list.append(x)
            y = X_train[x].value_counts()[-1:].index.to_list()[0]
            x = ''.join([x, '_', y])
            drops.append(x)
# So... dropping class_2seater caused an issue 
    # drops.remove('class_2seater')
    
    X_train = pd.get_dummies(X_train).drop(columns= drops)
    X_validate = pd.get_dummies(X_validate)
    X_test = pd.get_dummies(X_test)

    for i in drops:
        if i in X_validate: 
            X_validate = X_validate.drop(columns= i)
        if i in X_test:
            X_test = X_test.drop(columns= i)
    
    for x in X_train:
        # print(x)
        if x not in X_validate.columns:
            X_validate[x] = np.zeros(shape= len(X_validate))
            print(f'added column= \'{x}\' to validate, full of zeros')
        if x not in X_test.columns:
            X_test[x] = np.zeros(shape= len(X_test))
            print(f'added column= \'{x}\' to test, full of zeros')

    print(f'X_train {X_train.shape}, X_validate {X_validate.shape}, X_test {X_test.shape}')

    return X_train, X_validate, X_test


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<  SCALE_DATA  >~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def scale_data(train, validate, test):
    '''
    scales the data using MinMaxScaler from SKlearn
    should only be the X_train, X_validate, and X_test
    '''
#     Remember incoming columns and index numbers to output DataFrames
    cols = train.columns
    train_index = train.index
    validate_index = validate.index
    test_index = test.index
    
#     Make the scaler
    scaler = MinMaxScaler()
    
#     Use the scaler
    train = scaler.fit_transform(train)
    validate = scaler.transform(validate)
    test = scaler.transform(test)
    
#     Reset the transformed datasets into DataFrames
    train = pd.DataFrame(train, columns= cols, index= train_index)

    validate = pd.DataFrame(validate, columns= cols, index= validate_index)

    test = pd.DataFrame(test, columns= cols, index= test_index)
    
    return train, validate, test
