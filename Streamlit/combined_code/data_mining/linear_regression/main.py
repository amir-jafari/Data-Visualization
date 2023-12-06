import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm


def main():
    st.header("Linear Regression")
    st.divider()
    st.subheader("Step 1: Generate X and Y Data")

    distribution = st.radio(
        "Choose the distribution of X",
        ["Normal Distribution", "Uniform Distribution", "Gamma Distribution"],
        index=1,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        size = st.slider('Number of values', 1, 10000, 1000)

    if distribution == "Normal Distribution":
        with col2:
            mean = st.slider('The mean of x', -50, 50, 5)
        with col3:
            std = st.slider('The STD of x', 0, 50, 2)

        x = np.random.normal(mean, std, size)
    elif distribution == "Uniform Distribution":
        with col2:
            low = st.slider('The lower boundary', -100, 100, -10)
        with col3:
            high = st.slider('The upper boundary', -100, 100, 10)

        x = np.random.uniform(low, high, size)  # uniform_distribution
    else:
        with col2:
            shape = st.slider('k parameter', 0, 50, 2)
        with col3:
            scale = st.slider('θ parameter', 0, 50, 1)

        x = np.random.gamma(shape, scale, size) # gamma_distribution

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.hist(x, bins=30, alpha=0.7, color='blue')
    ax.set_title(f'Histogram of {distribution} of X Value')
    ax.set_xlabel('Value')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    st.write('##')
    st.write('***Change slope and intercept to generate Y data***')
    col4, col5, col6 = st.columns(3)

    with col4:
        slope = st.slider('The slope between x and y', -20, 20, 2)
    with col5:
        intercept = st.slider('The intercept between x and y', -50, 50, 0)
    with col6:
        error_std = st.slider('The STD of the error term', 0, 20, 2)

    error = np.random.normal(0, error_std, size)
    y = slope * x + intercept + error  # Add a linear relationship

    col7, col8 = st.columns(2)

    with col7:
        fig2, ax2 = plt.subplots()
        ax2.scatter(x, y, c='b', marker='.')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('X and Y dataset')
        st.pyplot(fig2)
    with col8:
        fig, ax = plt.subplots()
        ax.hist(error, bins=30, alpha=0.7, color='blue')
        ax.set_title(f'Histogram of error term')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    st.divider()
    st.subheader("Step 2: Get the result")

    test_size = 0.2

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=1)
    reg = LinearRegression().fit(X_train, y_train)

    st.write(f'The train-test split ratio is set to {test_size*100:.1f}%')
    st.write(f'For train dataset, The ***slope*** is  {round(reg.coef_[0][0], 2)}, and the ***intercept*** is {round(reg.intercept_[0], 2)}')

    y_pred = reg.predict(X_test)
    MSE = mean_squared_error(y_pred, y_test)
    st.write(f'For test dataset, ***Mean Squared Error (MSE)*** is: {MSE:.2f}, ***reg.score(X_train, y_train)*** is: {reg.score(X_train, y_train):.2f}')

    # Fit the regression model on training data
    model = sm.OLS(y_train, sm.add_constant(X_train)).fit()

    st.write('The summary of the regression model based on train dataset:')
    st.write(model.summary())

    st.divider()
    st.subheader("Step 3: Plot the results")

    fig2, ax2 = plt.subplots()
    ax2.scatter(X_train, y_train, c='r', marker='.', label='Train')
    ax2.plot(X_test, y_pred, c='g', marker='x', label='Prediction')
    ax2.legend(loc='lower right')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title('Regression')
    st.pyplot(fig2)

    residuals = y_test - y_pred

    fig3, ax3 = plt.subplots()
    ax3.scatter(X_test, residuals)
    ax3.hlines(y=0, xmin=X_test.min(), xmax=X_test.max(), linestyles='dashed')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Residuals')
    ax3.set_title('Error Residuals between test Y and predicted Y')
    st.pyplot(fig3)


if __name__ == "__main__":
    main()
