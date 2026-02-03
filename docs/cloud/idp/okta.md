---
sidebar_position: 4
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Okta SSO Integration
<CloudBadge/>
<PageTitle title="Okta SSO Integration | Dragonfly Cloud" />

## Overview

This guide walks you through setting up Single Sign-On (SSO) between Dragonfly Cloud and Okta using SAML 2.0.
With Okta SSO configured, your users can sign in to Dragonfly Cloud using their Okta credentials.

## Prerequisites

Before starting:

- **Okta Administrator Access**: You need administrator permissions in your Okta organization
- **Verified Domain**: Your email domain must be verified in Dragonfly Cloud. See [Domain Verification](./domains.md)
- **Dragonfly Cloud Owner Role**: You need Owner permissions in Dragonfly Cloud to configure SSO

## Configuration Overview

The setup process involves two main steps:

1. **Create SSO Connection in Dragonfly Cloud**: Set up the connection and obtain SAML configuration details
2. **Configure Okta Application**: Create and configure a SAML app in Okta

## Step 1: Create SSO Connection in Dragonfly Cloud

1. Navigate to **Account > Identity Providers > Connections** in Dragonfly Cloud
2. Click **+Connection** to create a new SSO connection
3. Enter the connection details:
   - **Name**: Give your connection a descriptive name (e.g., "Okta SSO")
   - **Provider Type**: Select **SAML: Okta**
   - **Domains**: Select your verified domain(s)

4. You'll need to configure the SAML settings. Keep this page open as you'll return to it after configuring Okta.

## Step 2: Configure SAML Application in Okta

### Create a New SAML Application

1. Sign in to your Okta Admin Console at `https://your-domain.okta.com/admin`
2. Navigate to **Applications > Applications**
3. Click **Create App Integration**
4. Select **SAML 2.0** as the sign-in method
5. Click **Next**

### General Settings

1. **App name**: Enter "Dragonfly Cloud" (or your preferred name)
2. **App logo** (optional): Upload a logo for the application
3. Click **Next**

### Configure SAML Settings

In the SAML Settings section, configure the following:

**Single Sign-On URL:**
- Enter the ACS (Assertion Consumer Service) URL provided by Dragonfly Cloud
- Example: `https://dragonflydb.cloud/auth/saml/callback`
- Check **Use this for Recipient URL and Destination URL**

**Audience URI (SP Entity ID):**
- Enter the Entity ID provided by Dragonfly Cloud
- Example: `https://dragonflydb.cloud`

**Default RelayState:**
- Leave empty (optional)

**Name ID format:**
- Select **EmailAddress**

**Application username:**
- Select **Email**

**Update application username on:**
- Select **Create and update**

### Attribute Statements

Add the following attribute statements to map Okta user attributes to SAML attributes:

| Name | Name Format | Value |
|------|-------------|-------|
| `email` | Unspecified | `user.email` |
| `firstName` | Unspecified | `user.firstName` |
| `lastName` | Unspecified | `user.lastName` |

### Group Attribute Statements (Optional)

You can optionally add group attribute statements if you plan to use group-based access control in the future.

Click **Next** after configuring SAML settings.

### Feedback

1. Select **I'm an Okta customer adding an internal app**
2. Check **This is an internal app that we have created**
3. Click **Finish**

## Step 3: Get Okta SAML Metadata

After creating the application, you need to obtain the SAML metadata to configure Dragonfly Cloud:

1. In the Okta application you just created, go to the **Sign On** tab
2. Scroll down to the **SAML 2.0** section
3. Right-click on **Identity Provider metadata** link and copy the URL

   OR

   Click on **Identity Provider metadata** to view the XML, then save it for manual configuration

The metadata URL will look like:
```
https://your-domain.okta.com/app/exk.../sso/saml/metadata
```

## Step 4: Complete Dragonfly Cloud Configuration

Return to the Dragonfly Cloud SSO connection configuration:

### Option A: Using Metadata URL

1. Paste the Okta metadata URL into the **Metadata URL** field
2. Dragonfly Cloud will automatically fetch and populate:
   - Entity ID
   - SSO URL
   - Certificate

## Step 5: Assign Users in Okta

Before users can sign in, they must be assigned to the application in Okta:

1. In the Okta Admin Console, go to the Dragonfly Cloud application
2. Navigate to the **Assignments** tab
3. Click **Assign** and select:
   - **Assign to People**: Assign individual users
   - **Assign to Groups**: Assign entire groups

4. Select the users or groups and click **Assign** and then **Done**

## Step 6: Enable the Connection

Back in Dragonfly Cloud:

1. Go to **Account > Identity Providers > Connections**
2. Find your Okta SSO connection
3. Toggle the connection to **Enabled**

## Step 7: Test the Connection

Test that SSO is working correctly:

1. Open a private/incognito browser window
2. Navigate to [Dragonfly Cloud](https://dragonflydb.cloud)
3. Enter your work email address (from your verified domain)
4. You should be redirected to Okta for authentication
5. After signing in with your Okta credentials, you should be redirected back to Dragonfly Cloud

:::tip
If you encounter issues, check the troubleshooting section below.
:::

## SCIM Provisioning

SCIM (System for Cross-domain Identity Management) allows Okta to automatically create, update, and deactivate user accounts in Dragonfly Cloud.

### Enabling SCIM in Dragonfly Cloud

1. Navigate to your SSO connection in Dragonfly Cloud
2. Toggle **SCIM Provisioning** to enabled
3. Copy the **SCIM Endpoint URL** and **Bearer Token** (you'll need these for Okta configuration)

### Configuring SCIM in Okta

1. In the Okta Admin Console, go to your Dragonfly Cloud application
2. Navigate to the **Provisioning** tab
3. Click **Configure API Integration**
4. Check **Enable API integration**
5. Enter the following:
   - **SCIM Base URL**: Paste the SCIM endpoint URL from Dragonfly Cloud
   - **OAuth Bearer Token**: Paste the bearer token from Dragonfly Cloud

6. Click **Test API Credentials** to verify the connection
7. Click **Save**

### Enable Provisioning Features

After the API integration is configured:

1. Still in the **Provisioning** tab, go to **Settings > To App**
2. Click **Edit**
3. Enable the following features:
   - **Create Users**: Automatically create users in Dragonfly Cloud when assigned in Okta
   - **Update User Attributes**: Sync user profile changes from Okta to Dragonfly Cloud
   - **Deactivate Users**: Automatically deactivate users in Dragonfly Cloud when unassigned in Okta

4. Click **Save**

### Attribute Mappings

Configure how Okta user attributes map to Dragonfly Cloud user attributes:

1. In the **Provisioning** tab, go to **Settings > To App > Dragonfly Cloud Attribute Mappings**
2. Verify the following mappings:
   - Okta `userName` → Dragonfly `userName`
   - Okta `email` → Dragonfly `email`
   - Okta `firstName` → Dragonfly `firstName`
   - Okta `lastName` → Dragonfly `lastName`

3. Click **Apply Attribute Mappings** if you make any changes

### Testing SCIM Provisioning

Test that SCIM provisioning is working:

1. Assign a test user to the Dragonfly Cloud application in Okta
2. Check the **Provisioning** logs in Okta for any errors
3. Verify the user appears in Dragonfly Cloud under **Account > Users**
4. Unassign the test user and verify they are deactivated in Dragonfly Cloud

## Troubleshooting

### Common Issues

**"User not found" when signing in**
- Ensure the user is assigned to the Dragonfly Cloud application in Okta
- If SCIM is enabled, wait a few minutes for provisioning to complete
- Check Okta's system log for authentication errors

**"Invalid SAML Response"**
- Verify the SAML attributes (email, firstName, lastName) are correctly configured in Okta
- Ensure the Name ID format is set to EmailAddress
- Check that the certificate has not expired

**"Okta metadata URL not accessible"**
- Ensure the metadata URL is correct
- Try using manual configuration instead of metadata URL
- Check if your network/firewall is blocking access to the Okta URL

**SCIM provisioning not working**
- Verify the SCIM endpoint URL and bearer token are correct
- Check the "To App" provisioning settings are enabled
- Review Okta's provisioning task log for specific error messages
- Ensure required attributes (email, firstName, lastName) are mapped

**"Certificate validation failed"**
- Verify you copied the complete certificate (including `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` lines)
- Ensure the certificate is not expired (check in Okta under Sign On > View Setup Instructions)
- Try refreshing the metadata URL to get the latest certificate

### Okta Logs

Check Okta's logs for detailed error information:

- **System Log**: Navigate to **Reports > System Log** in Okta Admin Console
- **Filter by application**: Search for "Dragonfly Cloud" to see authentication and provisioning events
- **Provisioning Task Log**: Go to the application's **Provisioning** tab to see SCIM operation logs

## Certificate Rotation

Okta certificates expire periodically. To rotate certificates:

1. In Okta, navigate to your Dragonfly Cloud application
2. Go to **Sign On** tab
3. Click **View Setup Instructions** to see the current certificate and its expiration date
4. If the certificate is near expiration or expired:
   - Okta will automatically generate a new certificate
   - Update the certificate in Dragonfly Cloud by refreshing the metadata URL
   - Or manually copy the new certificate from Okta to Dragonfly Cloud

5. It's recommended to update the certificate before it expires to prevent authentication failures

## Best Practices

- **Use Metadata URL**: Configure Dragonfly Cloud with Okta's metadata URL for automatic certificate rotation
- **Enable SCIM**: Enable SCIM provisioning to automate user lifecycle management
- **Use Groups**: Assign the application to Okta groups rather than individual users for easier management
- **Test Changes**: Always test SSO and SCIM configuration changes with a test user before rolling out to all users
- **Monitor Logs**: Regularly review Okta's system log and provisioning logs for issues
- **Certificate Expiration**: Set reminders to check certificate expiration dates
- **MFA**: Leverage Okta's MFA capabilities for enhanced security
- **Conditional Access**: Use Okta's sign-on policies to enforce additional security requirements

## Additional Resources

- [Okta SAML Documentation](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_saml.htm)
- [Okta SCIM Provisioning Guide](https://help.okta.com/en-us/content/topics/provisioning/lcm/lcm-provisioning-overview.htm)
- [Dragonfly Cloud Managed Users](./managed-users.md)
- [Domain Verification](./domains.md)
