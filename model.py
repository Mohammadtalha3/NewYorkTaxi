from preprocessing import Preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression

process= Preprocessing()
#data= process.Spliting_data()


X_train_scaled,y_train,X_test_scaled,y_test= process.Spliting_data()

# model=RandomForestRegressor()
# model.fit(X_train_scaled,y_train)
model = LinearRegression()
model.fit(X_train_scaled,y_train)

y_pred= model.predict(X_test_scaled)

rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse}")
print(f"R^2: {r2}")

