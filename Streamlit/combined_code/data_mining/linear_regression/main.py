import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def main():
    st.header("Linear Regression")
    st.divider()
    st.subheader("Step 1: Generate X and Y Data")

    with st.echo():
        x = np.linspace(0, 10, 1000).reshape(-1, 1)
        x1 = x + np.random.rand(len(x), 1) * 10
        y = 2 * x1 + 1

    st.divider()
    st.subheader("Step 2: Get the result")

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
    reg = LinearRegression().fit(X_train, y_train)

    st.write(f'Slope is  {reg.coef_} ans intercept is {reg.intercept_}')

    # %%---------------------------------------------------------------------------------
    pred = reg.predict(X_test)
    MSE = mean_squared_error(pred, y_test)
    st.write(f'MSE: {MSE:.2f}, reg.score(X_train, y_train): {reg.score(X_train, y_train):.2f}')

    st.divider()
    st.subheader("Step 3: Plot")

    plt.scatter(x, y, c='r', marker='.')
    # plt.scatter(X_train, y_train, c = 'b', marker= 'o')
    plt.plot(X_test, pred, c='g', marker='x')
    plt.legend(('Data', 'Trian', 'Prediction'), loc='lower right')
    plt.title('Regression')
    st.pyplot(plt)


if __name__ == "__main__":
    main()
