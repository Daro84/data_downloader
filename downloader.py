import pandas as pd
import os


####################################################################################################
###   SETTINGS  ###

#INSTRUMENT LIST by ticker - list of instruments to download (Stooq.pl)
ticker = [
    'KGH',
    'CDR',
    'DNP',
    'WIG20',
    'MWIG40'
]

#DATE - date range in a format YYYY-MM-DD (default: 2018-01-02 to 2019-01-31)
start_date = '2018-01-02'
end_date = '2019-01-31'

#MERGE - method of merging data by date ('inner' or 'outer', default='outer')
merge_type = 'outer'

#SORT ASCENDING - sort data ascending (by date) (ascending=True, descending=False, default=True)
sort_ascending = True

#FILE FORMAT - type of file format ('csv' or 'xlsx', default='csv')
file_format = 'xlsx'

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
for t in ticker:
    df = pd.read_csv('https://stooq.pl/q/d/l/?s=' + t + '&i=d')
    df_list.append(df)

# merge all data into one spreadsheet
merged = df_list[0]
for i in range(1,len(df_list)):
    merged = pd.merge(merged,df_list[i], on='Data', how=merge_type)

# create final names of columns
columns = ['Date']
for t in ticker:
    columns.extend([t+'_Open',t+'_High',t+'_Low',t+'_Close',t+'_Volume'])
merged.columns = columns

# select data within a specified date range and sort appropriately (ascending or descending)
merged['Date'] = pd.to_datetime(merged['Date'])
merged = merged.set_index('Date')
merged = merged[start_date:end_date]
merged.sort_values(by='Date', ascending=sort_ascending, inplace=True)

# write data to csv or xlsx format and save on your local computer in a specified path
if file_format == 'csv':
    merged.to_csv(path + file_name + '.csv')
else:
    merged.to_excel(path + file_name + '.xlsx')