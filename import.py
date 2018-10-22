from sqlalchemy import create_engine
from pandas.io.common import EmptyDataError
import pandas as pd
import os

engine = create_engine('postgresql://postgres:123@localhost:5432/ainalogs')
folder = os.path.join(os.getcwd(), 'csv')

try:
	for subdir, dirs, files in os.walk(folder):
	    for file in files:
		print 'importing: ' + file
		df = pd.read_csv(os.path.join(folder, file),  encoding='utf-8')
		df.to_sql('logs_data', engine, if_exists='append')

except EmptyDataError:
	df = pd.DataFrame()
