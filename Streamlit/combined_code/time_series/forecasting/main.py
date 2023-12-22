# auto regressive model, run AI, ARIMA model.

# And these models are available in the stats model. Okay, just one line. Yes. And you will get the predictions, okay. And you have the code for the predictions in basic plots, and then auto correlation and partial correlation. So this is called autocorrelation auto CFN. pcf.

# So I just use you pass this series and show the autocorrelation function, okay. And, for this one, generate random numbers. So you can generate for example, normal distribution or pass or someone upload the data so give them option.

'''
AR (Autoregressive Model): Models the current value as a linear combination of its previous values.

MA (Moving Average Model): Models the current value as a linear combination of the current and past error terms.

ARMA (Autoregressive Moving Average Model): Combines both AR and MA models.

ARIMA (Autoregressive Integrated Moving Average Model): Extends ARMA to include differencing of the data, useful for non-stationary time series.

SARIMA (Seasonal ARIMA): Extends ARIMA to account for seasonality in data.
'''

import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller

from statsmodels.tsa.seasonal import seasonal_decompose


import utils


def main():
    options_dic = {
        "Autoregression (AR)": 1,
        "Moving Average (MA)": 2,
        "Autoregressive Moving Average (ARMA)": 3,
        "Autoregressive integrated moving average (ARIMA)": 4,
        "Seasonal Autoregressive Integrated Moving-Average (SARIMA)": 5,
    }
    model_name = utils.sidebar(options_dic.keys())

    st.header("Model Forecasting")
    st.divider()
    st.subheader("Step 1: Get time series data")

    genre = st.radio(
        "Choose a method to get data",
        ["upload a csv file", "generate random data"],
    )

    if genre == 'upload a csv file':
        data = utils.upload_file("CSV data file")
    else:
        num_points = st.slider('Choose the number of generated data', 10, 800, 730)

        date_range = pd.date_range(start='1/1/2023', periods=num_points, freq='D')
        value = np.random.randn(num_points)

        # # Generate a trend (gradually increasing)
        # trend = np.linspace(start=1, stop=10, num=num_points)
        #
        # # Generate seasonal data (e.g., sinusoidal pattern to mimic yearly seasonality)
        # seasonality = 10 + np.sin(np.linspace(start=0, stop=2 * np.pi, num=num_points)) * 2
        #
        # # Generate some positive random noise
        # noise = np.random.rand(num_points) * 2
        #
        # # Combine trend, seasonality and noise
        # value = trend + seasonality + noise

        # Ensure all data is positive (should already be the case with this construction)
        value = np.abs(value)

        data = pd.DataFrame({'Date': date_range, 'Value': value})

    if data is None:
        st.stop()

    # data = pd.read_csv('/Users/xiaoqi/PycharmProjects/Data-Visualization/Streamlit/combined_code/time_series/forecasting/air_pollution.csv', parse_dates=['date'])
    # data.set_index('date', inplace=True)
    # st.write(data.head())

    index_column = st.selectbox(
        'Choose the index column of date information',
        data.columns,
    )
    data.set_index(index_column, inplace=True)

    X_column = st.selectbox(
        'Choose the column that need to predict',
        [col for col in data.columns if col != index_column],
    )

    st.write(data.head())

    st.divider()
    st.subheader("Step 2: Decompose the time series")

    period = st.slider('Choose the period of seasonal_decompose', 1, 500, 365)
    with st.expander("See the instructions of **period** choosing"):
        st.write(
            '''
            If your data has yearly observations and shows annual seasonality, set period=1. \n
            For data with quarterly observations, period=4 (since there are 4 quarters in a year). \n
            For monthly data, period=12 is common, as there are 12 months in a year. \n
            Use period=52 for weekly data, considering there are approximately 52 weeks in a year. \n
            If the data exhibits weekly seasonality, period=7 (7 days in a week). \n
            For daily data with annual seasonality (like daily temperatures over several years), period=365 (or 366 for leap years). \n
            If you have hourly data with a daily cycle, period=24. \n
            For hourly data with a weekly cycle, period=24*7.
            '''
        )

    plt.figure(num=None, figsize=(50, 20), dpi=80, facecolor='w', edgecolor='k')
    series = data[X_column]

    # st.write(series)
    result = seasonal_decompose(series, model='multiplicative', period=period)
    fig = result.plot()
    st.pyplot(fig)

    st.write('Augmented Dickey-Fuller test')
    X = data[X_column].values
    result = adfuller(X)
    st.write('ADF Statistic: %f' % result[0])
    st.write('p-value: %f' % result[1])
    st.write('Critical Values:')
    for key, value in result[4].items():
        st.write('\t%s: %.3f' % (key, value))


    st.divider()
    st.subheader("Step 3: Methods for time series forecasting")

    if not model_name:
        st.warning("***Pick up the model from the left side bar***")
        st.stop()

    resultsDict = {}
    predictionsDict = {}

    radio = 0.2
    index = int((1-radio) * len(X))

    model_index = options_dic[model_name]

    if model_index == 1:
        utils.AR_model(data[X_column], index, resultsDict, predictionsDict)
    elif model_index == 2:
        utils.MA_model(data[X_column], index, resultsDict, predictionsDict)
    elif model_index == 3:
        utils.ARMA_model(data[X_column], index, resultsDict, predictionsDict)
    elif model_index == 4:
        utils.ARIMA_model(data[X_column], index, resultsDict, predictionsDict)
    elif model_index == 5:
        utils.SARIMA_model(data[X_column], index, resultsDict, predictionsDict)

    # bar_metrics(resultsDict)
    st.stop()


if __name__ == "__main__":
    main()
