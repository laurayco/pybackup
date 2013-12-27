from os import walk, makedirs, listdir, getcwd
from os.path import basename, relpath, splitdrive, getmtime, expandvars, isdir, join
from tarfile import open as opentar
from fnmatch import filter
from time import time

FILE_PATTERN = "backup-*.tar.xz"

def recent_filter(last_modified): return lambda fn:getmtime(fn)>last_modified

def directory_filter(directory):
  _,path = splitdrive(directory)
  def archive_name(fn): return relpath(fn,path)
  return archive_name

def get_filelist(walk):
  for dirpath, dirnames, filenames in walk:
    for fn in filenames:
      yield join(dirpath,fn)

def run_backup(directory):
  backups = join(getcwd(),"Backups")
  try: backups=expandvars('${BACKUP_LOCATION}')
  except:pass
  finally:backups=join(backups,basename(directory))
  makedirs(backups,exist_ok=True)
  recent = max([0]+list(map(getmtime,filter([join(backups,f) for f in listdir(backups)],join(backups,FILE_PATTERN)))))
  archive_name, archive_recent, = directory_filter(directory), recent_filter(recent)
  file_names = [f for f in get_filelist(walk(directory)) if archive_recent(f)]
  if len(file_names)<1:
    print("No files to backup are more recent than the most recent backup.")
    return
  with opentar(join(backups,FILE_PATTERN.replace("*","{}").format(int(time()))),'w:'+FILE_PATTERN[FILE_PATTERN.rfind(".")+1:]) as tarobj:
    for fn in file_names:
      tarobj.add(fn,arcname=archive_name(fn))
      print(archive_name(fn))

if __name__=="__main__":
  from sys import argv
  errors,argv = [],argv[1:]
  for directory in argv:
    if isdir(directory):
      run_backup(directory)
