import pandas as pd

# def averageValues()

licor = pd.read_csv('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data/20210705_CanopyTower/Top Sensor/Licor/20210705_LicorData_CanopyTower_VP_F6.csv')
sparkFun = pd.read_csv('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data/20210705_CanopyTower/Bottom Sensor/20210705_SparkFunB_CanopyTower_VP_F6.csv')

# average every five rows
str_ind = 0
end_ind = 4

df = pd.DataFrame()

for index, row in licor.iterrows():

    if end_ind < len(sparkFun.index):
        slice = sparkFun.loc[str_ind:end_ind, :]
        # print(slice)

        time = sparkFun['rtcTime'].iloc[str_ind + 2]
        # print(time)

        str_ind = str_ind + 5
        end_ind = end_ind + 5

        average = slice.mean(axis=0)
        average = average.to_frame().transpose()

        average['rtcTime'] = time

        .concat([row, average], axis=1) # Does this need to be a dataframe?

        # print(average)

        df = df.append(average)

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        print(df)

######

print(df)
df.to_csv('20210705_LicorAndSparkFun_CanopyTower_VP_F6.csv')

# slice = sparkFun.loc[0:4,:]
#
# print(slice)
#
# average = sparkFun.mean(axis=0)
# average = average.to_frame().transpose()
#
# df = pd.DataFrame()
#
# df = df.append(average)
#
# df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
# print(df)


# For each of the five slices,