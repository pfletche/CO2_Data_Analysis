from convertLicorData import parseDataLine
import pandas as pd

data_file = open("F8_20210706.TXT", "r")

data_out = pd.DataFrame()

for line in data_file:

    labels, data  = parseDataLine(line)

    print(labels)
    print(data)

    dict = {}

    keys = labels
    values = data

    for index, element in enumerate(keys):
        dict[element] = [values[index]]

    line_df = pd.DataFrame(dict)

    data_out = data_out.append(line_df, ignore_index=True)

print(data_out)
data_out.to_csv("F8_20210706.csv", index=False)