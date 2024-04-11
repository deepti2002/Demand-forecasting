import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load pre-trained model
with open('/Users/deeptilalwani/Documents/Data Science/PROJECT 1_demand forecasting/submission docs/FINAL/final_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define user interface
st.title('Forecasting App')
st.write('Enter the forecasting period (in weeks):')
forecast_weeks = st.number_input('Weeks:', min_value=1, step=1)

#Load the Data
data = pd.read_csv("/Users/deeptilalwani/Documents/Data Science/PROJECT 1_demand forecasting/train.csv")

# Convert 'date' column to datetime
data['date'] = pd.to_datetime(data['date'])

# Set 'date' column as the index
data.set_index('date', inplace=True)

data['diff_sales'] = data['sales'] - data['sales'].shift(1)
data['diff_sales'].dropna(inplace=True)
weekly_data = data['diff_sales'].resample('W').mean().dropna()

# Create the Exponential Smoothing model with optimized parameters
final_model = sm.tsa.ExponentialSmoothing(weekly_data, trend='add', seasonal='add', seasonal_periods=52)
fit = final_model.fit(smoothing_level=0.5, smoothing_trend=0.2, smoothing_seasonal=0.2)


# Calculate forecast periods based on the input
forecast_periods = forecast_weeks  # Number of forecast periods

# Calculate split_point
split_point = int(len(weekly_data) * 0.8)  # 80% training, 20% validation
validation_data = weekly_data[split_point:]


# Generate forecast
if st.button('Generate Forecast'):
    # Calculate forecast periods based on the input
    forecast_periods = forecast_weeks  # Number of forecast periods

    # Perform forecasting based on the input
   
    forecast_values = fit.forecast(steps=forecast_periods)

    # Plot the forecast graph
    plt.plot(forecast_values)
    plt.xlabel('Weeks')
    plt.ylabel('Forecast Value')
    st.pyplot(plt)
