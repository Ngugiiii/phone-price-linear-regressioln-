# -*- coding: utf-8 -*-
"""phone-price-data-cleaning-linerregression-model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wfa1l_B1YVavasmpISQ6v4d12H3mh9rw

# Import Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error , mean_absolute_percentage_error
import statsmodels.api as sm

"""# Explore Data"""

df = pd.read_csv('Mobile phone price.csv')

df

# Clean column names
df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(' ', '_')

df

df['Brand'].unique()

df['Brand'].value_counts()

model_counts = df['Model'].value_counts().reset_index().rename(columns={'index':'Model' , 'Model' : 'Count'})

model_counts

Brand_counts = df['Brand'].value_counts().reset_index().rename(columns={'index' : 'Brand' , 'Brand' : 'count'})

Brand_counts

"""# Cleaning Data"""

df['Storage'] = df['Storage'].str.replace('GB','')

df['Storage'].head(20)

df["Camera_(MP)"] = df["Camera_(MP)"].str.replace("MP","")
df["Camera_(MP)"] = df["Camera_(MP)"].str.replace("D","")

df["Camera_(MP)"] = df["Camera_(MP)"].str.split("+")

listx = []
for i in df.index:
    listx.append(df["Camera_(MP)"][i][0])

df["Camera_(MP)"] = listx

df["Camera_(MP)"] = df["Camera_(MP)"].astype("float64")

df['RAM'] = df['RAM'].str.replace('GB','')

df['RAM'].head(20)

df['Price_($)'] = df['Price_($)'].str.replace('$','')

df['Price_($)'].head(20)

df['Screen_Size_(inches)'].unique()

df = df[~(df["Screen_Size_(inches)"] == "6.8 + 3.9")]

df = df[~(df["Screen_Size_(inches)"] == "7.6 (unfolded)")]

df["Screen_Size_(inches)"] = df["Screen_Size_(inches)"].astype("float64")

df['Price_($)'] = pd.to_numeric(df['Price_($)'] , errors='coerce')

df['Storage'] = pd.to_numeric(df['Storage'] , errors='coerce')

df['RAM'] = pd.to_numeric(df['RAM'] , errors='coerce')

df.info()

df.describe().T.style.background_gradient(cmap="Blues")

df.describe(include="O").T

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates(inplace=True)

df.duplicated().any()

df.shape

Mean_Price = df['Price_($)'].mean()

df['Price_($)'] = df['Price_($)'].fillna(Mean_Price)

df['Price_($)'].isnull().sum()

"""# Visualiztion"""

plt.figure(figsize=(12,10))
sns.heatmap(df.corr(), annot=True, linewidths=.5)

plt.figure(figsize=(12,10))
sns.boxplot(x="Battery_Capacity_(mAh)", y="Brand", data=df)

plt.figure(figsize=(12,8))
sns.set_style("darkgrid")
sns.scatterplot(data=df,x="Brand",y="Price_($)",hue="Screen_Size_(inches)")
plt.title("[Price vs Brand] by Screen Size")

plt.figure(figsize=(10, 8))
sns.histplot(data=df['Price_($)'], kde=True , color="Red")
plt.title('Price Distribution Chart')
plt.show()

"""# Encoding"""

df.columns

le = LabelEncoder()

Brand = LabelEncoder()
Model = LabelEncoder()

df['Brand'].value_counts()

df['Brand'] = Brand.fit_transform(df['Brand'])

df['Brand'].value_counts()

Brand.classes_

df['Model'].value_counts()

df['Model'] = Model.fit_transform(df['Model'])

df['Model'].value_counts()

"""# Split Data"""

X = df.drop('Price_($)', axis=1)
y = df['Price_($)']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

df.shape

X_train.shape

X_test.shape

"""# Data Scaling using Robust Scaler"""

ro_scaler = RobustScaler()
x_train = ro_scaler.fit_transform(X_train)
x_test = ro_scaler.fit_transform(X_test)

x_train.shape

"""# Linear Regression"""

lin = LinearRegression()

lin.fit(X_train,y_train)

lin.score(X_train,y_train)

lin.score(X_test , y_test)

lin.coef_

lin.intercept_

pd.DataFrame(lin.coef_ , df.columns[:-1] , columns = ["coeficient"])

y_pred = lin.predict(X_test)
y_pred

df2 = pd.DataFrame({"Y_test" : y_test , "Y_predict": y_pred})
df2.head(10)

reg_score = r2_score(y_test , y_pred)
reg_score

p = len(x_train[0])
n = len(y_train)
adj_R2 = 1-(reg_score)*(n-1)/(n-p-1)
adj_R2

mape = mean_absolute_percentage_error(y_test , y_pred)
mape

mae = mean_absolute_error(y_test , y_pred)
mae

x2 = sm.add_constant(X)
est = sm.OLS(y , x2)
est2 = est.fit()
print(est2.summary())

print(est2.rsquared_adj)