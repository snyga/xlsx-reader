from os import path as os_path
from os import listdir, remove
from time import strftime


import csv

def find_max_string(array:list[str], set_max=False) -> tuple:
    """
    Return tuple with length of array and longest index in array.
    """
    if set_max:
        row_num = set_max
    else:
        row_num = len(array)
    col_width = max([len(i) for i in array])
    return (col_width, row_num)

def cm2p(cm:float):
    """
    :Input: distance in centimeters (cm)
    :Returns: centimeters converted to pixels by the ration 1cm : 37.795275591 pixel 
    """
    return cm * 37.795275591

def get_index_from_str(dict:dict, item_key:str) -> int:
    """Returns indecies of itemkeys in a nested dictionary"""
    keys_and_items = [(i, key) for i, key in enumerate(dict[0].keys())]
    for i in keys_and_items:
        if item_key in i:
            index = i[0]
    return index

def merge_two_arrays(a:list, b:list, txt_fmt:bool=False) -> list[list[str]]:
    """
    Merge two arrays from a = [] and b = [] to arrays = [[a1, b1], [a2, b2]...[an, bn]].
    Array will always be the first entry in the new array.
    """
    if txt_fmt:
        merged_arrays = [[f'{str(a):<10s}:', b] for a, b in zip(a, b)]
    else:
        merged_arrays = [[a, b] for a, b in zip(a, b)]
    return merged_arrays

def get_newest_file(path:str) -> str:
    """
    Returns the newest file in the given path
    """
    print(path)
    list_of_storage_files = listdir(path)
    full_paths = [f'{path}/{file}' for file in list_of_storage_files]

    newest_file = max(full_paths, key=os_path.getctime)
    return newest_file

def get_last_dict_ID(data:dict) -> int: 
    """Returns last key in primary dictionary."""
    return data[list(data.keys())[-1]][' ID ']

def create_empty_list(data:dict) -> list[str]:
    """Returns list with length of data[0].keys() of 'Empty'"""
    empty_list = ['nan' for _ in range(len(data[0].keys()))]
    empty_list[0] = get_last_dict_ID(data) + 1
    return empty_list
    
def csv_to_nested_dict(csv_file):
    data_dict = {}
    with open(csv_file, 'r') as r_csv_file:
        reader = csv.reader(r_csv_file, delimiter=',')
        
        headers = reader.__next__()
        headers[0] = headers[0].strip('\ufeff')
        
        for i, row in enumerate(reader):
            base_dict = {}
            for col, header in enumerate(headers):
                base_dict[header] = row[col]
            data_dict[i] = base_dict
    return data_dict

def nested_dict_to_csv(data:dict[dict[str, str]], file_name:str):
    headers:list[str] = data[0].keys()
    with open(file_name, 'w', newline='') as w_csv_file:
        writer = csv.DictWriter(w_csv_file, fieldnames=headers)
        writer.writeheader()
        for key in data.keys():
            writer.writerow(data[key])
    
def save_data_to_csv(data:dict, path:str, save_data:list[bool]) -> None:
    print('Save data: ', save_data)
    if all(save_data):
        print('There has been some changes to the dictionary.')
        print('The status report has been updated...')
        time_stamp = strftime("%Y_%m_%d-%H_%M_%S")
        new_csv_file_name = path + f'/{time_stamp}' + '.xlsx'
        nested_dict_to_csv(data, new_csv_file_name)

        while True:
            list_of_storage_files = listdir(path)
            full_path = [f'{path}/{file}' for file in list_of_storage_files]
            
            if len(list_of_storage_files) <= 25:
                break
            print('Removing files...')
            oldest_file = min(full_path, key=os_path.getctime)
            remove(oldest_file)
    else:
        print('No changes were made to the status report.')