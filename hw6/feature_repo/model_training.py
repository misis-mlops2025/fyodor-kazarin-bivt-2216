import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime, timedelta

def create_dataset_with_timestamps():
    np.random.seed(42)  # For reproducible results
    driver_ids = list(range(1001, 1021))
    base_time = datetime(2021, 4, 12, 10, 59, 42)
    timestamps = [base_time + timedelta(hours=i*2) for i in range(10)]
    
    data = []
    for driver_id in driver_ids:
        for timestamp in timestamps:
            conv_rate = np.random.uniform(0.1, 1.0)
            acc_rate = np.random.uniform(0.5, 1.5)
            avg_daily_trips = int((conv_rate * 50 + acc_rate * 30 + np.random.normal(0, 5)).clip(1, 100))
            
            data.append({
                'driver_id': driver_id,
                'event_timestamp': timestamp,
                'conv_rate': conv_rate,
                'acc_rate': acc_rate,
                'avg_daily_trips': avg_daily_trips
            })
    
    df = pd.DataFrame(data)
    return df

def train_model(df):
    X = df[['conv_rate', 'acc_rate']]
    y = df['avg_daily_trips']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Model Performance:")
    print("Mean Squared Error: {:.2f}".format(mse))
    print("R² Score: {:.2f}".format(r2))
    print("Coefficients: conv_rate={:.2f}, acc_rate={:.2f}".format(model.coef_[0], model.coef_[1]))
    print("Intercept: {:.2f}".format(model.intercept_))
    
    return model, X_test, y_test, y_pred

def main():
    print("Creating dataset with 10 timestamps for all driver_id...")
    df = create_dataset_with_timestamps()
    print("Dataset created with {} rows".format(len(df)))
    print(df.head())
    
    print("\nTraining model to predict avg_daily_trips using conv_rate and acc_rate...")
    model, X_test, y_test, y_pred = train_model(df)
    
    print("\nSample predictions:")
    sample_data = pd.DataFrame({
        'conv_rate': [0.5, 0.8, 0.3],
        'acc_rate': [1.0, 1.2, 0.8]
    })
    predictions = model.predict(sample_data)
    for i, pred in enumerate(predictions):
        print("conv_rate={}, acc_rate={} => predicted avg_daily_trips={:.1f}".format(
            sample_data.iloc[i]['conv_rate'], 
            sample_data.iloc[i]['acc_rate'], 
            pred))

if __name__ == "__main__":
    main()
