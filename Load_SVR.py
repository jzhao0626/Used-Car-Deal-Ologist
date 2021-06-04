import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
import joblib


def submit_model(vehicle_as_dict):
    vehicle = pd.Series(vehicle_as_dict)
    # load the model from disk
    model = joblib.load("Used_Car_Price_Model_SVR.pkl")
    result = model.predict(vehicle)
    print("RESULT: ", result, flush=True)
    return result
