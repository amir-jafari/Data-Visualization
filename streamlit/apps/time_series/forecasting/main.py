"""
Time-series forecasting -- fit a classical model to a series and predict ahead.

What it shows:
    * stationarity: the ADF test, differencing, and seasonal decomposition
    * ACF/PACF plots, which are how you *choose* the model's orders
    * the family of models, each adding one idea to the last:

        AR    -- today is a linear combination of previous values
        MA    -- today is a linear combination of previous *errors*
        ARMA  -- both of the above
        ARIMA -- ARMA plus differencing, for a series that drifts
        SARIMA-- ARIMA plus a seasonal cycle

Data: browsed from S3 (data/time_series/forecasting), or generated, or uploaded.

    streamlit run streamlit/apps/time_series/forecasting/main.py
"""

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

    # The sample air_pollution.csv now lives in S3 and is offered by the picker above:
    #   s3://dats-dl/ajafari@gwu.edu/streamlit/data/time_series/forecasting/air_pollution.csv

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
        st.markdown(
            '''
            **Annual Data (Yearly Cycle):**
            - For yearly observations showing annual seasonality, set `period=1`.
    
            **Quarterly Data:**
            - For quarterly observations, use `period=4` (4 quarters in a year).
    
            **Monthly Data:**
            - Commonly, `period=12` for monthly data (12 months in a year).
    
            **Weekly Data:**
            - For weekly data, `period=52` is suitable (around 52 weeks in a year).
    
            **Daily Data:**
            - With weekly seasonality in daily data, use `period=7` (7 days in a week).
            - For annual seasonality in daily data, `period=365` (or `366` for leap years).
    
            **Hourly Data:**
            - `period=24` for daily cycles in hourly data.
            - `period=24*7` for weekly cycles.
    
            **Custom Period:**
            - The period can be any integer representing the seasonal cycle. For example, for 10-minute intervals with a daily pattern, `period=24*6` (144 intervals per day).
            ''',
            unsafe_allow_html=True
        )

    # plt.figure(num=None, figsize=(50, 20), dpi=80, facecolor='w', edgecolor='k')
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

    radio = st.slider('Choose the radio of the train test split', 0.10, 0.50, 0.25)

    if not model_name:
        st.warning("***Pick up the model from the left side bar***")
        st.stop()

    resultsDict = {}
    predictionsDict = {}

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
