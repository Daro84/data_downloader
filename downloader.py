import pandas as pd
import os


####################################################################################################
###   SETTINGS  ###

#INSTRUMENT LIST by ticker - list of instruments to download (Stooq.pl)
ticker = [
    'KGH',
    'DNP',
    'WIG20',
    'FW40',
    'EURPLN'
]

#DATE - date range in a format YYYY-MM-DD (default: 2018-01-02 to 2019-01-31)
start_date = '2018-01-02'
end_date = '2019-01-31'

#DATA - type of data to be downloaded ('Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Open Interest')
# each column can be customized, except column 'Data'
data_columns = [
    'Data',
    'Otwarcie',
    'Najwyzszy',
    'Najnizszy',
    'Zamkniecie',
    'Wolumen',
    'LOP'
    ]

#MERGE - method of merging data by date ('inner' or 'outer', default='outer')
merge_type = 'outer'

#SORT ASCENDING - sort data ascending (by date) (ascending=True, descending=False, default=True)
sort_ascending = True

#FILE FORMAT - type of file format ('csv' or 'xlsx', default='csv')
file_format = 'csv'

#PATH - complete path where file with market data will be saved on your local computer;
# if directory doesn't exist, it'll be created (default='C:\market_data')
path = r'C:\market_data'
if not os.path.exists(path):
    os.mkdir(path)

#FILE NAME - name of created csv file (default='\market_data')
file_name = '\market_data'

#####################################################################################################

# download data for each instrument from Stooq.pl and store in a list
df_list = []
columns = ['Data']
for t in ticker:
    df = pd.read_csv('https://stooq.pl/q/d/l/?s=' + t + '&i=d')
    for c in df.columns:
        if c not in data_columns:
            df.drop(c, axis=1, inplace=True)
    for c in data_columns[1:]:
        if c in df.columns:
            columns.append(c+'_'+t)
    df_list.append(df)

# merge all data into one spreadsheet
merged = df_list[0]
for i in range(1,len(df_list)):
    merged = pd.merge(merged,df_list[i], on='Data', how=merge_type)

# create final names of columns
merged.columns = columns

# select data within a specified date range and sort appropriately (ascending or descending)
merged['Data'] = pd.to_datetime(merged['Data'])
merged = merged.set_index('Data')
merged = merged[start_date:end_date]
merged.sort_values(by='Data', ascending=sort_ascending, inplace=True)

# write data to csv or xlsx format and save on your local computer in a specified path
if file_format == 'csv':
    merged.to_csv(path + file_name + '.csv')
else:
    merged.to_excel(path + file_name + '.xlsx')