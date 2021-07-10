import getMissions as gm
import pandas as pd

licor_data = pd.read_excel("/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles/Sliced Licor Files/F42_20210708_Licor_YuccaFarm_VPx2.xlsx")

prior_mission_status = 'NULL'
mission_array = []

for index, row in licor_data.iterrows():

    mission_status = row['mission_status']

    print(mission_status)

    if mission_status == 'M' and prior_mission_status != 'M':
        print('Create new dataframe')
        mission = pd.DataFrame()

        new = row[['adjusted_time',
                   'co2',
                   'h2o',
                   'h2odewpoint',
                   'raw_flowrate',
                   'mission_status']].copy()

        mission = mission.append(new)

    elif mission_status == 'M' and prior_mission_status == 'M':
        print('Add to dataframe')

        new = row[['adjusted_time',
                   'co2',
                   'h2o',
                   'h2odewpoint',
                   'raw_flowrate',
                   'mission_status']].copy()

        mission = mission.append(new)

    elif mission_status != 'M' and prior_mission_status == 'M':
        print('Output a csv')

        mission_array.append(mission)

    prior_mission_status = mission_status
