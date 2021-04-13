import tkinter as tk
from tkinter import filedialog
import os
import sys
import shutil

ICON = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADcklEQVQ4jR2TS29bVRSF1zn3aV8/
4ziO09ipE0cxVXAJlEppghjQph0wRVRUQYAE/RXMmDJhhkBi1HEFAipBKyExADXi0ZaUtEqCGyfx
K46vfX19n+ccFO/pltZaWvvbBEQFAZCNKj9SinU3BFSJgAuBgAlEZfqbA1w3Qw6JEDAvQDKuYr1a
hBpPQ5aJhIhKkYhqWs8N45bngXEAEFBkCZYfbmQMeeNSzvhJlimGlovMbBaypiBkHDTkHq5cnse9
rz/8/L21Ahj3UM0bWJ1LIAjZOIkqyeWcoQCug+lcEvmpBITAeCedOUmuBwR89MasevvJfk8tJTVc
XUziwV4PEhjmJlJJJ6rX2x17X0nEoOsKxkMVSDeWi5Vbb5bv/LvbvnWxlJkyWKgNHQ9Dj6PWdqAJ
gpVXZ4v5Qvr9QnHypgBJgPOHnHFGFA3SZ7evbm2PxGtbfx0UprOGVi3G0OjaaJw66HVtlC9X8O7N
VaR1Ck3lk9mp5FtaVNt0ff40YHRfsnyyOdyrzSzlVcYI/UpS5PyjupUI3QBdquODT64jRjheHDbh
2D4Y4xCEpmLJ+CaE+JsqrvVpdSmLj9+uSrblbX9579lFBeFHwmMPLrw8j0ycYne/DtfxEYQCp1aA
9qmD0+4Auk7v0he1npaLJnDnfg3/HIdfGKVzMfck+GbnqP/nhZVFyJKGkAn4XoAT00Gz6yLkBB4T
aHcsTk/UyNr9b3dw9+dt2AkD5eXSL66gOD83k8vNZOF6HD3ThmUHMIchBMhY0LYDDG1vJJUr5x6V
Li29MzE7lep7HsKhl8oUM9cmFgvrukwiUUWg2Wij0R4hgIJ4IgrbdnF41EWnO/Tp/GSkbUyoV8qv
zB9pkoRWsweT0bWtx7U0D3wM+iYOj030RwxG3IBp2mi3TAyGLk56I9DsVAY6DxtiMFhZrs7X05kE
Hv6+g/xkCnOFNB4/2RuXxokE3/fRbJkwLReuHyKiy5Cf/7GLiCaj2+l3iuXC6ysrle+ePj+uVBZy
xDQH8Z45gqQo0KM6Wq0+XPfslAISoSBnjSzEVTDOcQa3osowprPYuLZaXFrIPPv+h1/1+vEAqhHH
ZDYFxhgODjo46VpjkbNfkPVcYow1oQQjP4B11MBL+VR+v94S/9U6lsMVlGZiKJ3PodXqYSIdg+P4
GFguIGD9D5+etJD+Hg2ZAAAAAElFTkSuQmCC=="""


def get_list_of_files(dir_name):
    all_files = list()
    for (root, _, files) in os.walk(dir_name):
        for f in files:
            all_files.append(os.path.join(root, f))

    return all_files


t_root = tk.Tk()
img = tk.PhotoImage(data=ICON)
t_root.tk.call('wm', 'iconphoto', t_root._w, img)
t_root.withdraw()

game_exe_path = filedialog.askopenfilename(title="Select the game's executable", filetypes=(
    ("Executable", "*.exe"), ("All Files", "*.*")))
game_path = os.path.dirname(game_exe_path)
backup_path = os.path.join(game_path, 'Backup')
if game_exe_path == "" or not os.path.exists(backup_path):
    print("The game's executable was either incorrect or you have no 'Backup' folder.")
    sys.exit()

backed_up_files = get_list_of_files(backup_path)

# files that aren't in the game normally
if os.path.exists(f'{backup_path}/backup_exclude.txt'):
    with open(f'{backup_path}/backup_exclude.txt') as f:
        excluded_from_backup = f.read().splitlines()

    # remove duplicates
    excluded_from_backup = list(dict.fromkeys(excluded_from_backup))
    i = 0
    while i < len(excluded_from_backup):
        try:
            os.remove(os.path.join(game_path, excluded_from_backup[i]))
        except(FileNotFoundError):
            print(f'{excluded_from_backup[i]} is already deleted, skipping...')

        i += 1

i = 0
print('Restoring original files...')
while i < len(backed_up_files):
    file_relative_path = os.path.relpath(
        backed_up_files[i], backup_path)  # get relative path
    shutil.move(os.path.join(backup_path, file_relative_path),
                os.path.join(game_path, file_relative_path))
    i += 1

shutil.rmtree(backup_path)
print('Backup restored.')
os.system('pause')
