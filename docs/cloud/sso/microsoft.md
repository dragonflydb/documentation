---
description: "Set up SAML-based single sign-on between Dragonfly Cloud and Microsoft Entra ID."
sidebar_position: 6
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Microsoft Entra ID SSO Integration
<CloudBadge/>
<PageTitle title="Microsoft Entra ID SSO Integration | Dragonfly Cloud" />

## Overview

This guide walks you through setting up Single Sign-On (SSO) between Dragonfly Cloud and Microsoft Entra ID (formerly Azure Active Directory) using SAML 2.0.
With Microsoft Entra ID SSO configured, your users can sign in to Dragonfly Cloud using their Microsoft credentials.

## Prerequisites

Before starting:

- **Microsoft Entra ID Administrator Access**: You need Application Administrator or Global Administrator permissions in your Microsoft Entra ID tenant
- **Verified Domain**: Your email domain must be verified in Dragonfly Cloud. See [Domain Verification](./domains.md)
- **Dragonfly Cloud Owner Role**: You need Owner permissions in Dragonfly Cloud to configure SSO

## Configuration Overview

The setup process involves two main steps:

1. **Create SSO Connection in Dragonfly Cloud**: Set up the connection and obtain SAML configuration details
2. **Configure Microsoft Entra ID Enterprise Application**: Create and configure a SAML app in Microsoft Entra ID

## Step 1: Create SSO Connection in Dragonfly Cloud

1. Navigate to **Access > SSO** in Dragonfly Cloud
2. Click **Add Connection** to create a new SSO connection
3. Enter the connection details:
   - **Name**: Give your connection a descriptive name (e.g., "Microsoft Entra ID SSO")
   - **Provider Type**: Select **SAML: Microsoft**
   - **Domains**: Select your verified domain(s)

4. Copy the **ACS URL** and **Entity ID** values. You'll need them when configuring the Microsoft Entra ID application. Keep this page open as you'll return to it after configuring Microsoft Entra ID.

## Step 2: Create an Enterprise Application in Microsoft Entra ID

### Add a New Enterprise Application

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com)
2. Navigate to **Identity > Applications > Enterprise applications**
3. Click **New application**
4. Click **Create your own application**
5. Enter a name (e.g., "Dragonfly Cloud") and select **Integrate any other application you don't find in the gallery (Non-gallery)**
6. Click **Create**

### Configure Single Sign-On

1. In the newly created application, navigate to **Single sign-on** in the left menu
2. Select **SAML** as the single sign-on method

### Basic SAML Configuration

Click **Edit** on the **Basic SAML Configuration** section and configure:

**Identifier (Entity ID):**
- Enter the Entity ID provided by Dragonfly Cloud
- Example: `https://dragonflydb.cloud`

**Reply URL (Assertion Consumer Service URL):**
- Enter the ACS URL provided by Dragonfly Cloud
- Example: `https://account.dragonflydb.cloud/login/saml/callback`

Click **Save**.

:::tip
Some older Microsoft Entra ID tenants require the Identifier (Entity ID) to be prefixed with `spn:`. If validation of the Entity ID fails after saving, try prefixing the value with `spn:` (e.g. `spn:https://dragonflydb.cloud`).
:::

### Attributes & Claims

In the **Attributes & Claims** section, click **Edit** and configure the following claims. These are Microsoft Entra ID's default claim names, so in most cases they are already present and only need to point at the correct source attribute:

| Claim name | Source attribute |
|------------|-------------------|
| Unique User Identifier (Name ID) | `user.mail` (format: **Email address**) |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` | `user.mail` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` | `user.givenname` |
| `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` | `user.surname` |

Remove any other default claims that are not required to keep the assertion minimal.

## Step 3: Get Microsoft Entra ID SAML Metadata

After configuring SAML settings, obtain the metadata to configure Dragonfly Cloud:

1. In the **SAML Certificates** section, copy the **App Federation Metadata Url**
2. Also download the **Certificate (Base64)** and note the **Login URL** and **Microsoft Entra Identifier** from the **Set up Dragonfly Cloud** section, so you can verify or manually enter these values in the next step

The metadata URL will look like:
```
https://login.microsoftonline.com/{tenant-id}/federationmetadata/2007-06/federationmetadata.xml?appid={application-id}
```

## Step 4: Complete Dragonfly Cloud Configuration

Return to the Dragonfly Cloud SSO connection configuration:

1. Paste the Microsoft Entra ID metadata URL into the **Metadata URL** field.
2. Also enter the values you copied from Microsoft Entra ID:
   - **Entity ID**: Microsoft Entra Identifier
   - **Certificate**: Certificate (Base64)
3. Click **Create Connection**

## Step 5: Assign Users and Groups in Microsoft Entra ID

Before users can sign in, they must be assigned to the enterprise application:

1. In the Microsoft Entra admin center, go to the Dragonfly Cloud enterprise application
2. Navigate to **Users and groups**
3. Click **Add user/group**
4. Select the users or groups that should have access
5. Click **Assign**

## Step 6: Enable the Connection

Back in Dragonfly Cloud:

1. Go to **Access > SSO**
2. Find your Microsoft Entra ID SSO connection
3. Toggle the connection to **Enabled**

## Step 7: Test the Connection

Test that SSO is working correctly:

1. Open a private/incognito browser window
2. Navigate to [Dragonfly Cloud](https://dragonflydb.cloud)
3. Enter your work email address (from your verified domain)
4. You should be redirected to Microsoft for authentication
5. After signing in with your Microsoft credentials, you should be redirected back to Dragonfly Cloud

:::tip
You can also test the connection directly from the Microsoft Entra admin center using the **Test** button on the **Single sign-on** page.
:::

## SCIM Provisioning

SCIM (System for Cross-domain Identity Management) allows Microsoft Entra ID to automatically create, update, and deactivate user accounts in Dragonfly Cloud.

### Enabling SCIM in Dragonfly Cloud

1. Navigate to your SSO connection in Dragonfly Cloud
2. Toggle **SCIM Provisioning** to enabled
3. Copy the **SCIM Endpoint URL** and **bearer token** (you'll need these for Microsoft Entra ID configuration)

### Configuring SCIM in Microsoft Entra ID

1. In the Microsoft Entra admin center, go to your Dragonfly Cloud enterprise application
2. Navigate to **Provisioning**
3. Click **Get started** (or **New configuration**)
4. Set **Provisioning Mode** to **Automatic**
5. Under **Admin Credentials**, enter:
   - **Tenant URL**: Paste the SCIM endpoint URL from Dragonfly Cloud
   - **Secret Token**: Paste the bearer token from Dragonfly Cloud
6. Click **Test Connection** to verify the connection
7. Click **Save**

### Enable Provisioning Features

After the admin credentials are configured:

1. In **Mappings**, review the **Provision Microsoft Entra ID Users** attribute mappings
2. Confirm the following attributes are mapped:
   - `userName` → `email`
   - `emails[type eq "work"].value` → `email`
   - `name.givenName` → `firstName`
   - `name.familyName` → `lastName`
3. Go to **Settings** and set **Provisioning Status** to **On**
4. Optionally, scope provisioning to **Sync only assigned users and groups**
5. Click **Save**

### Testing SCIM Provisioning

Test that SCIM provisioning is working:

1. Assign a test user to the Dragonfly Cloud enterprise application in Microsoft Entra ID
2. Check the **Provisioning logs** in Microsoft Entra ID for any errors
3. Verify the user appears in Dragonfly Cloud under **Access > Users**
4. Unassign the test user and verify they are deactivated in Dragonfly Cloud

## Troubleshooting

### Common Issues

**"User not found" when signing in**
- Ensure the user is assigned to the Dragonfly Cloud enterprise application in Microsoft Entra ID
- If SCIM is enabled, wait a few minutes for provisioning to complete
- Check Microsoft Entra ID's sign-in logs for authentication errors

**"Invalid SAML Response"**
- Verify the claims (`.../emailaddress`, `.../givenname`, `.../surname`) are correctly configured under **Attributes & Claims**
- Ensure the **Email attribute** (and optional first/last name attributes) on the Dragonfly Cloud connection match the claim names configured in Microsoft Entra ID
- Ensure the Name ID format is set to **Email address**
- Check that the certificate has not expired

**"AADSTS7500529" or similar Entra ID errors**
- Verify the **Identifier (Entity ID)** and **Reply URL** exactly match the values provided by Dragonfly Cloud
- Ensure the user is assigned to the application
- On older tenants, try prefixing the Identifier with `spn:` (e.g. `spn:https://dragonflydb.cloud`)

**"Microsoft Entra ID metadata URL not accessible"**
- Ensure the App Federation Metadata Url is correct and includes the `appid` parameter
- Try using manual configuration instead of the metadata URL

**SCIM provisioning not working**
- Verify the SCIM endpoint URL (Tenant URL) and secret token are correct
- Check that **Provisioning Status** is set to **On**
- Review the **Provisioning logs** in Microsoft Entra ID for specific error messages
- Ensure required attributes (email, firstName, lastName) are mapped correctly

**"Certificate validation failed"**
- Verify you copied the complete Base64 certificate (including `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` lines)
- Ensure the certificate is not expired (check under **SAML Certificates**)
- Try refreshing the metadata URL to get the latest certificate

### Microsoft Entra ID Logs

Check Microsoft Entra ID's logs for detailed error information:

- **Sign-in logs**: Navigate to **Identity > Monitoring & health > Sign-in logs** and filter by the Dragonfly Cloud application
- **Provisioning logs**: Navigate to **Identity > Monitoring & health > Provisioning logs** for SCIM operation details

## Certificate Rotation

Microsoft Entra ID SAML certificates expire periodically. To rotate certificates:

1. In the Microsoft Entra admin center, navigate to your Dragonfly Cloud enterprise application
2. Go to **Single sign-on > SAML Certificates**
3. Check the **Expiration Date** of the active certificate
4. If the certificate is near expiration:
   - Create a new certificate under **SAML Certificates**
   - Update the certificate in Dragonfly Cloud by refreshing the metadata URL
   - Or manually copy the new certificate from Microsoft Entra ID to Dragonfly Cloud

5. It's recommended to update the certificate before it expires to prevent authentication failures

## Best Practices

- **Use Metadata URL**: Configure Dragonfly Cloud with Microsoft Entra ID's federation metadata URL for automatic certificate rotation
- **Enable SCIM**: Enable SCIM provisioning to automate user lifecycle management
- **Use Groups**: Assign the enterprise application to Microsoft Entra ID groups rather than individual users for easier management
- **Test Changes**: Always test SSO and SCIM configuration changes with a test user before rolling out to all users
- **Monitor Logs**: Regularly review Microsoft Entra ID's sign-in and provisioning logs for issues
- **Certificate Expiration**: Set reminders to check SAML certificate expiration dates
- **Conditional Access**: Leverage Microsoft Entra ID Conditional Access policies (MFA, device compliance, location) for enhanced security

## Additional Resources

- [Microsoft Entra SAML SSO Documentation](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso)
- [Microsoft Entra SCIM Provisioning Documentation](https://learn.microsoft.com/en-us/entra/identity/app-provisioning/use-scim-to-provision-users-and-groups)
- [Dragonfly Cloud Managed Users](./managed-users.md)
- [Domain Verification](./domains.md)
