---
sidebar_position: 3
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Managed Users and SCIM Provisioning
<CloudBadge/>
<PageTitle title="Managed Users and SCIM Provisioning | Dragonfly Cloud" />

## Overview

Managed users are user accounts that are automatically created, updated, and deactivated through your identity provider using SCIM (System for Cross-domain Identity Management) provisioning.
SCIM allows you to centrally manage user lifecycle in your identity provider, and those changes are automatically synchronized to Dragonfly Cloud.

With SCIM provisioning enabled, your identity provider becomes the source of truth for user management.

## Benefits of SCIM Provisioning

- **Automatic User Creation**: New users are automatically created in Dragonfly Cloud when assigned to the application in your IdP
- **Automatic Updates**: User profile changes (name, email) in your IdP are automatically synchronized
- **Automatic Deactivation**: When a user is removed from the application or deactivated in your IdP, they are automatically deactivated in Dragonfly Cloud
- **Centralized Management**: Manage all user access from your identity provider
- **Improved Security**: Ensure users lose access immediately when they leave your organization
- **Reduced Administrative Overhead**: No need to manually manage users in multiple systems

## How SCIM Provisioning Works

When SCIM is enabled for an SSO connection:

1. **Assignment**: An administrator assigns a user to the Dragonfly Cloud application in your identity provider
2. **Provisioning**: Your IdP sends a SCIM request to Dragonfly Cloud to create the user account
3. **Authentication**: The user signs in to Dragonfly Cloud through SSO for the first time
4. **Updates**: Any changes to the user's profile in your IdP are automatically pushed to Dragonfly Cloud
5. **Deprovisioning**: When the user is unassigned or deactivated in your IdP, they are automatically deactivated in Dragonfly Cloud

## Enabling SCIM Provisioning

To enable SCIM provisioning for an SSO connection:

1. Navigate to **Account > Identity Providers > Connections**
2. Select an existing SSO connection or create a new one
3. Toggle **SCIM Provisioning** to enabled
4. Copy the SCIM endpoint URL and bearer token provided by Dragonfly Cloud
5. Configure SCIM in your identity provider using the endpoint URL and bearer token

### Configuration in Your Identity Provider

The exact steps depend on your identity provider. Generally, you'll need to:

1. Access the SAML application configuration in your IdP
2. Navigate to the provisioning or SCIM configuration section
3. Enable provisioning
4. Enter the SCIM endpoint URL provided by Dragonfly Cloud
5. Enter the bearer token for authentication
6. Map user attributes (email, firstName, lastName)
7. Save and test the configuration

For detailed provider-specific instructions, see:
- [Okta SCIM Configuration](./okta.md#scim-provisioning)
- [OneLogin SCIM Configuration](./onelogin.md#scim-provisioning)

## User Lifecycle Management

### User Creation

When SCIM provisioning is enabled and a user is assigned to the Dragonfly Cloud application:

1. Your IdP sends a SCIM create request with user details (email, first name, last name)
2. Dragonfly Cloud creates a new user account
3. The user is marked as a "managed user"
4. The user can now sign in through SSO

:::info
Managed users cannot sign in with a password. They must use SSO authentication through your identity provider.
:::

### User Deactivation

When a user is unassigned from the application or deactivated in your identity provider:

1. Your IdP sends a SCIM deactivation request
2. Dragonfly Cloud deactivates the user account
3. The user immediately loses access to Dragonfly Cloud
4. The user's existing sessions are terminated

:::warning
Deactivated users cannot sign in, but their user account is not deleted. Historical data and audit logs are preserved.
:::

### User Reactivation

If a deactivated user is reassigned to the application in your IdP:

1. Your IdP sends a SCIM activation request
2. Dragonfly Cloud reactivates the user account
3. The user can sign in again through SSO

## Managed vs. Manually Created Users

**Managed Users (SCIM):**
- Created automatically through SCIM provisioning
- Managed entirely by your identity provider
- Can only sign in through SSO
- Cannot be manually deleted or modified in Dragonfly Cloud (must be managed in IdP)
- Automatically deactivated when removed from IdP

**Manually Created Users:**
- Created manually in Dragonfly Cloud by an Owner
- Can sign in with email and password (unless SSO is enforced for their domain)
- Can be modified and deleted in Dragonfly Cloud
- Not automatically synchronized with your identity provider

:::tip
For the best security and management experience, enable SCIM provisioning and manage all users through your identity provider.
:::

## SCIM Attributes

Dragonfly Cloud supports the following SCIM attributes:

| SCIM Attribute | Description | Required |
|----------------|-------------|----------|
| `userName` | User's email address | Yes |
| `emails[primary].value` | User's email address | Yes |
| `name.givenName` | User's first name | Yes |
| `name.familyName` | User's last name | Yes |
| `active` | User's active status (true/false) | Yes |

## Troubleshooting SCIM Provisioning

### Common Issues

**"User not created in Dragonfly Cloud"**
- Verify SCIM is enabled for the SSO connection
- Check that the SCIM endpoint URL and bearer token are correctly configured in your IdP
- Ensure required attributes (email, firstName, lastName) are mapped correctly
- Check your IdP's provisioning logs for error messages

**"User updates not synchronized"**
- Verify your IdP is configured to push updates (not just create users)
- Check that attribute mappings are correct
- Review your IdP's provisioning logs for failed update requests

**"User still has access after deactivation in IdP"**
- Verify your IdP is configured to push deactivation events
- Check that the user was actually removed from the application (not just deactivated in the directory)
- Allow a few minutes for the deactivation to propagate

**"SCIM authentication failed"**
- Verify the bearer token is correctly configured in your IdP
- Ensure the token was copied without extra spaces or characters
- Regenerate the token in Dragonfly Cloud if needed

### SCIM Logs and Monitoring

Most identity providers maintain provisioning logs that show:
- Successful and failed provisioning operations
- Error messages and details
- Timestamps of operations

Check your IdP's provisioning logs for detailed troubleshooting information.

## Disabling SCIM Provisioning

To disable SCIM provisioning:

1. Navigate to the SSO connection details
2. Toggle **SCIM Provisioning** to disabled

:::warning
When SCIM is disabled:
- Existing managed users remain in Dragonfly Cloud but are no longer synchronized
- New users will not be automatically provisioned
- User updates and deactivations will not be synchronized
- Managed users will need to be converted to manual users or managed through the Dragonfly Cloud UI
:::

## Best Practices

- **Enable SCIM Early**: Set up SCIM provisioning when first configuring SSO to ensure all users are managed consistently
- **Test Before Rollout**: Test SCIM provisioning with a small group of users before rolling out to your entire organization
- **Monitor Provisioning Logs**: Regularly review your IdP's provisioning logs to catch and resolve issues quickly
- **Document Your Configuration**: Keep documentation of your SCIM attribute mappings and configuration
- **Secure the Bearer Token**: Treat the SCIM bearer token as a sensitive credential and store it securely in your IdP
- **Plan for Deprovisioning**: Establish clear processes for removing access when users leave your organization

## Security Considerations

- The SCIM bearer token grants access to manage users in your Dragonfly Cloud organization. Keep it secure.
- Regularly rotate the SCIM bearer token (Dragonfly Cloud provides token rotation capabilities)
- Monitor SCIM activity for unexpected user creations or deactivations
- Use your identity provider's audit logs to track provisioning operations
- Ensure only authorized administrators have access to SCIM configuration in your IdP
