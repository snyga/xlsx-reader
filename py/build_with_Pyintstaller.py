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
dist_path = f'--distpath {dist}'

temp_dir = abs_path + 'temp'
work_path = f'--workpath {temp_dir}'

hidden_modules = ['openpyxl.cell._writer']
hidden_import = combine_argument_and_argname('--hidden-import', hidden_modules)

submodules = ['openpyxl']
collect_submodules = combine_argument_and_argname('--collect-submodules', submodules)

no_confirm = '-y'
no_clutter = '--clean'
one_file = '-F'
one_dir = '-D'
console = '--console'

'pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement/" --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/edit_status_0.2.py"'

py_to_exe = 'py/edit_status_0.2.py'
py_to_exe_path = abs_path + py_to_exe


pyinstaller_cmd = 'pyinstaller' + ' '.join(['pyinstaller',
                      no_confirm, one_file, no_clutter, console,
                      dist_path,
                      hidden_import, collect_submodules,
                      py_to_exe_path])
# print(pyinstaller_cmd)
print(subprocess.run([pyinstaller_cmd],shell=True, stdout=True))

