# This script aligns the data based on the different logging rates
# Licor Data: 2hz
# Vehicle Data: 10hz
# Kestral Data: 0.5hz
import pandas as pd
import os

# Get the first row, then the 21st row

def reduceLogRate(data, log_value): # Gets values at different log rate (no averaging)

    data_out = pd.DataFrame()

    for index, row in data.iterrows():
        if index % log_value == 0:
            new = row[['time(millisecond)',
                                'datetime(utc)',
                                'latitude',
                                'longitude',
                                'height_above_takeoff(feet)',
                                'altitude_above_seaLevel(feet)',
                                'flycState']].copy()

            data_out = data_out.append(new)

    return data_out

if __name__ == "__main__":

    for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data/All_Flight_Data/Vehicle Data (0.5hz)'):

        for file in files:
            if file != '.DS_Store' and file != 'Icon?':
                print('Reading File: ' + file)
                file_path = root + '/' + file

                vehicle_data = pd.read_csv(file_path)

                new_vehicle_data = reduceLogRate(vehicle_data, 20)
                print('Finished converting ', file)

                new_file_name = root + '/halfHz_' + file
                new_vehicle_data.to_csv(new_file_name, index=False)
                # data_file = open(file_path, "r", encoding="ascii", errors="surrogateescape")

