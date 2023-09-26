#%%
from sys import argv
from timeit import timeit
import subprocess
start = timeit()

def combine_argument_and_argname(arg:str, argnames:list[str]) -> str:
    return ''.join([f'{arg} ' + f'"{argname}"' + ' ' for argname in argnames])

pyinstaller_cmd = 'pyinstaller --noconfirm --onefile --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/edit_status_0.2.py"'

abs_path = "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/"
program_path = abs_path + "challenges.py"
dist = abs_path + "Basement Status"
dist_path = f'--distpath "{dist}"'

temp_dir = abs_path + 'temp'
work_path = f'--workpath "{temp_dir}"'

hidden_modules = ['openpyxl.cell._writer']
hidden_import = combine_argument_and_argname('--hidden-import', hidden_modules)

submodules = ['openpyxl']
collect_submodules = combine_argument_and_argname('--collect-submodules', submodules)

no_confirm = '--noconfirm'
no_clutter = '--clean'
one_file = '--onefile'
one_dir = '--onedir'
console = '--console'

# 'pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement Status/polymer_storage/" --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/py/edit_status_0.2.py"'
# 'pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement Status/polymer_storage/" --console "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/py/edit_status_0.2.py"'
py_to_exe = 'py/edit_status_0.2.py'
py_to_exe_path = f'"{abs_path + py_to_exe}"'


pyinstaller_cmd = 'pyinstaller ' + ' '.join([
                      no_confirm, 
                    #   one_file, 
                    #   no_clutter, 
                    #   dist_path, 
                    #   console,
                    #   hidden_import, 
                    #   collect_submodules,
                      py_to_exe_path])

pyinstaller_args = ['pyinstaller',
                    #   no_confirm, 
                    #   one_file, 
                    #   no_clutter, 
                    #   dist_path, 
                    #   console,
                    #   hidden_import, 
                    #   collect_submodules,
                        'edit_status_0.2.py'
                    #   py_to_exe_path
                      ]

print(pyinstaller_args)
# process = subprocess.run('pyinstaller.exe ".\hello_word.py"', shell=True, stdout=True, stderr=True,
#                          input=b'Finished?', check=True)

subprocess.run('pyinstaller -y -F --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement Status" --console --hidden-import "openpyxl.cell._writer"  --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/py/edit_status_0.2.py"', 
               stderr=True, stdout=True, check=True)