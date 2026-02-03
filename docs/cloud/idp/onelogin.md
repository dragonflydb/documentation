---
sidebar_position: 5
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# OneLogin SSO Integration
<CloudBadge/>
<PageTitle title="OneLogin SSO Integration | Dragonfly Cloud" />

## Overview

This guide provides step-by-step instructions for setting up Single Sign-On (SSO) between Dragonfly Cloud and OneLogin using SAML 2.0.
Once configured, your users can sign in to Dragonfly Cloud using their OneLogin credentials.

## Prerequisites

Before starting:

- **OneLogin Administrator Access**: You need administrator permissions in your OneLogin account
- **Verified Domain**: Your email domain must be verified in Dragonfly Cloud. See [Domain Verification](./domains.md)
- **Dragonfly Cloud Owner Role**: You need Owner permissions in Dragonfly Cloud to configure SSO

## Configuration Overview

The setup process involves:

1. **Create SSO Connection in Dragonfly Cloud**: Set up the connection and obtain SAML configuration details
2. **Configure OneLogin Application**: Create and configure a SAML app in OneLogin

## Step 1: Create SSO Connection in Dragonfly Cloud

1. Navigate to **Account > Identity Providers > Connections** in Dragonfly Cloud
2. Click **+Connection** to create a new SSO connection
3. Enter the connection details:
   - **Name**: Give your connection a descriptive name (e.g., "OneLogin SSO")
   - **Provider Type**: Select **SAML: Custom** (OneLogin uses standard SAML)
   - **Domains**: Select your verified domain(s)

4. Keep this page open as you'll need to return to complete the configuration after setting up OneLogin.

## Step 2: Create SAML Application in OneLogin

### Create a New Application

1. Sign in to your OneLogin Admin Portal at `https://your-domain.onelogin.com/admin`
2. Navigate to **Applications > Applications**
3. Click **Add App**
4. Search for "SAML Custom Connector (Advanced)" and select it
5. Click **Save**

### Configure Application Details

1. **Display Name**: Enter "Dragonfly Cloud" (or your preferred name)
2. **Description** (optional): Add a description for the application
3. **Visible in portal**: Check this box if you want users to see the app in their OneLogin portal
4. **Icons** (optional): Upload custom icons for the application
5. Click **Save**

## Step 3: Configure SAML Settings in OneLogin

Navigate to the **Configuration** tab:

### Application Details

1. **Audience (EntityID)**: Enter the Entity ID provided by Dragonfly Cloud
   - Example: `https://dragonflydb.cloud` or the specific SP Entity ID from Dragonfly

2. **Recipient**: Enter the ACS URL provided by Dragonfly Cloud
   - Example: `https://dragonflydb.cloud/auth/saml/callback`

3. **ACS (Consumer) URL Validator**: Enter a regular expression to validate the ACS URL
   - Example: `https://dragonflydb\.cloud/.*`
   - Or leave as default: `.*`

4. **ACS (Consumer) URL**: Enter the same ACS URL as Recipient
   - Example: `https://dragonflydb.cloud/auth/saml/callback`

5. **SAML initiator**: Select **Service Provider** (SP-initiated login)

6. **SAML nameID format**: Select **Email**

7. **SAML signature element**: Select **Assertion** (or **Both** for enhanced security)

8. Click **Save**

## Step 4: Configure Parameters (Attributes)

Navigate to the **Parameters** tab to configure user attribute mappings:

### Add Custom Parameters

Click the **+** button to add new parameters for each required attribute:

#### Email Attribute
1. Click **+** to add a parameter
2. **Field name**: `email`
3. Check **Include in SAML assertion**
4. Click **Save**
5. In the parameter list, click on `email`
6. **Value**: Select **Email** from the dropdown
7. Click **Save**

#### First Name Attribute
1. Click **+** to add a parameter
2. **Field name**: `firstName`
3. Check **Include in SAML assertion**
4. Click **Save**
5. In the parameter list, click on `firstName`
6. **Value**: Select **First Name** from the dropdown
7. Click **Save**

#### Last Name Attribute
1. Click **+** to add a parameter
2. **Field name**: `lastName`
3. Check **Include in SAML assertion**
4. Click **Save**
5. In the parameter list, click on `lastName`
6. **Value**: Select **Last Name** from the dropdown
7. Click **Save**

## Step 5: Get OneLogin SAML Metadata

Navigate to the **SSO** tab to obtain SAML metadata:

### Option A: Using Metadata URL (Recommended)

1. Scroll to the **Issuer URL** section
2. Copy the **Issuer URL** (this is your metadata URL)
   - Example: `https://app.onelogin.com/saml/metadata/your-app-id`

### Option B: Manual Configuration

If you prefer manual configuration:

1. **Issuer URL**: Copy this value (this is the Entity ID)
2. **SAML 2.0 Endpoint (HTTP)**: Copy this value (this is the SSO URL)
3. **X.509 Certificate**: Click **View Details** next to the certificate
4. Copy the certificate content (including BEGIN and END lines)

## Step 6: Complete Dragonfly Cloud Configuration

Return to the Dragonfly Cloud SSO connection configuration:

### Option A: Using Metadata URL (Recommended)

1. Paste the OneLogin metadata URL into the **Metadata URL** field
2. Dragonfly Cloud will automatically fetch and populate:
   - Entity ID
   - SSO URL
   - Certificate

### Option B: Manual Configuration

1. Enter the values you copied from OneLogin:
   - **Entity ID**: Issuer URL from OneLogin
   - **SSO URL**: SAML 2.0 Endpoint (HTTP) from OneLogin
   - **Certificate**: X.509 Certificate from OneLogin

2. Click **Create Connection**

## Step 7: Assign Users in OneLogin

Before users can sign in, they must be assigned to the application:

1. In the OneLogin Admin Portal, go to the Dragonfly Cloud application
2. Navigate to the **Users** tab
3. Click **Add Users** or **Add to application**
4. Select individual users or click **Select all**
5. Click **Continue** and then **Save**

Alternatively, assign by roles:

1. Navigate to **Users > Roles** in OneLogin
2. Select or create a role
3. Go to the **Applications** tab
4. Add the Dragonfly Cloud application to the role
5. All users in that role will have access

## Step 8: Enable the Connection

Back in Dragonfly Cloud:

1. Go to **Account > Identity Providers > Connections**
2. Find your OneLogin SSO connection
3. Toggle the connection to **Enabled**

## Step 9: Test the Connection

Test that SSO is working correctly:

1. Open a private/incognito browser window
2. Navigate to [Dragonfly Cloud](https://dragonflydb.cloud)
3. Enter your work email address (from your verified domain)
4. You should be redirected to OneLogin for authentication
5. After signing in with your OneLogin credentials, you should be redirected back to Dragonfly Cloud

:::tip
Test with a single user first before rolling out to your entire organization.
:::

## SCIM Provisioning

SCIM (System for Cross-domain Identity Management) allows OneLogin to automatically create, update, and deactivate user accounts in Dragonfly Cloud.

### Enabling SCIM in Dragonfly Cloud

1. Navigate to your SSO connection in Dragonfly Cloud
2. Toggle **SCIM Provisioning** to enabled
3. Copy the **SCIM Endpoint URL** and **Bearer Token** (you'll need these for OneLogin configuration)

### Configuring SCIM in OneLogin

1. In the OneLogin Admin Portal, go to your Dragonfly Cloud application
2. Navigate to the **Provisioning** tab
3. Enable **Provisioning** by toggling it on
4. **SCIM Base URL**: Paste the SCIM endpoint URL from Dragonfly Cloud
   - Example: `https://api.dragonflydb.cloud/scim/v2`
5. **SCIM Bearer Token**: Paste the bearer token from Dragonfly Cloud
6. **API Connection**: Click **Enable** and then **Verify** to test the connection

### Enable Provisioning Features

Configure the provisioning workflow:

1. Still in the **Provisioning** tab, configure the following:
   - **Workflow**: Enable the provisioning workflow
   - **Create user**: Check this box to create users in Dragonfly Cloud when assigned in OneLogin
   - **Delete user**: Check this box to deactivate users in Dragonfly Cloud when unassigned
   - **Update user**: Check this box to sync user profile changes

2. **Require Admin Approval**: Optionally enable if you want to manually approve provisioning actions

3. Click **Save**

### Entitlements and Provisioning Rules

Configure what triggers provisioning:

1. In the **Provisioning** tab, go to **Entitlements**
2. Click **Add Entitlement** if needed for group-based provisioning
3. Go to **Provisioning Rules** to define when users should be provisioned

### Testing SCIM Provisioning

Test that SCIM provisioning is working:

1. Assign a test user to the Dragonfly Cloud application in OneLogin
2. Check the **Users** tab in the application for provisioning status
3. Verify the user appears in Dragonfly Cloud under **Account > Users**
4. Unassign the test user and verify they are deactivated in Dragonfly Cloud
5. Check the **Activities** or **Events** log in OneLogin for provisioning events

## Troubleshooting

### Common Issues

**"User not found" when signing in**
- Ensure the user is assigned to the Dragonfly Cloud application in OneLogin
- If SCIM is enabled, wait a few minutes for provisioning to complete
- Check OneLogin's **Events** log for authentication errors

**"Invalid SAML Response"**
- Verify the SAML parameters (email, firstName, lastName) are correctly configured in OneLogin
- Ensure the Name ID format is set to Email
- Check that the certificate has not expired

**"OneLogin metadata URL not accessible"**
- Ensure the Issuer URL is correct
- Try using manual configuration instead of metadata URL
- Verify the application is enabled in OneLogin

**SCIM provisioning not working**
- Verify the SCIM endpoint URL and bearer token are correct
- Ensure the SCIM connection is verified (green status) in OneLogin
- Check that provisioning features (Create, Update, Delete) are enabled
- Review OneLogin's **Events** or **Provisioning** logs for error messages
- Ensure required parameters (email, firstName, lastName) are configured

**"Certificate validation failed"**
- Verify you copied the complete certificate (including `-----BEGIN CERTIFICATE-----` and `-----END CERTIFICATE-----` lines)
- Ensure the certificate is not expired (check in OneLogin under SSO tab)
- Try refreshing the metadata URL to get the latest certificate

### OneLogin Logs

Check OneLogin's logs for detailed error information:

- **Events**: Navigate to **Activity > Events** in OneLogin Admin Portal
- **Filter by application**: Filter events to show only Dragonfly Cloud application events
- **Provisioning Logs**: Check the **Provisioning** tab in the application for SCIM operation logs

## Certificate Rotation

OneLogin certificates expire periodically. To rotate certificates:

1. In OneLogin, navigate to your Dragonfly Cloud application
2. Go to the **SSO** tab
3. Check the **X.509 Certificate** section for expiration date
4. If the certificate is near expiration:
   - OneLogin may automatically generate a new certificate
   - Update the certificate in Dragonfly Cloud by refreshing the metadata URL
   - Or manually copy the new certificate from OneLogin to Dragonfly Cloud

5. Update before expiration to prevent authentication failures

## Best Practices

- **Use Metadata URL**: Configure Dragonfly Cloud with OneLogin's metadata URL for automatic updates
- **Enable SCIM**: Enable SCIM provisioning to automate user lifecycle management
- **Use Roles**: Assign the application to OneLogin roles rather than individual users for easier management
- **Test First**: Always test SSO and SCIM configuration changes with a test user before rolling out
- **Monitor Logs**: Regularly review OneLogin's events and provisioning logs
- **Certificate Monitoring**: Set reminders to check certificate expiration dates
- **Security Policies**: Leverage OneLogin's security policies for MFA, IP restrictions, etc.
- **User Portal**: Enable portal visibility to allow users to easily access Dragonfly Cloud from their OneLogin dashboard

## Additional Resources

- [OneLogin SAML Documentation](https://developers.onelogin.com/saml)
- [OneLogin SCIM Provisioning Guide](https://developers.onelogin.com/scim)
- [Dragonfly Cloud Managed Users](./managed-users.md)
- [Domain Verification](./domains.md)
