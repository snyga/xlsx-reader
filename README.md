# xlxs_reader
Graphical User Interface (GUI) for a database written in excel (xlsx).
At the moment the xlsx had the need for the first header to be ' ID '. There must also be a header named 'Plastic Type'.

# How to install
## Download and ready for use as is (Windows 10, 11):
  * Go ahead and download the edit_status_0.2.exe and it should be ready to use. You need to place it next to a folder named `polymer_storage` to work.

## Install with PyInstaller (not windows): 
* Download `edit_status_0.2.py` and place it in the same directory as your xlsx files. 
  * Install PyInstaller with `pip install pyinstaller` [PyInstaller](https://pyinstaller.org/en/stable/).
  * In your terminal run the following line: `pyinstaller --noconfirm --onefile --clean --distpath "C:/Users/username/Basement Status/polymer_storage/" --console --hidden-import "openpyxl.cell._writer" --collect-submodules "openpyxl"  "C:/Users/username/Basement Status/polymer_storage/edit_status_0.2.py"`

### Requirements for installation
PySimpleGUI and PyInstaller.

# Goals
To make the GUI a lot more general so it can read any kind of xlsx based database. 

# License
Licensed under MIT 3.0
