# Modern Dispersion Calculator TAMC Subsample
# Anthony Semeraro
# 14 June 2024

" This script reads in .csv files with a modern rivers name and n polar current measurements. It also read in a file of Transport"
" Anomaly data collected and processed by Dr. Benjamin Cardenas. Make sure to select the river morphology that you are processing."
" This script is only to be used for modern river current measurements, as the TA is automatically added which paleocurrent data does"
" does not need added."

" TA = Transport Anomaly"
# MC = Monte Carlo

#%% Importing module

import pandas as pd
from pandas import DataFrame
import random
import numpy as np
import math

#%% Loading in Data

# Modern River Dataset
riverdata = pd.read_csv(".csv") #! Do not forget to add an input file

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

Dispersion_DF = pd.DataFrame ()

#%% Initiating the main loop
i = 0

for column in columns:

    print(column)
    # Prints out name of river that it is processing

    River1 = riverdata[columns[i]].tolist()
    # Adding the river data to a list for further processing

    len_contents = len(River1)
    # Obtaining the lenght of the original dataset

    dispersion_file_normal = []
    # Creating an empty list for dispersion values to be added later

    while len_contents >= 5:
        # Subsampling down to 5 measurements

        Monte_Carlo = 500
        # Creates Monte Carlo Value -- Change if you want to run more or less

        disp = []
        # Creating an empty list for dispersion values to be added later

        while Monte_Carlo >=1:
            # Monte Carlo Loop

            column_contents = random.sample(River1, len_contents)
            # Randomly samples the river dataset for each run of the subsample

            rand_samp_anomaly = random.sample(ta_Columns,len_contents)
            # Randomly samples the anomaly dataset for each run of the subsample

            current_anomaly = [x+y if x and y else 0 for x, y in zip(column_contents, rand_samp_anomaly)]
            # Adds a TA to each river data point

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

        averagedisp = sum(disp) / len(disp)

        averagedisp = round(averagedisp,3)

        # dispersion_file_normal.append(averagedisp)
        #Writes String to dispersion text file

        dispersion_file_normal.append(averagedisp)

        len_contents -= 5
        # Change this to 1 for a smoother curve for Brady.


    dispersion_file = dispersion_file_normal[::-1]

    dispersion_file = DataFrame (dispersion_file,columns=[column])
    Dispersion_DF = pd.concat([Dispersion_DF,dispersion_file], axis=1)

    i = i + 1

# Creating a dictionary of river name and dispersion value
# dic = {"Dispersion": dispersion_name, "River": dispersion_file}

# Creating a dataframe from the dictionary
# df = pd.DataFrame(dic)

# Creating the final CSV document. Need to change name or else it overrides it each run
Dispersion_DF.to_csv(".csv") #! Do not forget to add an export file name

print("Program has succesfully completed")