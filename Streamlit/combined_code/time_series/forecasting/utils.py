import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm

from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

from metrics import evaluate


import warnings
warnings.filterwarnings("ignore")


def sidebar(options):
    with st.sidebar:
        genre = st.radio(
            "Choose your model",
            options,
            index=None,
        )
        return genre


def upload_file(file_name):
    file = st.file_uploader(f"Choose the {file_name}", type="csv")
    no_header = st.checkbox("Check it if the dataset doesn't have the header row", value=False)

    if file is not None:
        if no_header:
            df = pd.read_csv(file, header=None)
            df.columns = [f'Column{index}' for index in df.columns]
        else:
            df = pd.read_csv(file)

        return df


def plot_predict(test, pred, label):
    fig, ax = plt.subplots()
    ax.plot(test, label='Original')
    ax.plot(pred, color='red', label=label)
    ax.legend()
    st.pyplot(fig)


def AR_model(X, index, resultsDict, predictionsDict):
    X_training = X[:index]
    X_test = X[index:]

    # Walk throught the test data, training and predicting 1 day ahead for all the test data
    yhat = list()

    for t in tqdm(range(len(X_test))):
        temp_train = X[:len(X_training) + t]
        model = AutoReg(temp_train, 1)
        model_fit = model.fit()
        predictions = model_fit.predict(
            start=len(temp_train), end=len(temp_train), dynamic=False)
        yhat = yhat + [predictions]

    yhat = pd.concat(yhat)
    resultsDict['AR'] = evaluate(X_test, yhat.values)
    predictionsDict['AR'] = yhat.values

    plot_predict(X_test.values, yhat.values, 'AR predicted')


def MA_model(X, index, resultsDict, predictionsDict):
    # MA example
    X_training = X[:index]
    X_test = X[index:]

    yhat = list()
    for t in tqdm(range(len(X_test))):
        temp_train = X[:len(X_training) + t]
        model = ARIMA(temp_train, order=(0, 0, 1))
        model_fit = model.fit()
        predictions = model_fit.predict(
            start=len(temp_train), end=len(temp_train), dynamic=False)
        yhat = yhat + [predictions]

    yhat = pd.concat(yhat)
    resultsDict['MA'] = evaluate(X_test, yhat.values)
    predictionsDict['MA'] = yhat.values

    plot_predict(X_test.values, yhat.values, 'MA predicted')


def ARMA_model(X, index, resultsDict, predictionsDict):
    X_training = X[:index]
    X_test = X[index:]

    yhat = list()
    for t in tqdm(range(len(X_test))):
        temp_train = X[:len(X_training) + t]
        model = ARIMA(temp_train, order=(1, 0, 1))
        model_fit = model.fit()
        predictions = model_fit.predict(
            start=len(temp_train), end=len(temp_train), dynamic=False)
        yhat = yhat + [predictions]

    yhat = pd.concat(yhat)
    resultsDict['ARMA'] = evaluate(X_test, yhat.values)
    predictionsDict['ARMA'] = yhat.values

    plot_predict(X_test.values, yhat.values, 'ARMA predicted')


def ARIMA_model(X, index, resultsDict, predictionsDict):
    X_training = X[:index]
    X_test = X[index:]

    yhat = list()
    for t in tqdm(range(len(X_test))):
        temp_train = X[:len(X_training) + t]
        model = ARIMA(temp_train, order=(1, 0, 0))
        model_fit = model.fit()
        predictions = model_fit.predict(
            start=len(temp_train), end=len(temp_train), dynamic=False)
        yhat = yhat + [predictions]

    yhat = pd.concat(yhat)
    resultsDict['ARIMA'] = evaluate(X_test, yhat.values)
    predictionsDict['ARIMA'] = yhat.values

    plot_predict(X_test.values, yhat.values, 'ARIMA predicted')


def SARIMA_model(X, index, resultsDict, predictionsDict):
    X_training = X[:index]
    X_test = X[index:]

    yhat = list()
    for t in tqdm(range(len(X_test))):
        temp_train = X[:len(X_training) + t]
        model = SARIMAX(temp_train, order=(
            1, 0, 0), seasonal_order=(0, 0, 0, 3))
        model_fit = model.fit(disp=False)
        predictions = model_fit.predict(
            start=len(temp_train), end=len(temp_train), dynamic=False)
        yhat = yhat + [predictions]

    yhat = pd.concat(yhat)
    resultsDict['SARIMAX'] = evaluate(X_test, yhat.values)
    predictionsDict['SARIMAX'] = yhat.values

    plot_predict(X_test.values, yhat.values, 'SARIMAX')
