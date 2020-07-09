# !/usr/bin/env python
# encoding: utf-8

'''
A script to collect the project_save.tmx and glossary.txt files of
OmegaT projects and copy them to a centralized location for ease of
reference between projects or to facilitate their import into other
CAT tools.

The script creates subfolders with the original project name into a
user-selected central folder, and also renames the files to match
the name of the project.

@author: Philippe Tourigny
@last modified: 2020-07-09
'''

import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog


def select_path(startpath, title):
    '''Present user with a dialog to choose the starting folder'''

    rootWin = tk.Tk()
    rootWin.attributes('-topmost', True)
    rootWin.withdraw()

    return filedialog.askdirectory(initialdir=startpath, title=title)


def build_project_list(searchpath, pattern):
    '''Build a list of all OmegaT projects in the search path'''

    # TODO: Figure out how to ignore team projects correctly
    # ignore = '.repositories' # Discard team projects

    project_list = [omt.parent for omt in searchpath.rglob(pattern)]

    return project_list


def copy_project_data(destination, projects, memory, glossary):
    '''Copy the project_save.tmx and glossary.txt files to individual
       project folders in the destination path, renaming them to match
       the project name'''

    for project in projects:
        # Retrieve the project name and the memory and glossary files
        name = project.parts[-1]
        prjfiles = (Path(project, memory), Path(project, glossary))

        for prjfile in prjfiles:
            if prjfile.exists():
                project_folder = Path(destination, name)
                project_folder.mkdir(parents=True, exist_ok=True)
                newfile = Path(destination, name, name+prjfile.suffix)
                print('Copying '+str(prjfile)+' to '+' '+str(newfile))
                shutil.copy(prjfile, newfile)


# Define constants
HOME = Path.home()
TAOPATH = Path(HOME, 'Documents/Dossiers/TAO/')
DESTPATH = Path(HOME.anchor,'CAT_Data')

PROJECT = 'omegat.project'
MEMORY = 'omegat/project_save.tmx'
GLOSSARY = 'glossary/glossary.txt'

project_path = Path(select_path(TAOPATH, 'Select starting folder'))

projects = build_project_list(project_path, PROJECT)

destination = Path(select_path(DESTPATH, 'Select destination folder'))
copy_project_data(destination, projects, MEMORY, GLOSSARY)
