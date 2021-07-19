import pandas as pd
import os

vehicle_data = pd.read_csv("/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Vehicle Data/Jul-8th-2021-11-13AM-Flight-Airdata.csv")

print(vehicle_data)

def getVehicleMissions(data): # Use this for the Vehicle data sheet

    mission_array = []
    prior_row_state = 'NULL'

    mission_number = 1

    for index, row in data.iterrows():

        row_state = row['flycState']

        if row_state == 'Waypoint' and prior_row_state != 'Waypoint':
            mission = pd.DataFrame()

            new = row[['time(millisecond)',
                       'datetime(utc)',
                       'latitude',
                       'longitude',
                       'height_above_takeoff(feet)',
                       'altitude_above_seaLevel(feet)',
                       'flycState']].copy()

            mission = mission.append(new)

        elif row_state == 'Waypoint' and prior_row_state == 'Waypoint':

            new = row[['time(millisecond)',
                       'datetime(utc)',
                       'latitude',
                       'longitude',
                       'height_above_takeoff(feet)',
                       'altitude_above_seaLevel(feet)',
                       'flycState']].copy()

            mission = mission.append(new)

        elif row_state != 'Waypoint' and prior_row_state == 'Waypoint':

            mission_array.append(mission)

        prior_row_state = row_state

    return mission_array

def getVehicleMissionsNewFormat(data): # Use this for the Vehicle data sheet

    mission_array = []
    prior_row_state = 'NULL'

    mission_number = 1

    for index, row in data.iterrows():

        row_state = row[' OSD.flycState']

        if row_state == 'Waypoints' and prior_row_state != 'Waypoints':
            mission = pd.DataFrame()

            new = row[['CUSTOM.updateTime [local]',
                       ' OSD.flyTime [s]',
                       ' OSD.latitude',
                       ' OSD.longitude',
                       ' OSD.height [ft]',
                       ' OSD.altitude [ft]',
                       ' OSD.flycState']].copy()

            mission = mission.append(new)

        elif row_state == 'Waypoints' and prior_row_state == 'Waypoints':

            new = row[['CUSTOM.updateTime [local]',
                       ' OSD.flyTime [s]',
                       ' OSD.latitude',
                       ' OSD.longitude',
                       ' OSD.height [ft]',
                       ' OSD.altitude [ft]',
                       ' OSD.flycState']].copy()

            mission = mission.append(new)

        elif row_state != 'Waypoints' and prior_row_state == 'Waypoints':

            mission_array.append(mission)

        prior_row_state = row_state

    return mission_array


def getLicorMissions(data_frame):
    prior_mission_status = 'NULL'
    mission_array = []

    for index, row in data_frame.iterrows():

        mission_status = row['mission_status']

        if mission_status == 'M' and prior_mission_status != 'M':
            mission = pd.DataFrame()

            new = row[['adjusted_time',
                       'co2',
                       'h2o',
                       'h2odewpoint',
                       'raw_flowrate',
                       'mission_status']].copy()

            mission = mission.append(new)

        elif mission_status == 'M' and prior_mission_status == 'M':
            new = row[['adjusted_time',
                       'co2',
                       'h2o',
                       'h2odewpoint',
                       'raw_flowrate',
                       'mission_status']].copy()

            mission = mission.append(new)

        elif mission_status != 'M' and prior_mission_status == 'M':
            mission_array.append(mission)

        prior_mission_status = mission_status

    return mission_array


if __name__ == "__main__":

    for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles/Sliced Licor Files'):

        for file in files:
            if file != '.DS_Store':
                file_path = root + '/' + file

                # data = pd.read_csv(file_path)
                data = pd.read_excel(file_path)

                # mission_array = getVehicleMissions(data)
                mission_array = getLicorMissions(data)

                mission_number = 1

                for mission in mission_array:

                    file_name = root + '/' + 'M' + str(mission_number) + '_' + file
                    mission.to_csv(file_name[0:-4] + 'csv', index=False)

                    mission_number = mission_number + 1

                print('Finished ' + file)





