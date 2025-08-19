import csv

def mapdata_generator():
    csv_file_path = 'testgen/map_test_data.csv' # Replace with your CSV file name

    data_dict_list = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data_dict_list.append(row)

    return data_dict_list