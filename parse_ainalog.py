import sys
import os
import numpy as np
import scipy as sp
import csv
from glob import glob
import Tkinter as tk
import FileDialog
from tkFileDialog import askdirectory
import re


root = tk.Tk()
root.withdraw()
folder_path = askdirectory()
path = folder_path

# sub_dir =[]

# files = os.listdir(folder_path)
# for name in files:
    # sub_dir =[]
    # sub_path = '/home/shailesh/ainalog/'+name
    # sub_dir.append(sub_path)

    # print (sub_dir[0])
    # path = sub_dir[0]

    # path = '/home/shailesh/Documents/no_device_id'

# path = [i for i in sub_dir]

# print path


filenames = []
device_id_list = []
reading_list = []
time_stamp_start_list =[]
time_stamp_end_list = []
error_string_list =[]
status_list =[]
phone_model_list = []
app_version_list = []
platform_list = []
os_version_list = []
lot_code_list = []
test_type_list = []
blank_strip_blue_led_value_list = []
blank_strip_red_led_value_list = []
packet_decode_count_list = []
packet_decode_failure_count_list = []

def extract_log_files(file_path):
    for i, logfile in enumerate(glob(os.path.join(file_path, '*.txt'))):
        with open(logfile,'rU') as f:
            red_value = 'none'
            blue_value = 'none'
            reading_value="none"
            device_id="none"
            time_stamp_start = "none"
            time_stamp_end = "none"
            error_string = "none"
            status = "none"
            phone_model = "none"
            app_version = "none"
            platform = "none"
            os_version = "none"
            lot_code = "none"
            test_type = "none"
            blank_strip_led_value = []
            red_blue_value = "none"
            string_hello_message="Hello message"
            string_packet_found="Packet: Received data of length"
            string_decode_failure="Could not decode packet"
            string_packet_decoded="AinaRunner: Packet type "
            string_error = ""
            packet_decode_failure_count=0
            packet_found_count=0
            packet_decode_count=0
            packet_hello_message_count=0
            i =0

            for i, row in enumerate(f):
                if "Device ID: " in row:
                    device_id = row.split("Device ID: ")[1].rstrip('\n')

                if "updateUI() with state: 4, data: " in row:
                    reading_value = row.split("updateUI() with state: 4, data: ")[1].rstrip('\n')

                if "I/AinaRunner: Start runnerLoop()" in row:
                    time_stamp_start = row.split("I/AinaRunner: Start runnerLoop()")[0]
                
                if "I/AinaRunner:" in row:
                    time_stamp_end = row.split("I/AinaRunner:")[0]

                a = error_def(i,row)
                if a!=0:
                    if re.search(pattern="WARNING",string=a,flags=0)==None:
                        error_string = a
                        status = "Error"
                        break
                    else:
                        error_string = a
                        status = "Warning"

                elif a==0:
                    error_string = "No_Error"
                    status = "Pass"
                
                if "Phone model: " in row:
                    phone_model = row.split("Phone model: ")[1].rstrip('\n')

                if "Android ver:" in row:
                    platform = "Android"
                    os_version = row.split("Android ver:")[1].rstrip('\n')

                if "App ver:" in row:
                    app_version = row.split(",")[0].split("ver: ")[1].rstrip('\n')

                if "Last processor values: " in row:
                    red_blue_value = row.split("Last processor values: ")[1].rstrip('\n')
                    blank_strip_led_value.append(red_blue_value.split(" "))
                    red_value = blank_strip_led_value[0][0]
                    blue_value = blank_strip_led_value[0][1]

                if "config file: " in row:
                    config = row.split("config file: ")[1].rstrip('\n')
                    decode = config.split("_")
                    if len(decode) == 2:
                        lot_code = decode[1]
                        test_type = decode[0]
                    elif len(decode) == 3:
                        lot_code = decode[2]
                        test_type = decode[0] + "_" + decode[1]

                if row.find(string_hello_message) >= 0:
                    packet_hello_message_count+=1
                if packet_hello_message_count > 0:
                    if row.find(string_packet_found) >= 0: 
                        packet_found_count+=1
                    if row.find(string_decode_failure) >= 0: 
                        packet_decode_failure_count+=1
                    if row.find(string_packet_decoded) >= 0: 
                        packet_decode_count+=1
                    s= row.split()
                    n= len(s)
                    if n==0:
                        break

                i = i+1

            filenames.append(os.path.basename(logfile))
            device_id_list.append(device_id)
            reading_list.append(reading_value)
            time_stamp_start_list.append(time_stamp_start)
            time_stamp_end_list.append(time_stamp_end)
            error_string_list.append(error_string)
            status_list.append(status)
            phone_model_list.append(phone_model)
            app_version_list.append(app_version)
            platform_list.append(platform)
            os_version_list.append(os_version)
            lot_code_list.append(lot_code)
            test_type_list.append(test_type)
            blank_strip_red_led_value_list.append(red_value)
            blank_strip_blue_led_value_list.append(blue_value)
            packet_decode_count_list.append(packet_decode_count)
            packet_decode_failure_count_list.append(packet_decode_failure_count)

            with open (os.path.join(folder_path, device_id+".csv"),'wb') as s:
                csvwriter = csv.DictWriter(s,fieldnames=['Filename','Device ID', 'Reading', 'Start Time', 'End Time', 'Error String', 'Status', 'Phone Model', 'App Verson', 'Platform', 'Os Version', 'Lot Code', 'Test Type', 'Blue Bank Strip', 'Red Blank Strip', 'Packet Decode Count', 'Packet Decode Failure Count' ])
                csvwriter.writeheader()
                rows = zip(filenames, device_id_list, reading_list, time_stamp_start_list, time_stamp_end_list, error_string_list, status_list, phone_model_list, app_version_list, platform_list, os_version_list, lot_code_list, test_type_list, blank_strip_blue_led_value_list, blank_strip_red_led_value_list, packet_decode_count_list, packet_decode_failure_count_list )
                for row in rows:
                    csvwriter.writerow({'Filename':row[0],'Device ID':row[1], 'Reading': row[2], 'Start Time': row[3], 'End Time': row[4], 'Error String': row[5], 'Status': row[6], 'Phone Model': row[7], 'App Verson': row[8], 'Platform': row[9], 'Os Version': row[10], 'Lot Code': row[11], 'Test Type': row[12], 'Blue Bank Strip': row[13], 'Red Blank Strip': row[14], 'Packet Decode Count': row[15], 'Packet Decode Failure Count': row[16] })
                print ("Extraction Done" + logfile)

def error_def(line,row):
    output = 0

    if "ERROR_EXPIRED_SERVER_CHECKIN" in row:
        output = "ERROR_EXPIRED_SERVER_CHECKIN"
    if "ERROR_UNSUPPORTED_DEVICE_MODEL" in row:
        output = "ERROR_UNSUPPORTED_DEVICE_MODEL"
    if "ERROR_UNSUPPORTED_OS_OLD" in row:
        output = "ERROR_UNSUPPORTED_OS_OLD"
    if "ERROR_UNSUPPORTED_OS_NEW" in row:
        output = "ERROR_UNSUPPORTED_OS_NEW"
    if "ERROR_UNSUPPORTED_APP_VERSION" in row:
        output = "ERROR_UNSUPPORTED_APP_VERSION"
    if "ERROR_UNSUPPORTED_APP_VERSION_UPDATE_AVAILABLE" in row:
        output = "ERROR_UNSUPPORTED_APP_VERSION_UPDATE_AVAILABLE"
    if "WARNING_NO_INTERNET_CONNECTION" in row:
        output = "WARNING_NO_INTERNET_CONNECTION"
    if "ERROR_INVALID_CODE" in row:
        output = "ERROR_INVALID_CODE"
    if "ERROR_CODE_CONFIRMATION_FAILED" in row:
        output = "ERROR_CODE_CONFIRMATION_FAILED"
    if "ERROR_CONFIG_SETUP_FAILURE" in row:
        output = "ERROR_CONFIG_SETUP_FAILURE"
    if "WARNING_PACKET_TIMEOUT" in row:
        output = "WARNING_PACKET_TIMEOUT"
    if "ERROR_PACKET_TIMEOUT" in row:
        output = "ERROR_PACKET_TIMEOUT"
    if "ERROR_DEVICE_REMOVED" in row:
        output = "ERROR_DEVICE_REMOVED"
    if "ERROR_APP_VERSION" in row:
        output = "ERROR_APP_VERSION"
    if "ERROR_DEVICE_MALFUNCTION" in row:
        output = "ERROR_DEVICE_MALFUNCTION"
    if "WARNING_LOW_VOLUME" in row:
        output = "WARNING_LOW_VOLUME"
    if "ERROR_LOW_SAMPLE_VOLUME" in row:
        output = "ERROR_LOW_SAMPLE_VOLUME"
    if "WARNING_BATTERY_LOW" in row:
        output = "WARNING_BATTERY_LOW"
    if "ERROR_BATTERY_LOW" in row:
        output = "ERROR_BATTERY_LOW"
    if "WARNING_TEMPERATURE" in row:
        output = "WARNING_TEMPERATURE"
        #WARNING LOW OR HIGH TO BE UPDATED
    if "ERROR_TEMPERATURE" in row:
        output = "ERROR_TEMPERATURE"
    if "WARNING_OUT_OF_RANGE" in row:
        output = "WARNING_OUT_OF_RANGE"
        #Low or High
    if "ERROR_OUT_OF_RANGE" in row:
        output = "ERROR_OUT_OF_RANGE"
        #Low or high
    if "ERROR_TIMEOUT" in row:
        output = "ERROR_TIMEOUT"
    if "ERROR_STRIP_MOVED" in row:
        output = "ERROR_STRIP_MOVED"
    return output

extract_log_files(path)
