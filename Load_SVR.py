import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
import joblib


def submit_model(vehicle_as_dict, sorted_columns, pipeline_file):
    try:
        # set the first value as a list
        for key in vehicle_as_dict:
            vehicle_as_dict[key] = [vehicle_as_dict[key]]
            break
        # create the the dataframe
        testing_vehicle = pd.DataFrame.from_dict(vehicle_as_dict, orient='columns')
        # sorting columns into order
        testing_vehicle = testing_vehicle[sorted_columns]
        # load the model from disk
        testing_pipeline = joblib.load(pipeline_file)
        vehicle_testing_results = testing_pipeline.predict(testing_vehicle)
        testing_result = round(vehicle_testing_results[0], 2)
        print("testing_result: ", testing_result, flush=True)
        return testing_result
    except Exception as e:
        print("ERROR", vehicle_as_dict, e, flush=True)
        return "error"

if __name__ == "__main__":
    submit_model(
        {'year': 2005.0,
         'condition': 3,
         'odometer': 130414.0,
         'transmission': 'automatic',
         'size': 4,
         'type': 'van',
         'state': 'ia',
         'fwd': 0,
         'rwd': 1},
        ['year', 'condition', 'odometer', 'transmission', 'size', 'type', 'state', 'fwd', 'rwd'],
        "Used_Car_Price_Pipeline_SVR.pkl"
    )
