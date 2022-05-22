import csv
import re
import sys
from collections import Counter
from collections import OrderedDict

IDs = list[str]
valid_id_regex = re.compile(r"\d+")


def scan_csv(csv_file: str) -> IDs:  # scans all csv files and returns ids from each as individual lists
    try:
        with open(csv_file) as csv:  # opens csv files, uses regex to ignore invalid ids
            ids = [int(id_) for id_ in re.findall(valid_id_regex, csv.read())]
    except Exception as err:
        raise SystemExit(
            f"Error processing file {csv_file}: {err}")  # throws error and ends program if error processing csv

    return ids  # returns all ids as list[str]


def sort_ids_list(id_list: list) -> list[int]:  # takes a list of ids and sorts them
    sorted_list = sorted(id_list)
    return sorted_list  # returns sorted list


def ordered_dict(id_dict: dict) -> dict:  # takes a dictionary and sorts them by key
    od = OrderedDict(sorted(id_dict.items()))
    return od  # returns ordereddict object of type dict


def get_id_count(id_list: list) -> Counter:  # utilizes counter from collections to count ids within a list
    id_count = Counter(id_list)
    return id_count  # returns counter dictionary of type dict


input_args = sys.argv[2:]  # global variable keeping list of all input sys arguments


def get_all_ids_count() -> list:
    counts = []  # initializes list for counts
    id_dict = get_id_dict()  # gets dictionary with all ids
    # input_args = sys.argv[2:]
    for csv in input_args:  # iterates through each csv file in input args
        id_list = id_dict[csv]  # gets id_list from id_dict using csv as key
        count = get_id_count(id_list)  # gets count of all ids within list
        counts.append(count)  # appends new count to counts list
    return counts  # returns all counts


ids = {}  # global variable keeping dictionary with csv_file as key and ids as value


def get_id_dict() -> dict:
    csv_out, *csvs_in = sys.argv[1:]  # initializes sys arguments from user input

    for csv_file in csvs_in:  # iterates over each csv_file from input
        ids[csv_file] = scan_csv(
            csv_file)  # scans ids and csv, sets in dictionary with key:value being 'file.csv':[ids]
    return ids  # returns dictionary with all csv_file and ids


def update_new_keys(orig_dict: dict, new_dict: dict) -> dict:
    for key in new_dict.keys():
        new_count_len = len(input_args) - 1
        new_list = [0] * new_count_len
        new_list.append(new_dict[key])
        new_dict[key] = new_list

    # orig_dict.update(new_dict)

    return orig_dict


def update_new_keys_test(orig_dict: dict, new_dict: dict) -> dict:
    print('orig dict vvv')
    print(orig_dict)
    print('new_dict vvvv')
    print(new_dict)
    print('-----------')

    for key in new_dict.keys():
        new_count_len = len(input_args) - 1
        new_list = [0] * new_count_len
        new_list.append(new_dict[key])
        new_dict[key] = new_list

    # orig_dict.update(new_dict)

    print('orig dict post vvv')
    print(orig_dict)
    print('new_dict post vvvv')
    print(new_dict)
    print('-----------')
    return orig_dict


def update_dict_count(orig_dict: dict, new_dict: dict) -> dict:
    for key in orig_dict.keys():
        if key in new_dict:  # key in both dictionaries, appends count to end of original value
            print('------------')
            print('KEY: ' + str(key) + ' IN BOTH')
            orig_dict[key].append(new_dict[key])
            del new_dict[key]  # deletes new key from new_dict for
            print('DELETED KEY: ' + str(key))
            print('------------')
        else:
            print('key: ' + str(key) + ' not found')
            orig_dict[key].append(0)  # appends 0 if key from orig_dict is not present in new_dict

    update_new_keys_test(orig_dict, ## ERROR HERE
                         new_dict)  # takes updated orig_dict (with common values or values not in new_dict), updates with values from new_dict which now only consist of new ids

    return orig_dict


def base_dict_values_to_list(
        id_dict: dict) -> dict:  # transforms base dictionary values into lists to be appended to for count
    for key in id_dict.keys():
        id_dict[key] = [id_dict[key]]
    return id_dict  # returns new dict where key:value is id:[count]


# file_name_regex = re.compile(r"/^([^.]+)/")                 #regex to initialize get file name


def write_to_csv(data_to_write: dict):  # function to write to csv once all is completed
    file_to_write = sys.argv[1]  # gets name of file to write/create from sys args
    with open(file_to_write, 'w', newline='') as file:  # prepares file for write
        writer = csv.writer(file)
        writer.writerow(['id'] + input_args)  # writer object writes header row with id and file_name args
        for key_id in data_to_write:  # for each key in final_data
            counts = data_to_write[key_id]  # get counts from data_dict
            writer.writerow([key_id] + counts)  # writes to row as ID, count1, count2, countN...,
        print('file written')


def main():
    if len(sys.argv) < 2:
        raise SystemExit(
            f"Usage: {sys.argv[0]} file_to_write file1_to_read [fileN_to_read...]")  # shows error when input argument is invalid with less than 2 files. Argument expected is: output_file.csv input1.csv input2.csv inputN.csv...
    all_ids_count = get_all_ids_count()  # gets count for all ids
    base_dict_counter = all_ids_count[0]  # initializes base dictionary to add to
    base_dict = base_dict_values_to_list(base_dict_counter)  # converts base dictionary values to list

    for i in range(1, len(sys.argv) - 2):  # iterates through all csv arguments updating the base dictionary

        updated_orig_dict = update_dict_count(base_dict, all_ids_count[i])

    final_dict = ordered_dict(updated_orig_dict)  # gets final dictionary and sorts it using OrderedDict
    write_to_csv(final_dict)  # writes final dictionary to csv


if __name__ == '__main__':
    main()
