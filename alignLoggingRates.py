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
            # new = row[['time(millisecond)',
            #                     'datetime(utc)',
            #                     'latitude',
            #                     'longitude',
            #                     'height_above_takeoff(feet)',
            #                     'altitude_above_seaLevel(feet)',
            #                     'flycState']].copy()
            #
            # data_out = data_out.append(new)

            data_out = data_out.append(row)

    return data_out

def averageLoggingRateLicor(data, desired_log_rate):

    licor_log_rate = 2 # Two readings per second (2hz)

    rows_per_datapoint = int(licor_log_rate / desired_log_rate)

    data_out = pd.DataFrame()
    data_row = pd.DataFrame()

    for index, row in data.iterrows():

        if index % rows_per_datapoint == 0 and index > 0:

            # Get the time from the second index and remove the
            value = data_row['adjusted_time']
            time = value.iloc[1]

           # data_row = data_row.drop(columns=['date', 'time', 'adjusted_time'])
            data_row = data_row.drop(columns=['adjusted_time']) # Change to this if licor data doesn't have logger stamp

            data_row = data_row.mean()

            data_row['time'] = time

            data_out = data_out.append(data_row, ignore_index=True)

            data_row = pd.DataFrame()
            data_row = data_row.append(row)

        else:
            data_row = data_row.append(row)

    return data_out


if __name__ == "__main__":

    #data = pd.read_csv('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles/Sliced Licor Files/test/M3_F41_20210708_Licor_YuccaFarm_HPx3.csv')

    # # Input directory path for Vehicle Data Missions
    # for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data/All_Flight_Data/Vehicle Data (0.5hz)'):
    #
    #     for file in files:
    #         if file != '.DS_Store' and file != 'Icon?':
    #             print('Reading File: ' + file)
    #             file_path = root + '/' + file
    #
    #             vehicle_data = pd.read_csv(file_path)
    #
    #             new_vehicle_data = reduceLogRate(vehicle_data, 20)
    #             print('Finished converting ', file)
    #
    #             new_file_name = root + '/halfHz_' + file
    #             new_vehicle_data.to_csv(new_file_name, index=False)
    #             # data_file = open(file_path, "r", encoding="ascii", errors="surrogateescape")
    #
    #
    # Input directory path for Licor Data Missions
    for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles/Sliced Licor Files/missions'):

        for file in files:
            if file != '.DS_Store' and file != 'Icon?':
                print('Reading File: ' + file)
                file_path = root + '/' + file

                licor_data = pd.read_csv(file_path)

                new_licor_data = averageLoggingRateLicor(licor_data, 0.5)
                print('Finished converting ', file)

                new_file_name = root + '/halfHz_' + file
                sf = file.split('_')
                new_file_name = root + '/' + sf[1] + '_' + sf[0] + '_halfHz_' + file[7:None]

                new_licor_data.to_csv(new_file_name, index=False)



