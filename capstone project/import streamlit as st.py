import streamlit as st
import pandas as pd
import numpy as np
from tensorflow import keras

# Load the saved models
models = {}
for product in ['Maize meal(2kg)', 'price of bread (400g)', 'Refined Vegetable oil (1L)', 'Cows Milk(Fresh,Pasteurized) -500ML',' Diesel (1L)', 'Gasoline (1L)', '12-Month Inflation', 'Buy']:
    model = keras.models.load_model(f"{product}_time_series_model.h5")
    models[product] = model

# Define the forecast periods and dates
forecast_periods = 12
forecast_dates = pd.date_range(start='2023-04-01', periods=forecast_periods, freq='MS')

# Define the commodities and their corresponding indices
commodities = ['Maize meal(2kg)', 'price of bread (400g)', 'Refined Vegetable oil (1L)', 'Cows Milk(Fresh,Pasteurized) -500ML',' Diesel (1L)', 'Gasoline (1L)', '12-Month Inflation', 'Buy']
commodity_indices = {commodity: i for i, commodity in enumerate(commodities)}

# Define the default values for the commodity, month, and year
default_commodity = 'Maize meal(2kg)'
default_month = 'April'
default_year = '2023'

# Define a function to get the forecasted price for a given commodity, month, and year
def get_forecast_price(commodity, month, year):
    # Get the index of the commodity
    commodity_index = commodity_indices[commodity]

    # Get the last n_steps values from the training set
    last_n_steps = train_data[commodity][-n_steps:].values.reshape(-1, 1)

    # Calculate the number of months between the start date and the selected date
    selected_date = pd.to_datetime(f"{month} {year}")
    months_since_start = (selected_date - forecast_dates[0]) // pd.Timedelta(days=30)

    # Make predictions for the selected date
    forecast = models[commodity].predict(last_n_steps)[0][0]
    for i in range(months_since_start):
        last_n_steps = np.vstack([last_n_steps[1:], [[forecast]]])
        forecast = models[commodity].predict(last_n_steps)[0][0]

    # Return the forecasted price
    return forecast

# Load the data from the file
train_data = pd.read_csv("Time Series Data.csv")

# Define the number of steps to use for input to the model
n_steps = 12

# Set the title of the app
st.title('Commodity Price Forecasting App')

# Create a sidebar for selecting the commodity, month, and year
commodity = st.sidebar.selectbox('Commodity:', commodities, index=commodity_indices[default_commodity])
month = st.sidebar.selectbox('Month:', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], index=3)
year = st.sidebar.selectbox('Year:', ['2023', '2024', '2025', '2026'], index=0)

# Calculate the forecasted price for the selected commodity, month, and year
forecast_price = get_forecast_price(commodity, month, year)

# Display the forecasted price
st.write(f"Forecasted price of {commodity} for {month}, {year}: {forecast_price}")