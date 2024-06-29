import pickle
import pandas as pd
# from sklearn.linear_model import LinearRegression
from xgboost import XGBClassifier
# from imblearn.over_sampling import SMOTE

#read csv file
dataset = pd.read_csv("neo_v2.csv")

#preprocessing
dataset = dataset.drop(['id', 'name', 'orbiting_body', 'sentry_object'], axis=1)
dataset['hazardous'] = dataset['hazardous'].astype(int)

#split to X and y
X = dataset.drop(['hazardous'], axis = 1)
y = dataset['hazardous']

#upsize the minor class data
# smote = SMOTE(random_state=42)
# X_res, y_res = smote.fit_resample(X, y)

#from now the model name is switched from regressor to classifier
#create a model
# regressor = LinearRegression()
classifier = XGBClassifier(objective='binary:logistic', scale_pos_weight=30, max_depth=3, learning_rate=0.1, n_estimators=50)

#fit model
classifier.fit(X, y)

#serialization to .pkl file
pickle.dump(classifier, open('model.pkl', 'wb'))

#load from .pkl file
model = pickle.load(open('model.pkl', 'rb'))

#preview prediction
print(model.predict([[0.27, 0.59, 73588.73, 61438126.52, 20.00]]))
