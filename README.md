#pybackup

This is a python utility that will backup a directory into an tar file.
It has no dependancies, and as far as I can tell works on both Python
2.x and 3.x. It stores directory backups as follows:

* In a common folder named "Backups".
 * This can be overriden using the BACKUP_LOCATION environment variable.
* A directory's name part is used as a subdirectory in the "Backups" folder.
* Backup archives are stored following the pattern *backup-[timestamp].tar.xz*

###Details:
Presently all compression is handled using python's builtin tarfile
module.

##Notice:
It is important to *keep all backup files!*
This program will not make redundant backups of files.
So, if a file has not been modified since the last backup,
of that directory, it will not be added to the new archive.
If there are no updated files, logically, there will not be
a new archive made. It is also important to notice that
modifying your archive files will cause them to make the program
think it has made a backup when it has not. I advise not doing
this for obvious reasons.

##To-do:
* Install scripts
 * Including a chron-job / task scheduler for linux / windows respectively?
* Script / flag for consolodating backups? Make sure to warn about data loss.
This could be relevant to people who like revision history, I guess.
