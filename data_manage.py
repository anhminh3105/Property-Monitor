'''
this task must be called after calling sub.py if it tries to clean up all the csv files before running. 
'''
import os, glob, time, pathlib
import pandas as pd
from sub import clean_csv_files

def export_new_entry_with_cat(exporting_file, threshold, cat):
    df = pd.read_csv(exporting_file)
    if len(df.index) >= threshold:
        clean_csv_files(exporting_file)
        a_minute_row = pd.DataFrame(df.mean().round(2)).T
        print(a_minute_row)
        if '_' in exporting_file:
            data_cat = exporting_file.split('/')[-1].replace('.csv', '').split('_')[1] # try to take i.e. daily in /home/pi/GUI/database/soil_daily.csv
            file_to_write = pathlib.Path(exporting_file.replace(data_cat, cat))
        else:
            file_to_write = pathlib.Path(exporting_file.replace('.csv', '') + '_' + cat + '.csv')
        if file_to_write.is_file():
            a_minute_row.to_csv(file_to_write, header=False, index=False, mode='a+')
        else:
            a_minute_row.to_csv(file_to_write, index=False, mode='a+')

def main():
    run = True
    path_to_db = '/home/pi/GUI/database/'
    print('data_manage.py running\n')
    while run:
        for file_path in glob.glob(path_to_db + '*.csv'):
            if 'monthly' in file_path:
                export_new_entry_with_cat(file_path, 12, 'yearly')
            if 'daily' in file_path:
                export_new_entry_with_cat(file_path, 30, 'monthly')
            if 'hourly' in file_path:
                export_new_entry_with_cat(file_path, 24, 'daily')
            if 'minutely' in file_path:
                export_new_entry_with_cat(file_path, 60, 'hourly')
            if '_' not in file_path:
                export_new_entry_with_cat(file_path, 60, 'minutely')


if __name__ == "__main__":
    main()
