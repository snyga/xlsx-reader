"""
pyinstaller_cmd = 'pyinstaller --noconfirm --onefile --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/edit_status_0.2.py"'
'pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement Status/polymer_storage/" --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/py/edit_status_0.2.py"'
'pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/Basement Status/polymer_storage/" --console "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/py/edit_status_0.3.py"'
"""
#%%
import subprocess
import os
import shutil
import sys

def import_or_install(package:str):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        print(installed_packages)

def combine_argument_and_argname(arg:str, argnames:list[str]) -> str:
    return ''.join([f'{arg} ' + f'"{argname}"' + ' ' for argname in argnames])

check_packages = {'PyInstaller':  {'install_line': 'pyinstaller', 'keywords': ['-U'] },
                  'PySimpleGUI': {'install_line': 'pysimplegui', 'keywords': []}
                  }

for key, item in check_packages.items():
    package = item['install_line']
    import_or_install(package)


abs_path = os.path.abspath('..') 
script_name = '"\edit_status_0.3.py"'

hidden_modules = ['openpyxl.cell._writer']
hidden_import = combine_argument_and_argname('--hidden-import', hidden_modules)

submodules = ['openpyxl']
collect_submodules = combine_argument_and_argname('--collect-submodules', submodules)

no_confirm = '--noconfirm'
no_clutter = '--clean'
one_file = '--onefile'
one_dir = '--onedir'
console = '--console'

py_to_exe_path = 'edit_status_0.3.py'

input_list = ['pyinstaller', no_confirm, one_file, console, no_clutter, py_to_exe_path]
[print(item) for item in input_list]
process = subprocess.run(input_list, check=True, stdin=True, capture_output=True,
                         text=True)
print(process.check_returncode())

source = f'./dist/{py_to_exe_path.replace(".py", ".exe")}'
destination = f'./Basement_Status/{py_to_exe_path.replace(".py", ".exe")}'

print('Removing previous installation from Basement_Status')
if os.path.exists(destination):
    os.remove(destination)

print('Moving new installation to Basement_Status')
if os.path.isfile(source):
    shutil.move(source, destination)

print('Removing clutter from xlsx-reader')
list_dir = os.listdir()
for directory in ['build', 'dist']:
    if directory in list_dir:
        shutil.rmtree(directory)

for file in list_dir:
    if file.endswith('.spec'):
        os.remove(file)        



## find ud af at omdanne filerne til et zipformat i stedet - 
## 0: Download zipfil
## 1: Åben zipfil
## 2: Find den nyeste fil
## 3: Lav eventuelle opdateringer
## 4: Gem nyeste, slet ældste og zip det hele igen.
## 5: Upload til 
