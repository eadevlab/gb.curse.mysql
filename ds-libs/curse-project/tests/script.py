import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
# import cat

ds = pd.read_csv('./prep.csv')


y = ds['Credit Default']
X = ds.drop(['Credit Default'], axis=1)

X.drop(['Credit Score'], inplace=True, axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


model = DecisionTreeClassifier(max_depth=25)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f1_score(y_test, y_pred))