#%%
from sys import argv
from timeit import timeit
import subprocess
start = timeit()

pyinstaller_cmd = 'pyinstaller --noconfirm --onefile --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/SD38JP/OneDrive - Aalborg Universitet/Dokumenter/Basement/xlsx-reader/edit_status_0.2.py"'



import PyInstaller

print(dir(PyInstaller))


