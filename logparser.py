import urllib
import os
import shutil
import re
import sys
# sys.path.insert(0, '/Music/diabeta')

def log_parser(log_file):
    device_id = "none"
    time_stamp_start = "none"
    time_stamp_end = "none"
    error_string = "none"
    status = "none"
    phone_model = "none"
    data = "none"
    app_version = "none"
    platform = "none"
    os_version = "none"
    lot_code = "none"
    test_type = "none"
    metadata = "none"
    date_recorded = "2018-02-18 02:50:00.123+05:30"
    date_created = "2018-02-18 02:50:00.123+05:30"
    date_modified = "2018-02-18 02:50:00.123+05:30"
    uuid = "none"
    r0=0
    r1=0
    r2=0
    r3=0
    with open(log_file,'rU') as g:
        for i,row in enumerate(g):
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
                error_string = "No error"
                status = "Pass"

            if "Phone model: " in row:
                phone_model = row.split("Phone model: ")[1].rstrip('\n')

            if "Android ver:" in row:
                platform = "Android"
                os_version = row.split("Android ver:")[1].rstrip('\n')

            if "App ver:" in row:
                app_version = row.split(",")[0].split("ver: ")[1].rstrip('\n')

            if "Device ID:" in row:
                device_id = int(row.split("Device ID:")[1])

            if "data:" in row:
                data = row.split("data: ")[1].rstrip('\n')

            if "config file: " in row:
                config = row.split("config file: ")[1].rstrip('\n')
                decode = config.split("_")
                if len(decode) == 2:
                    lot_code = decode[1]
                    test_type = decode[0]
                elif len(decode) == 3:
                    lot_code = decode[2]
                    test_type = decode[0] + "_" + decode[1]


            # if "Red LED calib: [" in row:
            #     x = row.split("Red LED calib: [")[1]
            #     arr = x.split("],")[0]
            #     arr2 = arr.split(',')
            #     r0 = int(arr2[0])
            #     r1 = int(arr2[1])
            #     r2 = int(arr2[2])
            #     r3 = int(arr2[3])
            #     if r0!=1 and r1!=1 and r2==1 and r3==1:
            #         analyte = 'A1C'
            #     elif r0==1 and r1==1 and r2!=1 and r3!=1:
            #         analyte = 'GLU'
            #     elif r0==1 and r1==1 and r2==1 and r3==1:
            #         analyte = 'HB'
            #     elif r0!=1 and r1!=1 and r2!=1 and r3!=1:
            #         analyte = 'Lipids'

    # from collections import OrderedDict
    # output_dict = OrderedDict()
    output_dict = dict()    
    output_dict = {
                 "Filename":log_file,
                 "PhoneModel":phone_model,
                 "Platform":platform,
                 "OSVersion":os_version,
                 "AppVersion":app_version,
                 "AinaDeviceId":device_id,
                 "TestType":test_type,
                 "LotCode":lot_code,
                 "ErrorCode":error_string,
                 "StartTime":time_stamp_start,
                 "EndTime":time_stamp_end,
                 "Data":data,
                 "metadata":metadata,
                 "date_recorded":date_recorded,
                 "date_created":date_created,
                 "date_modified":date_modified,
                 "uuid":uuid
                 }

    # import numpy as np
    # import pandas as pd
    # from sqlalchemy import create_engine
    # import sql
    # engine = create_engine('postgres://postgres:123@localhost/aina_2018')
    # df = pd.DataFrame(output_dict, np.arange(1,2))
    # df.to_sql('analytics_logdata', engine , if_exists='append', index=False)

    # import sql
    # from sqlalchemy import create_engine
    # from sqlalchemy.orm import sessionmaker
    # from analytics.models import LogData
    # from django.conf import settings

    # engine = create_engine('postgres://postgres:123@localhost/aina_2018')
    # # Session.configure(bind=engine)
    # # create a Session
    # DBSession = sessionmaker(bind=engine)
    # session = DBSession()
     
    # add_output = LogData(Filename=log_file, PhoneModel=phone_model, Platform=platform,
    #                         OSVersion=os_version, AppVersion=app_version, DeviceId=device_id,
    #                         TestType=test_type, LotCode=lot_code, ErrorCode=error_string, 
    #                         StartTime=time_stamp_start, EndTime=time_stamp_end, Data=data)
    # session.add(add_output)
    # # commit the record the database
    # session.commit()
    return output_dict



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

# try:
#     index = 0
#     if len(sys.argv) == 2:
#         path = sys.argv[1]
#         # index = int(sys.argv[2])

#     # files = os.listdir(path)
#     file_path = path
#     print log_parser(file_path)
# except Exception as e:
#     print e
