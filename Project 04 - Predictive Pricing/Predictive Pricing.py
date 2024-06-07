import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
import statistics
import numpy as np
import os

# Load datasets
base_dir = os.path.dirname(os.path.abspath(__file__))
df_Customer = pd.read_csv(os.path.join(base_dir, 'Customer_anonymized2.csv'))
df_SalesRegion = pd.read_csv(os.path.join(base_dir, 'SalesRegion_anonymized2.csv'))
df_SalesStructure = pd.read_csv(os.path.join(base_dir, 'SalesStructure_anonymized2.csv'))
df_CustomerImportance = pd.read_csv(os.path.join(base_dir, 'CustomerImportance.csv'), sep=';')
df_BisnodeScore = pd.read_csv(os.path.join(base_dir, 'BisnodeScore.csv'), sep=';')
df_BusinessTree = pd.read_csv(os.path.join(base_dir, 'BusinessTree.csv'), sep=';')
df_OrderHeader = pd.read_csv(os.path.join(base_dir, 'OrderHeader_anonymized.csv'))
df_OrderItem = pd.read_csv(os.path.join(base_dir, 'OrderItem_anonymized.csv'))

# Rename columns in order header and order item datasets for clarity
df_OrderHeader = df_OrderHeader.rename(columns={"Discount": "DiscountOrderHeader", "Created": "CreatedOrderHeader"})
df_OrderItem = df_OrderItem.rename(columns={"Discount": "DiscountOrderItem", "Created": "CreatedOrderItem"})

# Convert numeric columns from string to float
df_OrderHeader['OrderValueLocalCurrency'] = df_OrderHeader['OrderValueLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderHeader['OrderTotalDiscountLocalCurrency'] = df_OrderHeader['OrderTotalDiscountLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderHeader['OrderTotalChargeLocalCurrency'] = df_OrderHeader['OrderTotalChargeLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderHeader['CreatedOrderHeader'] = pd.to_datetime(df_OrderHeader['CreatedOrderHeader']).astype('int64') / 10**9

df_OrderItem['ItemCount'] = df_OrderItem['ItemCount'].str.replace(',', '.').astype(float)
df_OrderItem['ItemLPriceLocalCurrency'] = df_OrderItem['ItemLPriceLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderItem['ItemSalesPriceLocalCurrency'] = df_OrderItem['ItemSalesPriceLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderItem['ItemChargeLocalCurrency'] = df_OrderItem['ItemChargeLocalCurrency'].str.replace(',', '.').astype(float)
df_OrderItem['DiscountOrderItem'] = df_OrderItem['DiscountOrderItem'].str.replace(',', '.').astype(float)
df_OrderItem['SystemDiscount'] = df_OrderItem['SystemDiscount'].str.replace(',', '.').astype(float)

# Merge SalesRegion and SalesStructure
df_merge = pd.merge(df_SalesStructure, df_SalesRegion, how='left', on='SalesRegionId')

# Merge SalesStructure with Customer
df_merge = pd.merge(df_Customer, df_merge, how='left', on='SalesDistrictId')

# Merge Customer with CustomerImportance
df_merge = pd.merge(df_merge, df_CustomerImportance, how='left', left_on='CustomerImportanceId', right_on='ImportanceId')

# Merge Customer with BisnodeScore
df_merge = pd.merge(df_merge, df_BisnodeScore, how='left', on='BisnodeScore')

# Merge OrderHeader with Customer (only keep orders with a customer)
df_merge = pd.merge(df_OrderHeader, df_merge, how='inner', on='CustomerId')

# Merge OrderItem with OrderHeader (only keep items with an order)
df_merge = pd.merge(df_OrderItem, df_merge, how='inner', on='OrderId')

# Merge with BusinessTree (left join to keep all items)
df_merge = pd.merge(df_merge, df_BusinessTree, how='left', left_on=['PckBusinessTreeId', 'BusinessYearEnd'], right_on=['BusinessTreeId', 'BusinessYearEnd'])

# Clean data
df_clean = df_merge.copy()
# Remove rows with missing OrderId
df_clean = df_clean.dropna(subset=['OrderId'])
# Remove rows with negative final order price
df_clean = df_clean.drop(df_clean[(df_clean['OrderValueLocalCurrency'] - df_clean['OrderTotalDiscountLocalCurrency'] - df_clean['OrderTotalChargeLocalCurrency']) < 0].index)
# Remove rows with null target variable
df_clean = df_clean.dropna(subset=['DiscountOrderItem'])

# Drop columns that are not needed for modeling
drop_columns = [
    'EEOChargeLocalCurrency', 'CustomerName1', 'SalesDistrictName', 'SalesRegionName', 'OrderTotalDiscountLocalCurrency', 
    'ItemSalesPriceLocalCurrency', 'BusinessTreeId', 'CustomerId', 'CustomerImportanceId', 'BisnodeScoreName', 
    'BisnodeScoreDescription', 'OrderId', 'ItemPosition', 'CreatedOrderItem', 'OrderValueLocalCurrency', 
    'DiscountOrderHeader', 'OrderTotalChargeLocalCurrency', 'ResponsibleEmployee', 'SalesRepresentativeName', 
    'SystemDiscount', 'ImportanceId'
]
df_clean = df_clean.drop(drop_columns, axis=1)

# Fill NaN values with 0
df_clean['ItemCount'] = df_clean['ItemCount'].fillna(0)
df_clean['ItemChargeLocalCurrency'] = df_clean['ItemChargeLocalCurrency'].fillna(0)

# Split data into train-test sets using TimeSeriesSplit
df_split = df_clean.copy()
tscv2splits = TimeSeriesSplit(n_splits=2)
df_split.set_index('CreatedOrderHeader', inplace=True)
df_split.sort_index(inplace=True)
X = df_split.drop(['DiscountOrderItem'], axis=1)
y = df_split['DiscountOrderItem']

# Perform train-test split
for train_val_index, test_index in tscv2splits.split(X):
    X_train_val, X_test = X.iloc[train_val_index, :], X.iloc[test_index, :]
    y_train_val, y_test = y.iloc[train_val_index], y.iloc[test_index]

# Initialize TimeSeriesSplit for cross-validation
tscv = TimeSeriesSplit(n_splits=5)

def dataPrepWithoutDataLeak(X_df, y_df):
    # Fill missing values with the mode for specific columns
    columns_to_fill = ['SalesRegionId', 'CustomerBranch', 'Importance', 'SalesDistrictId', 'BisnodeScore']
    for column in columns_to_fill:
        X_df[column] = X_df[column].fillna(X_df[column].mode()[0])

    # One-hot encode categorical variables
    columns_to_encode = ['SalesRegionId', 'CustomerBranch', 'Importance']
    one_hot_encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    X_train_encoded = one_hot_encoder.fit_transform(X_df[columns_to_encode])
    X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=one_hot_encoder.get_feature_names_out(columns_to_encode))
    X_df = X_df.drop(columns=columns_to_encode, axis=1)
    X_df.reset_index(inplace=True)
    X_df = pd.concat([X_df, X_train_encoded_df], axis=1)

    # Target encode specific columns
    columns_to_target_encode = ['SalesDistrictId']
    target_encoder = TargetEncoder()
    X_target_encoded = target_encoder.fit_transform(X_df[columns_to_target_encode], y_df)
    X_target_encoded_df = pd.DataFrame(X_target_encoded, columns=target_encoder.get_feature_names_out(columns_to_target_encode))
    X_df = X_df.drop(columns=columns_to_target_encode, axis=1)
    X_df = pd.concat([X_df, X_target_encoded_df], axis=1)

    return X_df

# Initialize Gradient Boosting Regressor
model = GradientBoostingRegressor()

# Define parameter grid for RandomizedSearchCV
param_dist = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.6, 0.8, 1.0],
    'max_depth': [3, 4, 5],
    'max_features': ['auto', 'sqrt', 'log2'],
    'min_samples_split': [2, 5, 10]
}

# Perform RandomizedSearchCV to find the best hyperparameters
random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=50, cv=tscv, verbose=2, n_jobs=-1, random_state=42)
X_train_prepped = dataPrepWithoutDataLeak(X_train_val, y_train_val)
random_search.fit(X_train_prepped, y_train_val)

# Retrieve the best model and parameters
best_model = random_search.best_estimator_
print(f'Best model found: {best_model}')
best_params = random_search.best_params_
print(f'Best parameters found: {best_params}')

# Evaluate the best model using cross-validation
mse_collection = []
r2_collection = []

for train_index, validation_index in tscv.split(X_train_val):
    X_train, X_val = X_train_val.iloc[train_index, :], X_train_val.iloc[validation_index, :]
    y_train, y_val = y_train_val.iloc[train_index], y_train_val.iloc[validation_index]

    X_train = dataPrepWithoutDataLeak(X_train, y_train)
    X_val = dataPrepWithoutDataLeak(X_val, y_val)

    X_train = X_train.reindex(sorted(X_train.columns), axis=1)
    X_val = X_val.reindex(sorted(X_val.columns), axis=1)

    # Train the model
    best_model.fit(X_train, y_train)
    
    # Predict on the validation set
    y_pred = best_model.predict(X_val)
    
    # Evaluate the model performance
    mse = mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)
    print(f'Mean Squared Error: {mse}')
    print(f'R-squared: {r2}')
    mse_collection.append(mse)
    r2_collection.append(r2)

# Print average evaluation metrics
print(f'Average Mean Squared Error: {statistics.mean(mse_collection)}')
print(f'Average R-squared: {statistics.mean(r2_collection)}')