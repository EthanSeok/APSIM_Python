# 일사량 null 값 처리를 위해 linearregression

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

def main():
    output_dir = "../output/model_result"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df_G = pd.read_csv("../output/weather/Gangneung_weather.csv")
    df_S = pd.read_csv("../output/weather/Chuncheon_weather.csv")
    df = pd.concat([df_G, df_S])
    df = df[df['evap'] != 0]
    df = df.fillna(0)

    y = df['evap']
    X = df[['radn']]

    # results = sm.OLS(y, sm.add_constant(X)).fit()
    # print(results.summary())


    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)
    #
    model = LinearRegression()
    model.fit(X_train, y_train)
    #
    y_predict = model.predict(X_test)
    print(y_predict)
    print(model.coef_)
    print(model.intercept_)
    print(model.score(X_test, y_test))
    # # df_VIF = pd.DataFrame({'컬럼': column, 'VIF': variance_inflation_factor(model.X_test, i)}
    # #              for i, column in enumerate(model.X_test)
    # #              if column != 'Intercept')
    # # print(df_VIF)
    #
    score = model.score(X_test, y_test)
    mae = mean_absolute_error(y_predict, y_test)
    r2 = r2_score(y_predict, y_test)
    mse = mean_squared_error(y_predict, y_test)
    print("mse:", mse)
    print("rmse:", np.sqrt(mse))
    #
    plt.scatter(y_test, y_predict)
    plt.scatter(y_train, model.predict(X_train))
    plt.plot([0, max(y_predict)], [0, max(y_predict)])
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"Linear Regression \n "
              f"mae: {mae:.4f} | r2: {r2:.4f} \n"
              f"score: {score:.4f} | mse: {mse:.4f} | rmse: {np.sqrt(mse):.4f}")


if __name__ == '__main__':
    main()