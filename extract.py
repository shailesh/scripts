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

red = []
blue = []
date_list = []
time_list = []
device_id_list = []
values = []

red_red_values = []
red_green_values = []
red_blue_values = []
red_clear_values = []

blue_red_values = []
blue_green_values = []
blue_blue_values = []
blue_clear_values = []

filenames = []

def extract_data(log_file):
    led_data = False
    with open(log_file,'rU') as g:
        date_time_list = []
        rR = []
        rG = []
        rB = []
        rC = []
        bR = []
        bG = []
        bB = []
        bC = []
        date = []
        time = []
        
        value = 'Error'
        for i, row in enumerate(g):

            if "Packet type 03:" in row:
                led_data = True
                led_color = 'RED'

            elif "Packet type 04:" in row:
                led_data = True
                led_color = 'BLUE'

            elif "Device ID:" in row:
                device_id = int(row.split("Device ID:")[1])

            elif "INSERT_STRIP" in row:
                date_time_string = (row.split("INSERT_STRIP"))[0]
                date_time_list = date_time_string.split()
                date = date_time_list[0]
                time = date_time_list[1]

            elif "updateUI(): 4, with data:" in row:
                value = float(row.split("updateUI(): 4, with data:")[1])
                
            elif "updateUI() with state: 4, data:" in row:
                value = float(row.split( "updateUI() with state: 4, data:")[1])

            elif "Temp" in row:
                temp_value = row.split("Temp: ")[1].rstrip()
                print temp_value

            elif led_data and "RGBC data:" in row:
                rgbc_values = row.split("RGBC data: [")[1].rstrip().split(', ')
                #print rgbc_values
                if led_color == "BLUE":
                    #bR.append(float(rgbc_values[0]))
                    #bG.append(float(rgbc_values[1]))
                    #bB.append(float(rgbc_values[2]))
                    bC.append(float(rgbc_values[3].split(']')[0]))

            elif "Could not decode packet" in row:
                value = "ERROR"
         

        #red_red_values.append(np.mean(rR))
        #red_green_values.append(np.mean(rG))
        #red_blue_values.append(np.mean(rB))
        #red_clear_values.append(np.mean(rC))
        
        #blue_red_values.append(np.mean(bR))
        #blue_green_values.append(np.mean(bG))
        #blue_blue_values.append(np.mean(bB))        
        blue_clear_values.append(np.mean(bC))

        date_list.append(date)
        time_list.append(time)
        device_id_list.append(device_id)
        
        # print device_id

    with open (os.path.join(folder_path, "Ainax_data.csv"),'wb') as s:
        csvwriter = csv.DictWriter(s,fieldnames=['Filename','Device ID','date', 'Time', 'UV Clear'])
        csvwriter.writeheader()
        rows = zip(filenames,device_id_list,date_list,time_list, blue_clear_values)
        for row in rows:
            csvwriter.writerow({'Filename':row[0],'Device ID':row[1],'date':row[2],'Time':row[3], 'UV Clear':row[4]})
        # print "Extraction Done"

def extract_log_files(file_path):
    for i, logfile in enumerate(glob(os.path.join(file_path, '*.txt'))):
        with open(logfile,'rU') as f:
            for i, row in enumerate(f):
                if "I/AinaRunner: ANALYZING_SAMPLE" in row:
                    filenames.append(os.path.basename(logfile))
                    extract_data(logfile)
                else:
                    continue

extract_log_files(path)