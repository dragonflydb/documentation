---
position: 0
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# SSO Connection
<CloudBadge/>
<PageTitle title="SSO | Dragonfly Cloud" />


## Overview

Dragonfly Cloud supports Single Sign-On (SSO) integration with external identity providers (IdP) using SAML 2.0 protocol connections.
This allows your organization to centralize user authentication and leverage your existing identity management system.

With SSO Connection enabled, Dragonfly Cloud users can:
- Sign in to Dragonfly Cloud using their corporate credentials
- Have access automatically managed through their identity provider
- Comply with their organization's security policies (MFA, password policies, etc.)

## Supported Identity Providers

Dragonfly Cloud supports the following identity providers:

- **[Okta SAML](./okta.md)**: Native integration with Okta using SAML 2.0
- **[Onelogin SAML](./onelogin.md)**: Native integration with Onelogin using SAML 2.0
- **Custom SAML Provider**: Any SAML 2.0 compliant identity provider (Azure AD, Google Workspace, Auth0, OneLogin, etc.)
- For other SSO integrations types please contact [support](mailto:support@dragonflydb.io).

## Setup guide

1. [Contact Support to enable SSO feature first.](mailto:support@dragonflydb.io)
2. [Add domain(s).](./domains.md)
3. [Add idp sso connection with created domain(s).](./add-sso-connection.md)
4. [Add managed users to connection you created on previous step.](./managed-users.md)
