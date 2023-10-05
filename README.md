# Documentation Website

This website is built using [Docusaurus v2](https://docusaurus.io/), a modern static website generator.

## Getting Started

### Prerequisites

Install yarn: https://yarnpkg.com/getting-started/install

### Installation

```
$ yarn
```

### Local Development

```
$ yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

### Build

```
$ yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Working with Search

Search is powered by Algolia.
For community members who maintain the documentation search functionality (those who have access to the Algolia account)
please refer to the [Docusaurus Search documentation](https://docusaurus.io/docs/search) first for an overview with more information.

There are a few components that might be useful to know about when debugging search-related issues:

- [DocSearch](https://docsearch.algolia.com/) is a program supporting documentation search, which is free for any open-source project. Dragonfly should be part of the program already.
- [Algolia Crawler](https://crawler.algolia.com/) request our documentation pages and creates indexes for them once a while.
- Algolia is where the indexes are actually stored and served from, you can access the [dashboard](https://dashboard.algolia.com/) to see the indexes and search analytics.
