import pandas as pd
from db_connect import connection 
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class Preprocessing:
    def __init__(self):
        self.con= connection()
        
    

    def Data_fetch(self, query):
        
        self.con.execute(query)
        data= self.con.fetchall()              
        return data

    def processing(self):
        
        query= """SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, 
            trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, 
            payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, 
            improvement_surcharge, total_amount, congestion_surcharge, airport_fee from yellow_taxi_data;"""
        data= self.Data_fetch(query)
        column_names = [
        'VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 
        'trip_distance', 'RatecodeID', 'store_and_fwd_flag', 'PULocationID', 'DOLocationID', 
        'payment_type', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 
        'improvement_surcharge', 'total_amount', 'congestion_surcharge', 'airport_fee'
        ]
        
        data=pd.DataFrame(data, columns=column_names)
        # print('this is converted dataframe',data)
        data = data.dropna(subset=['passenger_count', 'trip_distance', 'fare_amount'])
        data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])
        data['tpep_dropoff_datetime'] = pd.to_datetime(data['tpep_dropoff_datetime'])
        data['trip_duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds() / 60
        columns_to_use = [
        'VendorID', 'passenger_count', 'trip_distance', 'RatecodeID', 
        'PULocationID', 'DOLocationID', 'fare_amount', 'extra', 
        'mta_tax', 'congestion_surcharge', 'trip_duration'  
        ]
        df = data[columns_to_use]

        encoder= OneHotEncoder()
        rate_encoded = encoder.fit_transform(df[['RatecodeID']])
# Convert into dense matrix as Onehotencoding produces sparse mmatrix
        rate_encoded= rate_encoded.toarray()
        rate_encoded_columns = encoder.get_feature_names_out(['RatecodeID'])
        vendor_encoded = encoder.fit_transform(df[['VendorID']])
        vendor_encoded=vendor_encoded.toarray()

        vendor_encoded_columns = encoder.get_feature_names_out(['VendorID'])

        rate_encoded_df = pd.DataFrame(rate_encoded, columns=rate_encoded_columns)
        vendor_encoded_df = pd.DataFrame(vendor_encoded, columns=vendor_encoded_columns)
        df= pd.concat([df,rate_encoded_df,vendor_encoded_df], axis=1)
        return df 

    def Spliting_data(self):
        process=self.processing()
        X = process.drop(columns=['trip_duration'])  # All columns except the target
        y = process['trip_duration']  # The target variable
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        return X_train_scaled,y_train,X_test_scaled,y_test
    






        





