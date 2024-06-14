# Modern Dispersion Calculator TAMC
# Anthony Semeraro
# 17 Jan 2022

# This script reads in .csv files with a modern rivers name and n polar current measurements. It also read in a file of Transport"
# Anomaly data collected and processed by Dr. Benjamin Cardenas. Make sure to select the river morphology that you are processing."
# This script is only to be used for modern river current measurements, as the TA is automatically added which paleocurrent data does"
# does not need added."

#! Does not work on multiple columns in a single sheet. Returns NAN values for disperison for all except longest.
#* TODO: Fix Bug

# TA = Transport Anomaly"
# MC = Monte Carlo

#%% Importing module

import pandas as pd
import numpy as np
import math

#%% Loading in Data

# River Data Read In
riverdata = pd.read_csv("Cedar_Mtn_Final.csv")

# Assigning Transport Anomaly datasets for the modern data morphologies
Morphology = input("Please enter River Morphology. A for Anastomosing, B for Braided, M for Meandering:")

if Morphology == 'A':
    TA = input("Please enter morphology of Transport Anomaly to be used. B for Braided, M for Meandering:")

    if TA == "M":
        ta = pd.read_csv("Transport_Anomaly_Meandering_Trinity.csv")

    if TA == "B":
        ta = pd.read_csv("Transport_Anomaly_Braided_NorthLoup.csv")

elif Morphology == 'B':
    ta = pd.read_csv("Transport_Anomaly_Braided_NorthLoup.csv")

elif Morphology == 'M':
    ta = pd.read_csv("Transport_Anomaly_Meandering_Trinity.csv")

elif Morphology == '0':
    ta = pd.read_csv("Bedform_0_Subsample_Field_Data.csv")

else:
    print("Invalid input")

# Columns becomes an index of the column names, each name individually is a string
columns = riverdata.columns
ta_columns = ta.columns
ta_Columns = ta[ta_columns[0]].tolist()

# Creating empty lists to hold data during loop
dispersion_file = []
dispersion_name = []

#%% Initiating the main loop
i = 0

for column in columns:

    River1 = riverdata[columns[i]].tolist()

    # Initiating Monte Carlo Loop
    Monte_Carlo = 10000
    disp = []
    while Monte_Carlo >= 1:

        lencolumn = len(River1)
        rand_samp_anomaly = np.random.choice(ta_Columns, lencolumn)
        current_anomaly = rand_samp_anomaly + River1

        # Math Section

        # Splitting the x and y components using a lambda x function
        cosine_X = lambda x: math.cos(math.radians(x))
        cosine   = np.array([cosine_X(xi) for xi in current_anomaly])

        sine_Y   = lambda x: math.sin(math.radians(x))
        sine     = np.array([sine_Y(xi) for xi in current_anomaly])

        # Getting the average of the x and y components
        avg_cosine = np.average(cosine)
        avg_sine   = np.average(sine)

        #Calculates Dispersion Value
        disp_value = math.sqrt((avg_cosine**2)+(avg_sine**2))

        # Appends the dispersion value to the list created above
        disp.append(disp_value)

        # Initiates the next iteration of the Monte Carlo loop
        Monte_Carlo -= 1

    # Finding the average dispersion value for each river from the 500 iterations and rounding to 3 decimal points
    averagedisp = sum(disp) / len(disp)
    averagedisp = round(averagedisp,3)

    # Appending the river names and dispersion values to the lists created above

    dispersion_name.append(column)
    dispersion_file.append(averagedisp)

    # Initiating the loop for the next river in the dataset
    i = i + 1

# Creating a dictionary of river name and dispersion value
dic = {"River": dispersion_name, "Dispersion": dispersion_file}

print(dispersion_file)

# Creating a dataframe from the dictionary
df = pd.DataFrame(dic)

# Creating the final CSV document. Need to change name or else it overrides it each run
df.to_csv("Cedar_Mountain_Field.csv")

print("Program has succesfully completed")

# %%