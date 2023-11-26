# generate_synthetic_data.py
import pandas as pd
import numpy as np
import numpy.random as ra

# Generate random data
working_days = 52 * 5
total = 24
work = 9
habits = 1

# desired sum
life = total - work - habits

# defines WFH (0) or WFO (1)
# defines working from home or working from office
# using multiple equal values as weighted chance based on working days per week
commute = ra.choice([1, 1, 0, 0, 0], size=working_days)

# defines !WO (0) or WOFH (1) or WOFG (2)
# defines non working out or working out from home or working out from gym
# using multiple equal values as weighted chance based on working days per week
workout = ra.choice([0, 2, 1, 2, 0], size=working_days)

# taking in mind the sleep cycle (~ 90 min)
sleep = ra.uniform(3, 9, size=working_days)

study = ra.uniform(0, 5, size=working_days)

socialize = ra.uniform(0, 5, size=working_days)

# Calculate the sum of commute and workout
fixed_sum = commute + workout

# Calculate the remaining sum needed for continuous columns to reach 14
remaining_sum = 14 - fixed_sum

# Calculate the sum of continuous columns
continuous_sum = sleep + study + socialize

# Scale continuous columns proportionally
scale_factor = remaining_sum / continuous_sum

sleep = sleep * scale_factor
study = study * scale_factor
socialize = socialize * scale_factor

# Clip values to ensure they remain within the specified intervals
sleep = np.clip(sleep, 3, 9)
study = np.clip(study, 0, 5)
socialize = np.clip(socialize, 0, 5)

# Calculates the extra time added after scaling and clipping
noise = np.round(life - commute - workout - sleep - study - socialize, 2) + 0

###########################################################################################

# personal evaluation of commuting hours
commute_value = [0, 1]
commute_evaluation = [1, 0]

# Performing polynomial interpolation (linear, degree=1)
commute_coefficients = np.polyfit(commute_value, commute_evaluation, 1)
commute_func = np.poly1d(commute_coefficients)

# Display the polynomial function
# print(commute_func)
# -1 x + 1

###########################################################################################

# personal evaluation of working out hours
workout_value = [0, 1, 2]
workout_evaluation = [0, 0.5, 1]

# Performing polynomial interpolation (linear, degree=1)
workout_coefficients = np.polyfit(workout_value, workout_evaluation, 1)
workout_func = np.poly1d(workout_coefficients)

# Display the polynomial function
# print(workout_func)
# 0.5 x

###########################################################################################

# personal evaluation of sleeping hours
sleep_value = [3, 4, 5, 6, 7, 8, 9]
sleep_evaluation = [0, 0.2, 0.4, 0.6, 0.8, 1, 0.8]

# Performing polynomial interpolation
sleep_coefficients = np.polyfit(sleep_value, sleep_evaluation, 1)
sleep_func = np.poly1d(sleep_coefficients)

# Display the polynomial function
# print(sleep_func)
# -0.0005556 x + 0.01833 x - 0.2472 x + 1.742 x - 6.752 x + 13.84 x - 11.8

###########################################################################################

# personal evaluation of studying hours
study_value = [0, 1, 2, 3, 4, 5]
study_evaluation = [0, 0.2, 1, 0.8, 0.6, 0]

# Performing polynomial interpolation
study_coefficients = np.polyfit(study_value, study_evaluation, 1)
study_func = np.poly1d(study_coefficients)

# Display the polynomial function
# print(study_func)
# -0.03333 x + 0.4417 x - 2.083 x + 3.958 x - 2.083 x + 5.092e-14

###########################################################################################

# personal evaluation of socializing hours
socialize_value = [0, 1, 2, 3, 4, 5]
socialize_evaluation = [0, 0.8, 1, 0.6, 0.2, 0]

# Performing polynomial interpolation
socialize_coefficients = np.polyfit(socialize_value, socialize_evaluation, 1)
socialize_func = np.poly1d(socialize_coefficients)

# Display the polynomial function
# print(socialize_func)
# -0.008333 x + 0.1083 x - 0.4417 x + 0.3917 x + 0.75 x + 1.248e-14

###########################################################################################


###########################################################################################

# Generate target variable (price) using a simple formula
evaluation = abs(np.round(commute_func(commute), 1)) + np.round(workout_func(workout), 1) + np.round(sleep_func(sleep), 1) + np.round(study_func(study), 1) + np.round(socialize_func(socialize), 1)
evaluation = np.round(evaluation, 1)

# Create a DataFrame
data = pd.DataFrame({
    'commute': commute,
    'workout': workout,
    'sleep': sleep,
    'study': study,
    'socialize': socialize,
    'noise': noise,
    'evaluation': evaluation
})

filtered_data = data[data['noise'] == 0]

new_data = pd.DataFrame({
    'commute': commute,
    'workout': workout,
    'sleep': sleep,
    'study': study,
    'socialize': socialize,
    'evaluation': evaluation
})

# Save the dataset to a CSV file
new_data.to_csv('synthetic_daily_hours_data.csv', index=False)

# Display the first few rows of the synthetic dataset
print(new_data.head())