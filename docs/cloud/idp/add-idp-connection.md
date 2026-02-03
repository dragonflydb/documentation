---
sidebar_position: 1
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Adding an Identity Provider Connection
<CloudBadge/>
<PageTitle title="Adding an Identity Provider Connection | Dragonfly Cloud" />

## Overview

Dragonfly Cloud supports Single Sign-On (SSO) integration with external identity providers (IdP) using SAML 2.0 protocol.
This allows your organization to centralize user authentication and leverage your existing identity management system.

With SSO enabled, users can:
- Sign in to Dragonfly Cloud using their corporate credentials
- Benefit from your organization's security policies (MFA, password policies, etc.)
- Have their access automatically managed through your identity provider

## Supported Identity Providers

Dragonfly Cloud supports the following identity providers:

- **[Okta](./okta.md)**: Native integration with Okta using SAML 2.0
- **Custom SAML Provider**: Any SAML 2.0 compliant identity provider (Azure AD, Google Workspace, Auth0, OneLogin, etc.)

## Prerequisites

Before setting up an SSO connection, you need to:

1. **Verify your domain**: You must verify ownership of your organization's email domain. See [Domain Verification](./domains.md) for detailed instructions.
2. **IdP Administrator Access**: You need administrative access to your identity provider to configure the SAML application.
3. **SAML Metadata**: Your identity provider must provide SAML metadata, including:
   - Metadata URL (recommended) or manual configuration
   - X.509 Certificate

## Adding an SSO Connection

To add a new SSO connection in Dragonfly Cloud:

1. Navigate to the **Account > IdP Connections** section in Dragonfly Cloud.
2. Click the **Create Connection** button to create a new SSO connection, put down name, type and linked domains.
3. Copy the following information ACS URL and Entity ID, you will need it for IdP app configuration.
4. Create IdP application configuration with data from step 3.
3. Provide the following information from your IdP metadata:
   - **Metadata URL**: Metadata URL of your identity provider
   - **Certificate**: Copy your PEM encoded certificate into form
5. Click **Create Connection** to save your configuration

## Configuring Your Identity Provider

For detailed provider-specific instructions, see:

- [Okta Configuration Guide](./okta.md)
- [OneLogin Configuration Guide](./onelogin.md)

## Enabling and Managing Connections

After configuring both Dragonfly Cloud and your identity provider:

1. **Enable the Connection**: Toggle the connection to "Enabled" to activate SSO for your domains.
2. **Test the Connection**: Verify that users can successfully authenticate through your IdP.
3. **Enable SCIM (Optional)**: Enable SCIM provisioning to automatically manage users. See [Managed Users](./managed-users.md) for details.

## Disabling an SSO Connection

To disable an SSO connection:

1. Navigate to the connection details page
2. Toggle the connection to "Disabled"

When a connection is disabled, users from associated domains will no longer be able to sign in through SSO.
Existing sessions will remain active until they expired.

:::warning
Disabling an SSO connection does not delete user accounts. Users created through SSO will still exist in your organization.
:::

## Multiple Domains

A single SSO connection can be associated with multiple domains.
This is useful when your organization uses multiple email domains (e.g., `company.com` and `company.io`).

:::tip
Each domain can only be linked to one SSO connection at a time.
:::

## Troubleshooting

### Common Issues

**"Domain is not verified"**
- Ensure your domain is verified before attempting to create an SSO connection. See [Domain Verification](./domains.md).

**"Domain is already used"**
- A domain can only be linked to one SSO connection. Unlink it from the other connection first.

**"Invalid certificate"**
- Ensure the certificate is in valid PEM format and not expired.
- The certificate must be currently valid (between `notBefore` and `notAfter` dates).

**"Invalid metadata URL"**
- The metadata URL must use HTTPS protocol.
- Ensure the URL is accessible from the internet.

**"No special characters are allowed"**
- Connection names can only contain alphanumeric characters, underscores, and spaces.

## Security Considerations

- Always use HTTPS for all SAML URLs
- Regularly rotate your IdP certificates before expiration
- Monitor your IdP audit logs for suspicious authentication attempts
- Consider enabling SCIM provisioning to automatically deprovision users when they leave your organization
- Use your IdP's built-in security features (MFA, conditional access, etc.)
