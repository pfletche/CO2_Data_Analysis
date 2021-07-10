from shutil import copyfile
import os

for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data/AdjustedTimeFiles'):
    print(root)
    print(dirs)
    print(files)

    for file in files:
        if file != '.DS_Store':

            old_file_name = root + '/' + file

            new_file_name = root + '/' + file[0:-4] + 'csv'

            copyfile(old_file_name, new_file_name)
