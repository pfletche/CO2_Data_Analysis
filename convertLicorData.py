# Importing the required libraries

import linecache as lc
import re
import pandas as pd

def parseDataLine(data_line):

    data_line = re.split('[<>\n]', str(data_line))

    for value in data_line:
        if value.startswith('/'):
            data_line.remove(value)

    while '' in data_line:
        data_line.remove('')


    data_line.remove('li850')
    data_line.remove('data')

    raw_index = data_line.index('raw')

    # Get the data and the raw data
    data = data_line[0:raw_index]
    raw_data = data_line[raw_index + 1:None]

    # Get the data labels and values
    labels = []
    values = []
    for index, element in enumerate(data):
        if index % 2 == 0:
            labels.append(element)
        else:
            values.append(element)

    # Get the raw data labels and values
    raw_labels = []
    raw_values = []

    for index, element in enumerate(raw_data):
        if index % 2 == 0:
            new_name = 'raw_' + element
            raw_labels.append(new_name)
        else:
            raw_values.append(element)

    # Combine the normal and raw data/labels
    labels = labels + raw_labels
    data = values + raw_values

    return labels, data

def parseTimeStamp(time_stamp):
    time_stamp = re.split('[,\n^]', time_stamp)

    while '' in time_stamp:
        time_stamp.remove('')

    labels = ['date', 'time']

    return labels, time_stamp


def getDataAndTimeStamp(data_file):
    line_counter = 0
    line_list = []
    add_partial_line = 0

    time_stamps = []
    data_lines = []

    for line in data_file:
        if len(line) > 1:
            # Save each line of data before the time stamp

            # Save the time stamp
            if add_partial_line == 1:
                first_half_line = line_list[-1].strip()
                second_half_line = line.strip()

                full_line = first_half_line + second_half_line

                line_list[-1] = full_line
                add_partial_line = 0

                # print(line_list)
                # print(len(line_list))
                data_lines.append(line_list)

                line_list = []


            elif line[0] == '^':
                # print(line)
                time_stamps.append(line)

                if len(line_list) == 0:
                    err = '**** NO DATA FOR TIME STAMP'
                    # print('**** NO DATA FOR TIME STAMP')
                    data_lines.append(err)

                    # Get average of prior and future data

                else:

                    last_line = line_list[-1]
                    last_line_split = last_line.split('<')

                    if last_line_split[-1] != '/li850>\n':
                        # print('**** Not a Full Line ****')
                        # print(last_line_split)
                        # print(line_list)
                        # print(len(line_list))
                        add_partial_line = 1

                        # if last part of last line is </li850>
                        # if
                        # move on and save in DF

                    else:
                        # print('**** FULL LINE ****')
                        # print(last_line_split)
                        # include next line and count as one line
                        # print(line_list)
                        # print(len(line_list))
                        data_lines.append(line_list)
                        line_list = []
            else:
                line_list.append(line)
                line_counter += 1

    # print(len(time_stamps))
    time_stamps.pop(0)
    time_stamps.pop(-1)
    # print(len(time_stamps))
    #
    # print(len(data_lines))
    data_lines.pop(0)
    data_lines.pop(-1)
    # print(len(data_lines))

    return time_stamps, data_lines

# GET THE AVERAGE DATA FOR MULTIPLE LINES
def averageDataLines(data_lines):

    data_lines_out = []

    for data in data_lines:

        if len(data) > 1 and data != '**** NO DATA FOR TIME STAMP':

            # Get the size of the data values/labels to create zeros list
            labels, data_values = parseDataLine(data[0])

            summed_vals = [0] * len(data_values)

            # Sum the values of each element for every data line
            for index, element in enumerate(data):
                # print(element)

                labels, values = parseDataLine(element)
                values = [float(i) for i in values]

                summed_vals = [sum(x) for x in zip(summed_vals, values)]

            # Get the average values for the data line
            average_values = [x / len(data) for x in summed_vals]
            # print('AVERAGE OF LAST VALUES: ', average_values, '\n') # Debugging Print Statement

            data_lines_out.append(average_values)

        elif data == '**** NO DATA FOR TIME STAMP':
            data_lines_out.append('NULL')

        else:
            # print('DATA', data)
            # l, v = parseDataLine(data)
            # print('VALUES', v)
            # print('LABELS', l)

            labels, data_values = parseDataLine(data[0])
            data_values = [float(i) for i in data_values]

            zero_vals = [0] * len(data_values)

            summed_vals = [sum(x) for x in zip(zero_vals, data_values)]

            data_lines_out.append(summed_vals)

    return labels, data_lines_out

# GET THE AVERAGE BETWEEN LAST AND NEXT LINES (FOR EMPTY DATA)
def fixEmptyData(data):

    data_list = []

    for index, element in enumerate(data):
        if element == 'NULL':
            prior_values = data[index-1]
            prior_values = [float(i) for i in prior_values]

            next_values = data[index+1]
            next_values = [float(i) for i in next_values]

            summed_vals = [sum(x) for x in zip(prior_values, next_values)]
            average_values = [x / 2 for x in summed_vals]

            data_list.append(average_values)
        else:
            data_list.append(element)

    return data_list

def convertToDf(data_file, output_file_name):
    time_lines, data_lines = getDataAndTimeStamp(data_file)

    data_labels, data = averageDataLines(data_lines)

    data = fixEmptyData(data)

    data_out = pd.DataFrame()

    for index, element in enumerate(data):

        time_labels, time_stamp = parseTimeStamp(time_lines[index])

        time_dict = {}
        data_dict = {}

        keys = time_labels
        values = time_stamp

        for index, time in enumerate(keys):
            time_dict[time] = values[index]

        # Create the data line dictionary
        keys = data_labels

        for index, val in enumerate(keys):
            data_dict[val] = [element[index]]

        # Merge the dictionaries

        time_dict.update(data_dict)

        line_df = pd.DataFrame(time_dict)

        data_out = data_out.append(line_df, ignore_index=True)

        # Add the dictionaries to a list

    data_out.to_csv(output_file_name, index=False)



if __name__ == "__main__":

    data_file = open("serialLog00018.TXT", "r")

    time_lines, data_lines = getDataAndTimeStamp(data_file)

    time_labels = []
    time_stamps = []

    data_labels, data = averageDataLines(data_lines)

    data = fixEmptyData(data)

    data_out = pd.DataFrame()

    for index, element in enumerate(data):

        time_labels, time_stamp = parseTimeStamp(time_lines[index])

        time_dict = {}
        data_dict = {}


        keys = time_labels
        values = time_stamp

        for index, time in enumerate(keys):
            time_dict[time] = values[index]

        # Create the data line dictionary
        keys = data_labels

        for index, val in enumerate(keys):
            data_dict[val] = [element[index]]

        # Merge the dictionaries

        time_dict.update(data_dict)

        line_df = pd.DataFrame(time_dict)

        data_out = data_out.append(line_df, ignore_index=True)

        # Add the dictionaries to a list







# Parse the time stamps
#     time_dict = {}
#     time_dict_list = []
#
#     for stamp in time_lines:
#         label, time_stamp = parseTimeStamp(stamp)
#
#         print(label)
#         print(time_stamp)
#
#         keys = label
#         values = time_stamp
#
#         for index, element in enumerate(keys):
#             time_dict[element] = values[index]
#
#
#         print(time_dict)
#
#         time_labels.append(label)
#         time_stamps.append(time_stamp)
#
#     print(time_labels)
#     print(time_stamps)
#
#     keys = time_labels
#     values = time_stamps
#
#     data_dict = {}
#     data_dict_list = {}
#
#     for line in data_lines:
#         if len(line) > 1:
#             # print(len(line))
#             # print(line)
#             print('**')
#
#             # Process the line
#
#             # if len(line) > 10: # aka 'NO DATA FOR TIME STAMP'
#             #     print('NO DATA')
#             # else:
#             #     for data in line:
#
#         else:
#             #print(line)
#             # Process the line
#             labels, data = parseDataLine(line)
#             print('\n\n')
#             print(labels)
#             print(data)
#
#             keys = labels
#             values = data
#
#             for index, element in enumerate(keys):
#                 data_dict[element] = values[index]
#             # print(data_dict)
#
#
# # Get the time stamp
# # Get the data
#     # Determine how many lines of data there are
#     # Get the average for the data lines
#
#         # Parse the time stamps and Data
#         time_dict = {}
#         data_dict = {}
#
#
#
#         for stamp in time_lines:
#             label, time_stamp = parseTimeStamp(stamp)
#
#             print(label)
#             print(time_stamp)
#
#             keys = label
#             values = time_stamp
#
#             for index, element in enumerate(keys):
#                 time_dict[element] = values[index]
#
#             print(time_dict)
#
#             time_labels.append(label)
#             time_stamps.append(time_stamp)
#
#         print(time_labels)
#         print(time_stamps)
#


