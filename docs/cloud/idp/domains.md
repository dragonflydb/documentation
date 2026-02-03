---
sidebar_position: 2
---

import PageTitle from '@site/src/components/PageTitle';
import CloudBadge from'@site/src/components/CloudBadge/CloudBadge'

# Domain Verification
<CloudBadge/>
<PageTitle title="Domain Verification | Dragonfly Cloud" />

## Overview

Before you can configure SSO for your organization, you must verify ownership of your email domain(s).
Domain verification ensures that only authorized administrators can configure SSO for a domain, preventing unauthorized access to your organization.

Dragonfly Cloud uses DNS-based verification to confirm domain ownership.

## Why Verify Your Domain?

Domain verification is required for:

- **SSO Configuration**: You can only create SSO connections for verified domains.
- **Security**: Prevents unauthorized parties from configuring SSO for domains they don't control.
- **User Management**: Ensures that users signing in through SSO belong to your organization.

## Adding a Domain

To add and verify a domain:

1. Navigate to **Account > Identity Providers > Domains** in Dragonfly Cloud.
2. Click the **+Domain** button.
3. Enter your organization's email domain (e.g., `company.com`).
   - Only enter the domain name, without `@` or `https://`
   - Example: `company.com`, not `@company.com` or `https://company.com`
4. Click **Add Domain**.

Dragonfly Cloud will generate a unique verification token for your domain.

## Domain Verification Process

Dragonfly Cloud uses DNS TXT record verification. After adding a domain, you need to:

1. **Get Verification Token**: Copy the DNS TXT record value provided by Dragonfly Cloud.
2. **Add DNS TXT Record**: Add a TXT record to your domain's DNS configuration with the verification token.
3. **Wait for DNS Propagation**: DNS changes can take up to 48 hours to propagate, though it's usually much faster (minutes to hours).
4. **Verify Domain**: Return to Dragonfly Cloud and click **Verify Domain**.

### DNS Record Format

Add a TXT record with the following configuration:

- **Host/Name**: `_dfcloud-verification` or `_dfcloud-verification.yourdomain.com`
- **Type**: `TXT`
- **Value/Data**: The verification token provided by Dragonfly Cloud (e.g., `abc123...`)
- **TTL**: 3600 (or your DNS provider's default)

:::tip Example
If your domain is `company.com` and your verification token is `abc123xyz789`, add:

```
Host: _dfcloud-verification
Type: TXT
Value: abc123xyz789
```

Some DNS providers may require the full hostname: `_dfcloud-verification.company.com`
:::

## Checking Verification Status

After adding the DNS record:

1. Wait a few minutes for DNS propagation
2. Return to the Dragonfly Cloud Domains page
3. Click **Verify** next to your domain

If the DNS record is found and matches the verification token, your domain will be marked as verified with a timestamp.

### Verification Troubleshooting

If verification fails:

**"Domain is not verified" error:**
- Wait longer for DNS propagation (up to 48 hours)
- Verify the TXT record was added correctly (no typos in the token)
- Check that you used the correct host name (`_dfcloud-verification`)
- Use a DNS lookup tool to confirm the TXT record is visible (e.g., `dig TXT _dfcloud-verification.yourdomain.com` or online tools like `nslookup.io`)
- Ensure there are no extra spaces or characters in the token value

**DNS propagation check:**
```bash
# Check if your DNS TXT record is visible
dig TXT _dfcloud-verification.yourdomain.com

# Or use nslookup
nslookup -type=TXT _dfcloud-verification.yourdomain.com
```

## Managing Verified Domains

Once verified, you can:

- **Link to SSO Connection**: Associate the domain with an SSO connection to enable SSO for users with email addresses in this domain.
- **Remove Domain**: Delete the domain if it's no longer needed (only possible if not linked to an active SSO connection).

### Linking Domains to SSO Connections

After verification:

1. Navigate to **Account > Identity Providers > Connections**
2. Create a new connection or edit an existing one
3. Select the verified domain(s) to associate with the connection

:::warning
- A domain must be verified before it can be linked to an SSO connection.
- Each domain can only be linked to one SSO connection at a time.
- To link a domain to a different connection, first remove it from the current connection.
:::

## Multiple Domains

Organizations with multiple email domains can verify and use multiple domains:

- Verify each domain separately with its own DNS TXT record
- Link multiple domains to the same SSO connection if they use the same identity provider
- Or create separate SSO connections for different domains if they use different identity providers

Example: If your organization uses both `company.com` and `company.io`, verify both domains and link them to the same SSO connection.

## Removing a Domain

To remove a domain:

1. Ensure the domain is not linked to any active SSO connection
2. Navigate to the Domains page
3. Click the delete/remove button next to the domain

:::warning
You cannot remove a domain that is currently linked to an SSO connection.
First remove the domain from the SSO connection, then delete the domain.
:::

After removing a domain from Dragonfly Cloud, you can optionally delete the DNS TXT record from your domain's DNS configuration.

## Domain Format Requirements

Valid domain formats:

- Must be a valid domain name (e.g., `company.com`, `subdomain.company.com`)
- Must contain at least one dot (`.`)
- Can contain lowercase and uppercase letters (case-insensitive)
- Can contain numbers and hyphens
- Cannot start or end with a hyphen
- Cannot be just a TLD (e.g., `.com` is invalid)

Examples:
- Valid: `company.com`, `mail.company.com`, `company.co.uk`, `company-inc.com`
- Invalid: `.com`, `company`, `company.`, `-company.com`, `company-.com`

## Security Notes

- Keep your DNS configuration secure with appropriate access controls
- Regularly review verified domains to ensure only authorized domains are verified
- Remove domains that are no longer used by your organization
- DNS TXT records are publicly visible, but the verification token itself doesn't grant access
