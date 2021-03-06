import tkinter as tk
from tkinter import filedialog
import os
import shutil
import subprocess
import sys

ICON = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADQklEQVQ4jU2SyW8cVRDGv7f09Ez3
9CzYeItNotjEdmJMHILBCKEExMWIC4fkhBBS7oQbEgfgkH8AiXsQkTjAEa5A4IIAgRIRQqREcTwz
XpjpHnfP0v36bWhGEaJUqkNJ9dWvFrJ5+hj+b8Za1P3CxZrvbD4xUfo+PUh+2dp+HSvnlpGnAiee
mkWaCTx42IC1AHdG8bERQqC0fdlK/R3VHFRqPNrvv33O0BucUxjGUCy6yEQOIQQACi7VYwE7ErCQ
yn4aSgmhLI4GOSTRX+gk+qAeeD8JRleiTrsG6vy5MD//rjZacZ3r/wgsbKknzMaom2commGO7fUJ
LAXpmVt3ds4cthoghGLrhfWz1Wp1d+8g/JDzUmFcTCmBlPqkycR4lCwfEShAKETdPu7EO/j95z9Q
9HwElTKWTx2/muf5R9wU6FjAAKhWK2/FvRBKGQhC0AozPIp9ZPdD7DsajWYXjCfohAnWHeZ1w/g8
90suQMYOyuizllG02gk4Z7hycQ5rxzzcuHmA8pyGpRSUELguHzf1PfcZ7vvuaP/gDBgM1eJIoFx0
sFTheH66iEY7xX43w2xdwCu5GA4yCCFhjEGtGhzn/V4KrTTKfqFScourjsMxMx2gxIHrN1vja7ie
A6E1OKWw1iCKetDGQGq9wCefDJBlEkGJPy0UdYsuQ9zLAc9FLIAxHzEgxsJSgrJfRJYJKKmRpdkM
7TXaODFVBmF8lVgzegdwSsAYAeMMBBaEYIxNxnmGYSZx2O7CKxVqdPBPhLWFGizjK0OhwBltcko+
pqNiCtyLYux0uthttNE9GuDgsAuZSyS9FEl/WOfbW/Nr52dLn//6dzh7O0rhMxLlmfzEUnq5OllZ
vbSxhHo9gCFA0k8ReA4KBTYm1Ro19s5L89fuNodvfPnbfvDK8gQCq384jMXXrXZcfXVz+bX333sT
rsexvDSH5zZOQmqF8GiAo14K7jg+n674V/66F6PWi+DLGiIhv8mFRFnhs6QTX7v+1Y9oNkPcvtvC
6tIMrFZ4uNNONs4uRplQt8jVC6e+TQbp5owZiPuq0NlnfFvGYk9ECrtCXgiHafDi6bniYt1xHuxG
DeZ7e32h2nMLU8nkVB3/AhJ1lqM/VaYaAAAAAElFTkSuQmCC=="""


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

# get paths
MOD_PATH = "files"
if not os.path.exists(MOD_PATH):
    print(
        f'Folder "{MOD_PATH}" not found. Did you extract all the files from the archive?')
    os.system('pause')
    sys.exit()

game_exe_path = filedialog.askopenfilename(title="Select the game's executable", filetypes=(
    ("Executable", "*.exe"), ("All Files", "*.*")))
game_path = os.path.dirname(game_exe_path)
if game_exe_path == "" or not os.path.exists(os.path.join(game_path, 'data')):
    print("The game's executable was either incorrect or unspecified.")
    sys.exit()
partool_path = filedialog.askopenfilename(
    title="Select the ParTool/ParManager executable", filetypes=(("Executable", "*.exe"), ("All Files", "*.*")))
if partool_path == "":
    print('ParTool executable was not specified.')
    sys.exit()

backup_folder = os.path.join(game_path, 'Backup')

# files that aren't in the game normally
if os.path.exists(f'{MOD_PATH}/backup_exclude.txt'):
    with open(f'{MOD_PATH}/backup_exclude.txt') as f:
        excluded_from_backup = f.read().splitlines()
else:
    excluded_from_backup = []


# replace files
replace_files_path = os.path.join(MOD_PATH, 'replace')
replacer_files = get_list_of_files(replace_files_path)
print('Replacing files...')
i = 0
while i < len(replacer_files):
    file_relative_path = os.path.relpath(
        replacer_files[i], replace_files_path)  # get relative path
    try:
        if file_relative_path not in excluded_from_backup:
            os.makedirs(os.path.dirname(os.path.join(backup_folder,
                        file_relative_path)), exist_ok=True)  # make backup dir
            os.rename(os.path.join(game_path, file_relative_path), os.path.join(
                backup_folder, file_relative_path))  # move files to backup dir
    except(FileNotFoundError):
        cont = input(
            f'{file_relative_path} not found\nType "y" to continue and "n" to stop.\n')
        if cont.lower() == 'y':
            print('Continuing...')
        else:
            print('Quitting...')
            sys.exit()
    except(FileExistsError):
        print(f'Backup for {file_relative_path} exists already, skipping.')
    shutil.copy(os.path.join(replace_files_path, file_relative_path),
                os.path.join(game_path, file_relative_path))
    i += 1

with open(f'{backup_folder}/backup_exclude.txt', 'a') as f:
    for row in excluded_from_backup:
        f.write(f'{row}\n')

# get par files
add_files_path = os.path.join(MOD_PATH, 'add')
add_files = get_list_of_files(add_files_path)
i = 0
par_list = []
while i < len(add_files):
    file_relative_path = os.path.relpath(add_files[i], add_files_path)
    par_only = f'{file_relative_path.split(".par",1)[0]}.par'
    par_list.append(par_only)
    i += 1

# remove duplicates
par_list = list(dict.fromkeys(par_list))

# add files
print('Adding files to .par archives...')
i = 0
while i < len(par_list):
    try:
        os.makedirs(os.path.dirname(os.path.join(
            backup_folder, par_list[i])), exist_ok=True)
        os.rename(os.path.join(game_path, par_list[i]), os.path.join(
            backup_folder, par_list[i]))
    except(FileNotFoundError):
        print(f'{par_list[i]} not found. Did you select the correct path?')
        os.system('pause')
        sys.exit()
    except(FileExistsError):
        print(f'Backup for {par_list[i]} exists already, skipping.')
    subprocess.run(
        f'"{partool_path}" add "{os.path.join(backup_folder, f"{par_list[i]}")}" "{os.path.join(add_files_path, par_list[i])}" "{os.path.join(game_path, par_list[i])}"', check=True)
    i += 1

print(f'Old files were backed up to {backup_folder}')
print('Install complete.')
os.system('pause')
