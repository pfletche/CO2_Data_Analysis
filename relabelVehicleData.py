import pandas as pd
import os
from shutil import copyfile

for (root1, dirs2, files1) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data/All Vehicle Data'):
    for file in files1:

        file_array1 = file.split('_')

        if len(file_array1) > 1 and file_array1[0] != '.DS' and file_array1[0] != 'SCRUB':

            for (root2, dirs2, files2) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Vehicle Data'):
                for file2 in files2:

                    file_array2 = file2.split('_')
                    # print(file_array2)

                    if len(file_array2) > 1 and file_array2[0] != '.DS' and file_array2[0] != 'SCRUB':
                        # print(file_array1[1][0:-6])
                        # print(file_array2[1][0:-3])
                        if file_array1[1][0:-6] == file_array2[1][0:-3]:
                            # print(file_array1)
                            # print(file_array2, '\n')

                            old_file_name = root2 + '/' + file2

                            new_file_name = root2 + '/' + file_array1[0] + '_' + file2

                            print(new_file_name)
                            #
                            copyfile(old_file_name, new_file_name)