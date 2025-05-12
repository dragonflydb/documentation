---
sidebar_position: 11
---

import PageTitle from '@site/src/components/PageTitle';

# Managing Users

<PageTitle title="Managing Users | Dragonfly Cloud" />

## Overview

Dragonfly Cloud adopts a role-based access control (RBAC) model to manage users.
The following roles are available:

- **User**: Full access to all resources.
  Can create, view, update, and delete data stores, networks, payment methods, etc.
- **Owner**: Same as User, but can also add and remove users and change the role of a user.
- **Viewer**: Read-only access to all resources.

## Viewing and Managing Users

To view and manage user, go to the [Account > Users](https://dragonflydb.cloud/account/users) tab in Dragonfly Cloud.

- An **Owner** can add a user by clicking the [+User](https://dragonflydb.cloud/account/users/new) button.
- Enter the new user's first name, last name, and email address, and select a role.
- Once added, the new user will be able to log in to your Dragonfly Cloud account.
- An **Owner** can delete an existing user or modify its role under the three-dot
  menu (<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e8eaed"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>)
  on the right side of the user row.
