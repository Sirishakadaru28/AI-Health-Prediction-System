import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib


data={
"glucose":[90,180,110,220,95,170,130],
"haemoglobin":[14,10,13,8,15,11,12],
"cholesterol":[170,250,180,300,160,240,200],

"result":[
"Healthy",
"Diabetes Risk",
"Healthy",
"High Disease Risk",
"Healthy",
"Health Warning",
"Medium Risk"
]
}


df=pd.DataFrame(data)


X=df[
[
"glucose",
"haemoglobin",
"cholesterol"
]
]


y=df["result"]


model=RandomForestClassifier()


model.fit(X,y)


joblib.dump(
model,
"health_model.pkl"
)


print("Model Created Successfully")