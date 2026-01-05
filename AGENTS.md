# Agent Guidelines for Dragonfly Documentation

Instructions for AI agents contributing technical content to the Dragonfly documentation repository.

## About Dragonfly

Dragonfly is a modern in-memory datastore fully compatible with Redis and Memcached APIs. It achieves 25X performance vs Redis through multi-threaded, shared-nothing architecture supporting millions of QPS on a single instance.

## Repository Structure

[Docusaurus v2](https://docusaurus.io/) site structure:
- `docs/` - Main content (about, getting-started, command-reference, managing-dragonfly, development, integrations, migrating-to-dragonfly, cloud, reference)
- `src/` - React components
- `static/` - Images and assets
- `docusaurus.config.js` - Site config
- `sidebars.js` - Auto-generated sidebar

## Documentation Standards

**File Format**: Markdown with YAML front matter
```markdown
---
description: SEO description (recommended)
sidebar_position: 1 (optional)
---
# Page Title
```

**Writing Style**: Clear technical writing for developers, practical code examples, proper heading hierarchy, emphasize Redis compatibility and performance.

**Category Files**: Use `_category_.yml` for sidebar ordering:
```yaml
position: 2
label: "Section Name"
```

## Documentation Templates

**Command Reference**:
```markdown
---
description: Learn how to use Redis COMMAND...
---
import PageTitle from '@site/src/components/PageTitle';

# COMMAND NAME
<PageTitle title="Redis COMMAND (Documentation) | Dragonfly" />

## Syntax
    COMMAND argument [optional]

**Time complexity:** O(...)
**ACL categories:** @category1, @category2

## Return
[Simple string reply](link): Description

## Examples
```shell
dragonfly> COMMAND arg
"result"
```
```

**Integration Guide**:
```markdown
---
description: Integration Name
---
# Integration Name

## Introduction
Brief intro...

## TL;DR
Quick start...

## Running with Dragonfly
Setup instructions...
```

## Building and Testing

**Prerequisites**: Node.js >= 16.14, Yarn

**Commands**:
```bash
yarn install      # Install dependencies (required after cloning or if build fails)
yarn start        # Local dev server at http://localhost:3000
yarn build        # Build site (verifies no broken links)
yarn serve        # Serve production build locally
```

**Important Notes**:
- Always run `yarn install` first if `yarn build` fails with "docusaurus: not found"
- Run `yarn build` before committing to verify no broken links or errors
- The build process takes 1-2 minutes to complete
- If node_modules becomes corrupted, delete it and run `yarn install` again

## Content Areas

**Command Reference** (`docs/command-reference/`): Redis-compatible commands by category. Include time complexity, parameters, return values, examples with `dragonfly>` prompt.

**Integration Guides** (`docs/integrations/`): Third-party tools (BullMQ, Django, Sidekiq, etc.). Explain purpose, provide TL;DR, detail minimal config changes, include examples.

**Managing Dragonfly** (`docs/managing-dragonfly/`): Operations - config flags, monitoring, HA, backups, cluster, security. Focus on production readiness.

**Getting Started** (`docs/getting-started/`): Installation via Docker, Kubernetes, binary. Step-by-step with prerequisites and expected output.

**Migration Guides** (`docs/migrating-to-dragonfly/`): From Redis instances/clusters. Address pain points, provide checklists, document differences.

## Technical Conventions

**Code Blocks**: Use language-specific syntax highlighting (`bash`, `python`, `javascript`, etc.)

**Command Prompts**: Use `dragonfly>` (not `redis>`) for interactive examples:
````markdown
```shell
dragonfly> SET key value
"OK"
```
````

**Option Markers**: Preserve `!` markers when referencing command options in prose text (e.g., `!DESC`, `!ALPHA`, `!TYPE`). This is an established documentation convention for highlighting options.

**Links**: Internal links use relative paths (`./page.md`), external use full URLs.

**Images**: Store in `/static/img/`, reference as `/img/filename.png` with alt text.

## Dragonfly Key Features

Highlight these differentiators:
- **Multi-threaded architecture** - Vertical scaling, shared-nothing design
- **Snapshot consistency** - No fork-based snapshots (unlike Redis)
- **Native pipelining** - Automatic operation batching
- **Cache mode** - Built-in eviction policies
- **Cluster mode** - Native and emulated modes
- **Lua 5.4 scripting** - Special flags support
- **HTTP admin console**

**Configuration**: Flags via CLI args, flagfile, env vars (DFLY_ prefix), or `CONFIG SET`. Use `dragonfly --helpfull` to list all. Default port 6379, 16 databases.

**Compatibility**: High Redis compatibility (drop-in replacement), Memcached API support, standard Redis clients, cluster protocol support, Lua 5.4 (Redis uses 5.1).

**Performance**: Emphasize vertical scaling vs clustering. Hardware: x86_64/arm64, Linux 4.14+ (5.10+ recommended). 25X performance vs Redis.

## Common Tasks

**Add Integration**: Create `docs/integrations/name.md`, follow template, add to overview, test, build.

**Add Command**: Create `docs/command-reference/category/name.md`, include syntax/complexity/examples, build.

**Update Config**: Edit `docs/managing-dragonfly/flags.md`, maintain format, include defaults, build.

## Resources

- [Docusaurus Docs](https://docusaurus.io/docs)
- [Dragonfly GitHub](https://github.com/dragonflydb/dragonfly)
- [Dragonfly Website](https://www.dragonflydb.io)
- [Redis Commands](https://redis.io/commands) (for reference)
- [Discord](https://discord.gg/HsPjXGVH85)

## Quality Checklist

- [ ] Front matter with description
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Tested code examples
- [ ] Valid links
- [ ] `dragonfly>` prompt (not `redis>`)
- [ ] Build succeeds: `yarn build`
- [ ] Preview checked: `yarn start`

## Best Practices

- **Minimal changes** - Only modify relevant files
- **Follow patterns** - Use existing doc structure
- **Test changes** - Always build and verify
- **Verify with Docker** - Test command syntax and behavior using a running Dragonfly container before documenting
- **Emphasize compatibility** - Dragonfly is drop-in Redis replacement
- **Highlight performance** - Note benefits when relevant
- **Real examples only** - No placeholder content
- Version info: https://version.dragonflydb.io/v1

## Testing Guidelines

When documenting commands:

1. **Use Docker as source of truth**: Always test command syntax with a running Dragonfly container to verify actual behavior:
   ```bash
   docker run -d --name dragonfly-test -p 6379:6379 docker.dragonflydb.io/dragonflydb/dragonfly:latest
   docker exec -it dragonfly-test redis-cli
   ```

2. **Verify actual behavior**: Test commands interactively to confirm syntax, options, and return values. The running container is the authoritative source for what is supported.

3. **Update compatibility table**: If you discover discrepancies between the compatibility table (`docs/command-reference/compatibility.md`) and actual container behavior, update the table to match reality.

4. **Document only supported features**: Do not document command options or features that produce errors or are not yet implemented in Dragonfly, even if they exist in Redis/Valkey.

5. **Do not rely on introspection**: The `COMMAND DOCS` and similar introspection commands may not be implemented - always test with actual command execution.
