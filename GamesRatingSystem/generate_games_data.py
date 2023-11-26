# generate_synthetic_data.py
import pandas as pd
import numpy as np
import numpy.random as ra

games = 500

# Generate random data
lines = ra.choice([10,10,10,20,20,20,30,30,40,50,243,243,243,117649,117649], size=games)
volatility = ra.choice([1,1,1,2,2,3,3,4,5], size=games)
hitrate = ra.choice([1,2,3,3,4,4,5,5,5], size=games)
theme = ra.choice(['asian','asian', 'magic', 'casual', 'casual', 'casual', 'casual', 'sequence', 'sequence', 'sequence'], size=games)
rating = ra.choice([1,2,2,3,3,3,4,4,4,4,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,8,8,8,8,9,9,9,10,10], size=games)

# Create a DataFrame
data = pd.DataFrame({
    'lines': lines,
    'volatility': volatility,
    'hitrate': hitrate,
    'theme': theme,
    'rating': rating
})

# Save the dataset to a CSV file
data.to_csv('synthetic_games_data.csv', index=False)

# Display the first few rows of the synthetic dataset
print(data.head())