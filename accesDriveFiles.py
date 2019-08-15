import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
# for file1 in file_list:
#   print('title: %s, id: %s' % (file1['title'], file1['id']))


file_list = drive.ListFile({'q': "name='StockData_BA.xlsx' and trashed=false"}).GetList()
for file in file_list:
  print('%s' % (file['id']))

# file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()

# file_list = []
# for file1 in file_list:
#     if file1['title'] == '[name_of_target_folder]':
#         folder_id = file1['id']