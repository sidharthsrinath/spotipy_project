import tensorflow as tf
import keras
import pandas as pd 
import functions
import os

def read_df(filename):
    return pd.DataFrame(pd.read_csv(filename)) #dataframe based on the csv file it reads

