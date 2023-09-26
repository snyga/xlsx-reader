#%%
from PySimpleGUI import Text, Table, Button, Column, Window, Input, Listbox, popup_ok_cancel
from PySimpleGUI import VerticalSeparator, HorizontalSeparator
from PySimpleGUI import WIN_CLOSED
from PySimpleGUI import theme as sg_theme


from status_utility import find_max_string, cm2p, get_newest_file, get_last_dict_ID
from status_utility import create_empty_list, merge_two_arrays
from status_utility import csv_to_nested_dict, save_data_to_csv

#%% directly to do with the listings
def find_unique_main_keys(data:dict[dict[str]], item_key:str):
    """
    Main key is the row, while key_item is the specific column.
    - data: dict()
    - item_key: str()
    - Returns all unique nested keys.

    - If 'item_key' == ' ID ' 
    """
    unique_main_keys = []
    for key in data.keys():
        item:str = data[key][item_key]
        if item not in unique_main_keys and str(item) != 'nan':
            unique_main_keys.append(str(item))
    if item_key != ' ID ': 
        return ['Show all'] + sorted(unique_main_keys)
    else: 
        return sorted(unique_main_keys)

def create_temporary_list(data:dict, item_key:str='Show all', item:str=''):
    """Returns a list of lists based on a nested dictinary"""
    temp_lists = []
    for main_key in data.keys():
        temp_list = [i for _, i in data[main_key].items()]
        # print(main_key, data[main_key])
        if 'Show all' in [item_key, item]:
            temp_lists.append(temp_list)
        elif item_key != 'Show all' and item in data[main_key][item_key]:
            temp_lists.append(temp_list)
    return temp_lists

def create_new_base_dict(data:dict) -> tuple[dict[int, dict[str, str]], list[str]]:
    """
    Creates a new dictionary based on a nested dictionary and appends it to the exsisting dictionar.:
    :param data: dictionary with the following setup:
     - data = {a:{a1:'', a2:''}, 
               b:{b1:'', b2:''},
               ...}
     - Returns the original dictionary with a new key containing an empty dictionary. 
       The key will always increase by one.
    """
    base_dict:dict[str] = {}
    for _, key in enumerate(list(data[0].keys())):
        base_dict[key] = 'nan'
    last_ID = get_last_dict_ID(data)
    base_dict[' ID '] = last_ID + 1
    data[last_ID] = base_dict
    return data

def update_dict_with_list(data:dict, new_list:list, new_entry:bool=False):
    if new_entry:
        data = create_new_base_dict(data)
    for key, item in data.items():
        if new_list != None:
            if item[' ID '] == new_list[0]:
                item_keys = list(item.keys())
                print('', '_'*100, f'Updating key {key}:', '-'*100, sep='\n')               ## for debugging
                print(f"{'Original list':55s}|{'New list'}", '.'*100, sep='\n')
                for i in range(len(item_keys)):
                    if i != 0:
                        print(f'{str(data[key][item_keys[i]]):<55s}|{str(new_list[i])}')    ## for debugging
                        data[key][item_keys[i]] = new_list[i]
                    if i in [5, 10, 15]:
                        print('.'*100)
                print('-'*100)                                                              ## for debugging
                break
    return data

#%%
def change_data_through_input(value:int, header:list, result:list) -> str:
    value_to_change = header[value]
    old_value = result[value]

    layout = [
        [Text(f'The current value is: {old_value}')],
        [Input('', size=(40, 1), key='-INPUT CHANGE-', enable_events=True)],
        [Button('Submit change')]
    ]

    layout.append([Button('Exit')])
    window = Window(f'Update {value_to_change} of ID {result[0]}', layout, font=40,  modal=True, keep_on_top=True)
    
    copy_value_to_change = [value_to_change].copy()[0]
    while True:
        event, values = window.read()
        if event in ['Exit', WIN_CLOSED]:
            value_to_return:str = copy_value_to_change
            break
        if event == 'Submit change' and values['-INPUT CHANGE-'] != '':
            print(values['-INPUT CHANGE-'], type(values['-INPUT CHANGE-']))
            value_to_return:str = values['-INPUT CHANGE-']
            break
    window.close()
    return value_to_return

def change_data_popup(data_row:list, header_data:list, table_key:str, headings:list[str], update_button:str, window_title:str) -> list:
    """
    Modify a list in PySimpleGUI as a function of the header data.
    A window is opened to edit existing data. 
    The data is read into a table with data as the row headers and headings as the column headers

    Dependable on a global variable 'save_data' to be defined outside the function. 

    :param data_row: List to change. Must have same length as header_data
    :param header_data: List of headers (all strings)
    :param table_key: sg.Table() requires a key to function. Should be in the format '-KEY NAME-' to observe the general syntax.
    :param headings: list(str, str)
    :param update_button: Text for button for updates. Should be readable for humans.
    :param window_title: Title of the window. Should be readable for humans.
    """

    data_row_with_IDs = merge_two_arrays(header_data, data_row)
    headings = [header + ' '*20 for header in headings]
    layout = [
        [Table(values=data_row_with_IDs, 
                key=table_key,
                headings=headings,
                num_rows=len(data_row),
                col_widths=40,
                justification='left',
                hide_vertical_scroll=True,
                )],
        [Button(update_button, tooltip='Click here to update the database.'), 
        Button('Save changes', tooltip='Saves the changes and return to the main window. Only press if you are confident in the changes.')]
    ]

    layout.append([Button('Close', size=(10, 1))])
    window = Window(title=window_title, layout=layout, location=(150, 500), modal=True, keep_on_top=True)

    row_in_copy:list = data_row.copy()
    while True:
        event, values = window.read()
        if event in ['Close', WIN_CLOSED]:
            print('Data_row_copy: \n')
            final_row = row_in_copy
            break
        elif event == update_button:            
            if values[table_key]:
                change_index = values[table_key][0]
                changed_value = change_data_through_input(change_index, header_data, data_row)
                data_row[change_index] = changed_value
                window[table_key].update(values=merge_two_arrays(header_data, data_row))
        elif event == 'Save changes':
            final_row = data_row
            global save_data
            save_data[0] = True
            break

    window.close()    
    return final_row

#%%
def specific_data_popup(data_row:list, header_data:list) -> list:
    data_row_with_IDs = merge_two_arrays(header_data, data_row)
    layout = [
        [Table(values=data_row_with_IDs, 
                  key='-ROW DATA-',
                  headings=['Name', 'Current value'],
                  num_rows=len(data_row),
                  col_widths=40,
                  justification='left',
                  hide_vertical_scroll=True,
                  )],
        [Button('Update entry', tooltip='Click here to update the database.'), 
         Button('Save changes', tooltip='Saves the changes and return to the main window. Only press if you are confident in the changes.')]
    ]

    layout.append([Button('Close', size=(10, 1))])
    window = Window(title='Selected row', layout=layout, location=(150, 500), modal=True, keep_on_top=True)

    row_in_copy:list = data_row.copy()
    while True:
        event, values = window.read()
        if event in ['Close', WIN_CLOSED]:
            print('Data_row_copy: \n')
            final_row = row_in_copy
            break
        elif event == 'Update entry':
            change_index = values['-ROW DATA-'][0]
            if values['-ROW DATA-']:
                changed_value = change_data_through_input(change_index, header_data, data_row)
                data_row[change_index] = changed_value
                window['-ROW DATA-'].update(values=merge_two_arrays(header_data, data_row))
        elif event == 'Save changes':
            final_row = data_row
            global save_data
            save_data[0] = True
            break

    window.close()    
    return final_row

#%%

def main_window(storage_path):
    how_to_text = """Select a filter in the box to the left and press 'Update filter'.\n
Find the entry you wish to either view or change and highlight it by click on it and press 'Select entry'.\n
This will open a new window where you can update the current values. Select a row and press 'Update entry', which opens yet another window.\n
Type in the new value and press 'Submit change'. This will update the previous window. Now press 'Save changes' to save and close the updating window.\n
In the primary window press 'Save and exit' to save the new data. If you do not wish to save you changes, press 'Exit without saving'.\n
To delete an entry select it and press 'Delete entry'.\n
    """
    do_not_text = """**Change the ID.**

If you change its to an existing ID, it will OVERWRITE the chosen ID and CANNOT BE RESTORED!
    """

    sg_theme('DarkGrey')

    csv_file = get_newest_file(storage_path)
    data = csv_to_nested_dict(csv_file)

    font_general = ('Courier New', 8)
    font_text = ('Courier New', 10)
    font_header = ('Courier New', 20, 'bold')
    header_data = list(data[0].keys())
    sort_by_column = 'Plastic Type'
    unique_keys = find_unique_main_keys(data, sort_by_column)
    temp_lists = create_temporary_list(data)

    filter_data_layout = Listbox(unique_keys,
                    size=find_max_string(unique_keys, 15), 
                    key='-FILTER DATA-', no_scrollbar=False,
                    font=font_general)

    how_to_layout = Text(how_to_text ,size=(80, 15), font=font_text)
    do_not_layout = Text(do_not_text, size=(40, 15), font=font_text)

    filter_coloumn_layout =         [[Text('Filters', auto_size_text=True, font=font_header)], [filter_data_layout], [Button(button_text='Update filter')]]
    instructions_coloumn_layout =   [[Text('Instructions', auto_size_text=True, font=font_header)], [how_to_layout]]
    do_not_coloumn_layout =         [[Text('Do not', auto_size_text=True, font=font_header)], [do_not_layout]]

    col_h = cm2p(9.5)

    upper_layout = [
        [Column(filter_coloumn_layout,       scrollable=False,   size=(cm2p(7), col_h)), VerticalSeparator('Green'), 
        Column(instructions_coloumn_layout, scrollable=False,    size=(cm2p(18), col_h)), VerticalSeparator('green'),
        Column(do_not_coloumn_layout,       scrollable=False,    size=(cm2p(10), col_h))]
    ]

    table_layout = [
        [Table(values=temp_lists,
                headings=header_data,
                def_col_width=20,
                num_rows=15,
                auto_size_columns=True, 
                alternating_row_color='darkgrey',
                vertical_scroll_only=False,
                font=font_general,
                key='-TABLE-')],
        [HorizontalSeparator('green', pad=((0, 0),(5, 5)))],
        [Button('Select entry', button_color='blue'), Button('Add new entry', button_color='darkblue'), Button('Delete entry', button_color='DarkRed')]
    ]

    layout = [[upper_layout],
            [HorizontalSeparator('green', pad=((0, 0),(5, 5)))],      
            table_layout,
            ]

    layout.append([HorizontalSeparator('green', pad=((0, 0),(15, 5)))])
    layout.append([Button('Exit without saving', size=(25, 1), button_color='darkred'), 
                Button('Save and exit', size=(25, 1), button_color='darkgreen')])

    window = Window('Show database', layout, location=(100, 100), size=(1900, 1080), resizable=True, keep_on_top=False).finalize()

    keyword = 'Show all'
    result = create_temporary_list(data)
    data_copy = data.copy()
    while True:
        print('Save data: ', save_data)
        event, values = window.read()
        print(event, values)
        if event in ['Exit without saving', WIN_CLOSED]:
            save_data[1] = False
            data = data_copy
            break
        if event == 'Save and exit' and save_data[0]:
            save_data[1] = True
            break
        elif event == 'Update filter': #DO NOT DELETE!!!
            print('Update filer')
            if values['-FILTER DATA-']:
                keyword = values['-FILTER DATA-'][0]
                result = create_temporary_list(data, sort_by_column, keyword)
                window['-TABLE-'].update(values=result)
        elif event == 'Select entry':
            print('Select entry')
            if values['-TABLE-']:
                index_number = values['-TABLE-'][0] # bare et tal - angiver et specifikt 
                data_row = result[index_number]
                specific_data = change_data_popup(data_row, header_data, table_key='-ROW DATA-', headings=['Name', 'Current value'],
                                                    update_button='Update entry', window_title='Selected row')
                data = update_dict_with_list(data, specific_data)
                window['-TABLE-'].update(values=create_temporary_list(data, sort_by_column, keyword))
        elif event == 'Add new entry':
            print(event)
            # new_entry = change_data_popup()
            empty_list:list[str] = create_empty_list(data)
            new_list = change_data_popup(data_row=empty_list, header_data=header_data, table_key='-NEW VALUE-', headings=['Name', 'Current value'],
                                        update_button='New value', window_title='New entry')
            data = update_dict_with_list(data, new_list=new_list, new_entry=True)
            result = create_temporary_list(data, sort_by_column, keyword)
            window['-TABLE-'].update(values=result)
        elif event == 'Delete entry':
            # add popup as security!
            is_delete_ok = popup_ok_cancel('Do you wish to delete this entry?')
            print('ok_cancel?', is_delete_ok)
            if values['-TABLE-'] and is_delete_ok == 'OK':
                index_number = values['-TABLE-'][0] # bare et tal - angiver et specifikt 
                delete_entry = result[index_number][0] - 1
                data.pop(delete_entry)
                window['-TABLE-'].update(values=create_temporary_list(data, sort_by_column, keyword))
                save_data[0] = True
            pass
        print('Ended test', values)
    window.close()

    save_data_to_csv(data, storage_path, save_data)

#%%

storage_path = '../Basement Status/polymer_storage_files'
# storage_path = 'test_folder'
global save_data
save_data = [False, False]



main_window(storage_path)