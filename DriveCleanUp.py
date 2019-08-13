from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
DriveTitles = list()

for file1 in file_list:
    if int(file1['fileSize']) < 11000:
        print('title: %s, size: %s' % (file1['title'], file1['id']))
        
  
print('done')
