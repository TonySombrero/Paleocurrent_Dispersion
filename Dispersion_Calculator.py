# Paleocurrent Dispersion Calculator

# Anthony Semeraro
# 14 June 2024

# This script reads in a .csv file of paleocurrent measurements. Line 1 is name of the dataset, paleocurrent
# measurements begin on line 2. This script returns the dispersion value along with a .csv file with the
# dataset name and the dispersion value. The input file can contain as many paleocurrent datasets as a .csv
# will allow as long as they are in the correct format listed above.

import pandas as pd
import numpy as np
import math

#%% Loading in Data

# Paleocurrent Data #! Ensure you rename the output file
riverdata = pd.read_csv(".csv")

# Columns becomes an index of the column names, each name individually is a string
columns = riverdata.columns

# Creating empty lists to hold data during loop
dispersion_file = []
dispersion_name = []

i = 0

for column in columns:

    # Writing data to list format
    riverlist = riverdata[columns[i]].tolist()

    # Removing NaN values from list
    river1 = [x for x in riverlist if pd.isnull(x) == False]

    # Splitting the x and y components using a lambda x function
    cosine_X = lambda x: math.cos(math.radians(x))
    cosine   = np.array([cosine_X(xi) for xi in river1])

    sine_Y   = lambda x: math.sin(math.radians(x))
    sine     = np.array([sine_Y(xi) for xi in river1])

    # Averaging of the x and y components
    avg_cosine = np.average(cosine)
    avg_sine   = np.average(sine)

    #Calculates Dispersion Value
    disp_value = math.sqrt((avg_cosine**2)+(avg_sine**2))

    # Appending the river names and dispersion values to the lists created above
    dispersion_name.append(column)
    dispersion_file.append(disp_value)

    # Returns Dataset Name
    print(column)

    # Returns Dispersion Value for Dataset
    print(disp_value)

    # Initiating the loop for the next river in the dataset if dataset has another column
    i = i + 1

# Creating a dictionary of river name and dispersion value
dic = {"Dispersion": dispersion_name, "River": dispersion_file}

# Creating a dataframe from the dictionary
df = pd.DataFrame(dic)

# Creating the final CSV document
df.to_csv(".csv") #! Do not forget to add a name for the output file

print("Program has succesfully completed")
# %%
