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