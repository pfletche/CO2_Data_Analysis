import os
import convertLicorData as CLD


for (root, dirs, files) in os.walk('/Users/paul/Google_Drive/NIMBUS_lab/Costa Rica/Flight Data csv/Licor Data'):
    print(root)
    print(dirs)
    print(files)

    for file in files:
        if file != '.DS_Store':
            file_path = root + '/' + file
            print(file_path)
            data_file = open(file_path, "r", encoding="ascii", errors="surrogateescape")

            output_file_name = root + '/' + file[0:-3] + 'csv'

            print(output_file_name)

            CLD.convertToDf(data_file, output_file_name)

            data_file.close()

            print('Finished data file: ', file)