import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
import statistics
import numpy as np
import os
import logging
import yaml

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config.yml')
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file {config_file} not found.")
        raise
    except yaml.YAMLError as exc:
        logging.error(f"Error parsing YAML file: {exc}")
        raise

# Load datasets
def load_data(base_dir):
    try:
        data_files = {
            'Customer': 'Customer_anonymized2.csv',
            'SalesRegion': 'SalesRegion_anonymized2.csv',
            'SalesStructure': 'SalesStructure_anonymized2.csv',
            'CustomerImportance': 'CustomerImportance.csv',
            'BisnodeScore': 'BisnodeScore.csv',
            'BusinessTree': 'BusinessTree.csv',
            'OrderHeader': 'OrderHeader_anonymized.csv',
            'OrderItem': 'OrderItem_anonymized.csv'
        }
        data = {name: pd.read_csv(os.path.join(base_dir, file), sep=';' if 'Importance' in file or 'Score' in file or 'Tree' in file else ',') 
                for name, file in data_files.items()}
        return data
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}")
        raise
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

# Preprocess data
def preprocess_data(data):
    # Rename columns for clarity
    data['OrderHeader'] = data['OrderHeader'].rename(columns={"Discount": "DiscountOrderHeader", "Created": "CreatedOrderHeader"})
    data['OrderItem'] = data['OrderItem'].rename(columns={"Discount": "DiscountOrderItem", "Created": "CreatedOrderItem"})
    
    # Convert numeric columns from string to float
    for col in ['OrderValueLocalCurrency', 'OrderTotalDiscountLocalCurrency', 'OrderTotalChargeLocalCurrency']:
        data['OrderHeader'][col] = data['OrderHeader'][col].str.replace(',', '.').astype(float)
    data['OrderHeader']['CreatedOrderHeader'] = pd.to_datetime(data['OrderHeader']['CreatedOrderHeader']).astype('int64') / 10**9
    
    for col in ['ItemCount', 'ItemLPriceLocalCurrency', 'ItemSalesPriceLocalCurrency', 'ItemChargeLocalCurrency', 'DiscountOrderItem', 'SystemDiscount']:
        data['OrderItem'][col] = data['OrderItem'][col].str.replace(',', '.').astype(float)
    
    # Merge datasets
    df_merge = pd.merge(data['SalesStructure'], data['SalesRegion'], how='left', on='SalesRegionId')
    df_merge = pd.merge(data['Customer'], df_merge, how='left', on='SalesDistrictId')
    df_merge = pd.merge(df_merge, data['CustomerImportance'], how='left', left_on='CustomerImportanceId', right_on='ImportanceId')
    df_merge = pd.merge(df_merge, data['BisnodeScore'], how='left', on='BisnodeScore')
    df_merge = pd.merge(data['OrderHeader'], df_merge, how='inner', on='CustomerId')
    df_merge = pd.merge(data['OrderItem'], df_merge, how='inner', on='OrderId')
    df_merge = pd.merge(df_merge, data['BusinessTree'], how='left', left_on=['PckBusinessTreeId', 'BusinessYearEnd'], right_on=['BusinessTreeId', 'BusinessYearEnd'])
    
    # Clean data
    df_clean = df_merge.dropna(subset=['OrderId'])
    df_clean = df_clean.drop(df_clean[(df_clean['OrderValueLocalCurrency'] - df_clean['OrderTotalDiscountLocalCurrency'] - df_clean['OrderTotalChargeLocalCurrency']) < 0].index)
    df_clean = df_clean.dropna(subset=['DiscountOrderItem'])
    
    # Drop unnecessary columns
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
    
    return df_clean

# Prepare data without data leak
def data_prep_without_data_leak(X_df, y_df):
    columns_to_fill = ['SalesRegionId', 'CustomerBranch', 'Importance', 'SalesDistrictId', 'BisnodeScore']
    for column in columns_to_fill:
        X_df.loc[:, column] = X_df[column].fillna(X_df[column].mode()[0])

    columns_to_encode = ['SalesRegionId', 'CustomerBranch', 'Importance']
    one_hot_encoder = OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore')
    X_train_encoded = one_hot_encoder.fit_transform(X_df[columns_to_encode])
    X_train_encoded_df = pd.DataFrame(X_train_encoded, columns=one_hot_encoder.get_feature_names_out(columns_to_encode))
    X_df = X_df.drop(columns=columns_to_encode, axis=1)
    X_df.reset_index(inplace=True)
    X_df = pd.concat([X_df, X_train_encoded_df], axis=1)

    columns_to_target_encode = ['SalesDistrictId']
    target_encoder = TargetEncoder()
    X_target_encoded = target_encoder.fit_transform(X_df[columns_to_target_encode], y_df)
    X_target_encoded_df = pd.DataFrame(X_target_encoded, columns=target_encoder.get_feature_names_out(columns_to_target_encode))
    X_df = X_df.drop(columns=columns_to_target_encode, axis=1)
    X_df = pd.concat([X_df, X_target_encoded_df], axis=1)

    return X_df

# Train and evaluate model
def train_evaluate_model(X_train_val, y_train_val, tscv, param_dist):
    model = GradientBoostingRegressor()
    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=50, cv=tscv, verbose=2, n_jobs=-1, random_state=42)
    X_train_prepped = data_prep_without_data_leak(X_train_val, y_train_val)
    random_search.fit(X_train_prepped, y_train_val)

    best_model = random_search.best_estimator_
    logging.info(f'Best model found: {best_model}')
    
    mse_collection = []
    r2_collection = []

    for train_index, validation_index in tscv.split(X_train_val):
        X_train, X_val = X_train_val.iloc[train_index, :], X_train_val.iloc[validation_index, :]
        y_train, y_val = y_train_val.iloc[train_index], y_train_val.iloc[validation_index]

        X_train = data_prep_without_data_leak(X_train, y_train)
        X_val = data_prep_without_data_leak(X_val, y_val)

        X_train = X_train.reindex(sorted(X_train.columns), axis=1)
        X_val = X_val.reindex(sorted(X_val.columns), axis=1)

        best_model.fit(X_train, y_train)
        
        y_pred = best_model.predict(X_val)
        
        mse = mean_squared_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)
        logging.info(f'Mean Squared Error: {mse}')
        logging.info(f'R-squared: {r2}')
        mse_collection.append(mse)
        r2_collection.append(r2)

    logging.info(f'Average Mean Squared Error: {statistics.mean(mse_collection)}')
    logging.info(f'Average R-squared: {statistics.mean(r2_collection)}')

# Main function
def main():
    try:
        config = load_config()
        base_dir = config['data_directory']
        data = load_data(base_dir)
        df_clean = preprocess_data(data)
        
        # Split data into train-test sets using TimeSeriesSplit
        df_clean.set_index('CreatedOrderHeader', inplace=True)
        df_clean.sort_index(inplace=True)
        X = df_clean.drop(['DiscountOrderItem'], axis=1)
        y = df_clean['DiscountOrderItem']

        tscv2splits = TimeSeriesSplit(n_splits=2)
        for train_val_index, test_index in tscv2splits.split(X):
            X_train_val, X_test = X.iloc[train_val_index, :], X.iloc[test_index, :]
            y_train_val, y_test = y.iloc[train_val_index], y.iloc[test_index]

        tscv = TimeSeriesSplit(n_splits=5)
        param_dist = config['param_dist']
        train_evaluate_model(X_train_val, y_train_val, tscv, param_dist)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
