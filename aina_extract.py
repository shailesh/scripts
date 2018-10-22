import sys
import os
import numpy as np
import scipy as sp
import csv
from glob import glob
import Tkinter as tk
import FileDialog
from tkFileDialog import askdirectory

root = tk.Tk()
root.withdraw()
folder_path = askdirectory()
path = folder_path

device_id_list = []
reading_list = []


filenames = []

def extract_log_files(file_path):
    for i, logfile in enumerate(glob(os.path.join(file_path, '*.txt'))):
        with open(logfile,'rU') as f:
            reading_value=[]
            device_id=[]
            for i, row in enumerate(f):
                if "Device ID: " in row:
                    device_id = row.split("Device ID: ")[1].rstrip('\n')

                if "updateUI() with state: 4, data: " in row:
                    reading_value = row.split("updateUI() with state: 4, data: ")[1].rstrip('\n')   

            device_id_list.append(device_id)
            reading_list.append(reading_value)
            filenames.append(os.path.basename(logfile))
            with open (os.path.join(folder_path, "Aina_data.csv"),'wb') as s:
                csvwriter = csv.DictWriter(s,fieldnames=['Filename','Device ID', 'Reading'])
                csvwriter.writeheader()
                rows = zip(filenames,device_id_list, reading_list)
                for row in rows:
                    csvwriter.writerow({'Filename':row[0],'Device ID':row[1], 'Reading': row[2]})
                print "Extraction Done"

extract_log_files(path)
