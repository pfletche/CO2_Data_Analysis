import pandas as pd
import os

directory = '/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Colab Test/VehicleRAW/untitled folder'

vehicle_data_files = os.listdir(directory)

from shutil import copyfile

#copyfile('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Colab Test/VehicleRAW/F44_DJIFlightRecord-2021-07-13-[10-26-42].csv', '/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Colab Test/VehicleRAW/2F44_DJIFlightRecord-2021-07-13-[10-26-42].csv')

for file_name in vehicle_data_files:

    vehicle_dataframe = pd.read_csv(directory + '/' + file_name, low_memory=False)

    # new_df = vehicle_dataframe['CUSTOM.updateTime [local]']

    print(vehicle_dataframe)


# from csv import reader
# # open file in read mode
#
# with open('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Colab Test/VehicleRAW/DJIFlightRecord-2021-07-13-[14-23-04].csv', 'r') as read_obj:
#     # pass the file object to reader() to get the reader object
#     csv_reader = reader(read_obj)
#     # Iterate over each row in the csv using reader object
#
#     print(csv_reader[0:1])