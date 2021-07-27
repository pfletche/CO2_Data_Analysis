import pandas as pd
import os


# for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles'):
#
#
#     for file in files:
#         if file != '.DS_Store':
#
#             print(file)
#             print(root + '/' + file)
#
#
#             file_df = pd.read_excel(root + '/' + file, index_col=None)
#
#             print(file_df)
#
#             file_df = file_df.loc[:, ~file_df.columns.str.contains('^Unnamed')]
#
#             file_df.to_csv(root + '/' + file[0:-4] + 'csv', index=False)




# I need to convert the sparkfun files to csvs
# I need to process the licor files from


test = pd.read_csv('Miss_Baker_Jul_19_2021_12_41_56_PM.csv')
print(test)