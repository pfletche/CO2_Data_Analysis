import pandas as pd


# ************************************************************************************
# Name: reduceLogRate(data, log_value)
# Description: gets value at a different logging rate
# Usage: use to get vehicle data at 0.5 hz to align with Kestral
# ************************************************************************************

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

# ************************************************************************************
# Name: averageLoggingRateLicor(data, desired_log_rate)
# Description: gets value at a different logging rate with averaging
# Usage: use to get Licor data at 0.5 hz to align with Kestral
# ************************************************************************************

def averageLoggingRateLicor(data, desired_log_rate): # Get the value at a different log rate with averaging

    print(data)

    licor_log_rate = 2 # Two readings per second (2hz)

    rows_per_datapoint = int(licor_log_rate / desired_log_rate)

    data_out = pd.DataFrame()
    data_row = pd.DataFrame()

    for index, row in data.iterrows():

        if index % rows_per_datapoint == 0 and index > 0:

            # Get the time from the second index and remove the
            value = data_row['adjusted_time']
            time = value.iloc[1]

            data_row = data_row.drop(columns=['adjusted_time', 'mission_status'])

            data_row = data_row.mean()

            data_row['time'] = time

            data_out = data_out.append(data_row, ignore_index=True)

            data_row = pd.DataFrame()
            data_row = data_row.append(row)

        else:
            data_row = data_row.append(row)

    return data_out

def increaseTime(time):

    hours, minutes, seconds = time.split(':')

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    if seconds >= 59: # then add to the minutes
        seconds = 0

        if minutes >= 59: # then add to the hours
            minutes = 0

            if hours >= 24:
                hours = 1
            else:
                hours += 1
        else:
            minutes += 1
    else:
        seconds += 1

    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)

    time_out = str(hours) + ':' + str(minutes) + ':' + seconds

    return time_out

def assignAdjustedTimeCol(data, flight_start_time):

    adjusted_time = []

    current_time = flight_start_time

    for index, row in data.iterrows():

        if index == 0:
            current_time = current_time
        elif index % 2 != 0:
            current_time = current_time
        else:
            current_time = increaseTime(current_time)

        adjusted_time.append(current_time)

    data['adjusted_time'] = adjusted_time

    return data




# ************************************************************************************
# assignMissionTimes(data, data_file_name, flight_log)
# assigns a time column based on start and stop times in the flight log
# requires flight logging start time, mission start times, mission end times
# ************************************************************************************

def assignMissionTimes(data, data_file_name, flight_log):

    # Get the flight number
    flight_number = data_file_name.split('_')[0]
    print('Flight Number: ', flight_number)

    # Get flight log row in flight_log
    log_row = flight_log.loc[flight_log['Flight Number'] == flight_number]

    # Get number of missions
    num_missions = log_row['# of Missions'].item()
    print('Number of Missions: ', num_missions)

    # Get flight start time
    flight_start_time = log_row['Flight Start Time'].item()
    print('Flight Start Time: ', flight_start_time)

    data = assignAdjustedTimeCol(data, flight_start_time)

    mission_times = []

    # Get start and stop times for missions
    for missions in range(num_missions):
        print(missions)

        times = []

        mission_num = missions + 1

        start_column = 'Mission ' + str(mission_num) + ' Start'
        stop_column = 'Mission ' + str(mission_num) + ' Stop'

        times.append(log_row[start_column].item())
        times.append(log_row[stop_column].item())

        mission_times.append(times)

    print(mission_times)

    print(data)

    # Next thing to do it iterate through and split up the missions based on the times.

    # Get the row with the first mission start time - return the index
    # Get the row with the first mission end time - return the index

    return data, mission_times


def sliceMissions(data, mission_times):

    missions = []

    for index, times in enumerate(mission_times):
        start_mission_row = data.loc[data['adjusted_time'] == mission_times[index][0]]
        start_ind = start_mission_row.index.to_list()[0]

        end_mission_row = data.loc[data['adjusted_time'] == mission_times[index][1]]
        end_ind = end_mission_row.index.to_list()[1]

        print('Mission ', str(index), ' start index: ', start_ind)
        print('Mission ', str(index), ' end index: ', end_ind)

        missions.append(data.loc[start_ind:end_ind, :])

    return missions

# data_file_name = 'F39_20210708_Licor_YuccaFarm_VPx2.csv'
#
# data = pd.read_csv(data_file_name)
# flight_log = pd.read_csv('Flight_Log.csv')
#
# data_with_adjusted_time, mission_times = assignMissionTimes(data, data_file_name, flight_log)
#
# missions = sliceMissions(data_with_adjusted_time, mission_times)
#
# print(missions)