---
sidebar_position: 6
---

# Backups

Dragonfly Cloud supports [manual on-demand](#manual-on-demand-backups) and recurring [scheduled backups](#scheduled-backups).  
Existing backups can be [restored](#restoring-from-backup) to an existing data store.

# Manual On-Demand Backups

To create a manual on-demand backup click the three dots menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the data store row 
, expand the *backups* menu and select *manual*, the backup drawer will open on the right.

Enter a meaningful *description* that will help you identify the backup later for restore.  
Set the *retention period* to the number of days after which the backup will be deleted automatically.  
Click *Create*.

View created backups under the *Account > Backups* tab.

# Scheduled Backups

To set a recurring scheduled backup click the three dots menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the data store row 
, expand the *backups* menu and select *schedule*, the backup drawer will open on the right.  
Set *Backup Policy* to *Enabled*, the Schedule options will appear.  
Select the *days of the week* (or *every day*) and *hours of the day* (or *every hour*) to set when the scheduled backup will be created.  
Set the *retention period* to the number of days after which each created backup will be deleted automatically.  
Click *Apply*

You can edit the backup schedule anytime. 

# Restoring from Backup 

To restore a backup in an existing data store, click the three dots (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) menu in the row of the data store you would like to restore into, the restore backup drawer will open on the right.  
Select the backup you want to restore and click Restore.   
***Note: This operation will clear any existing data in the data store.***


# Viewing and Deleting Backups 

You can view all backups under the *Account > Backups* tab.  
To delete a backup click the three dots menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the backup row and click *Delete*.
