---
sidebar_position: 6
---

# Backups

Dragonfly Cloud supports [manual on-demand](#manual-on-demand-backups) and recurring [scheduled backups](#scheduled-backups).  
Existing backups can be [restored](#restoring-from-backup) to an existing data store.

# Manual On-Demand Backups

To create a manual on-demand backup, follow the steps below:

- Click the three-dot menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the data store row.
- Expand the **Backups** menu and select **Manual**, the backup drawer will open on the right.
- Enter a meaningful **Description** that will help you identify the backup later for restoration.
- Set the **Retention** period to the number of days after which the backup will be deleted automatically.
- Click **Create**.

View created backups under the **Account > Backups** tab.

# Scheduled Backups

To set a recurring scheduled backup, follow the steps below:

- Click the three-dot menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the data store row.
- Expand the **Backups** menu and select **Schedule**, the backup drawer will open on the right.
- Set the **Backup Policy** to **Enabled**, the **Schedule** options will appear.
- Select the day(s) of the week (or **Every Day**) and hours of the day (or **Every Hour**) to set when the scheduled backup should be created.
- Set the **Retention** period to the number of days after which the backup will be deleted automatically.
- Click **Apply**.

You can edit the backup schedule anytime. 

# Restoring from Backup 

To restore a backup in an existing data store, follow the steps below:

- Click the three-dot menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the row of the data store you would like to restore to.
- The restore backup drawer will open on the right.
- Select the backup you want to restore and click **Restore**.
- ***CAUTION: This operation will clear any existing data in the data store.***

# Viewing and Deleting Backups 

You can view all backups under the **Account > Backups** tab.
To delete a backup, click the three-dot menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>) in the backup row and click **Delete**.

# Importing Redis Backups (RDB)

You can import Redis backups (RDB files) to Dragonfly Cloud from a remote storage.  
Once imported the backup will be visible under the **Account > Backups** tab as described in [Viewing and Deleting Backups](#viewing-and-deleting-backups) and will be available for restoration as described in [Restoring from Backup](#restoring-from-backup).

To import a Redis backup, follow the steps below:
- Navigate to **Account > Backups** tab.
- Click **+ Import RDB**
- Enter a meaningful **Description** that will help you identify the backup later for restoration.
- Set **retention period** to the number of days after which the imported backup will be deleted automatically.
- Enter the **HTTP URL** of the RDB file to import. 
- Chose the **target cloud** to import to, must match the cloud of the data store you want to restore to.
- Chose the **target region** to import to, preferably match the region of the data store you want to restore to.
- Click **Import**.
- Once the backup is visible in status **ready** you can restore it to a data store as described in [Restoring from Backup](#restoring-from-backup). 

    # Accessability

    The imported rdb file URL must be publicly accessible via HTTP(S) over the internet.

    It is most secure to use a signed URL with a short expiration time to import the RDB file.
    See [AWS S3 Pre-signed URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html) or [Google Cloud Storage Signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls) for more information.

    Otherwise you can generate a long random URL and delete the file after import to ensure security.  


