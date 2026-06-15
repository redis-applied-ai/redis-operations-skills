---
name: redis-software-support-package-health-analysis
description: "Generate, upload, and supplement Redis Software support packages for cluster health analysis, support tickets, upgrade readiness, reproducible errors, sync failures, import stalls, or data inconsistencies. Use when the user needs Cluster Manager, CLI, or REST API debuginfo collection, alternate debuginfo paths, per-node fallback packages, live rladmin outputs, large package splitting, secure upload guidance, or cleanup of old debuginfo archives."
---

# Redis Software Support Package Health Analysis

Use this skill when Redis Software diagnostics need to be collected for Redis Support or proactive cluster health review. A support package is a compressed diagnostic archive with logs, configuration, and runtime statistics; it should be paired with live command output when the issue is active.

## Safety Rules

- Support package generation can take several minutes and add load. Prefer a lower-traffic window for production clusters.
- Redact secrets from separately shared command output, screenshots, and timelines.
- Do not run cleanup commands for old archives without explicit confirmation of the path and file pattern.
- Do not treat `--skip_aof` or `--skip_db_backups` as `rladmin` flags; use them only with collectors that explicitly document those options.
- Verify current upload limits and link behavior from the active Redis Support ticket before splitting or re-uploading large files.

## When To Collect

Collect a support package:

- after production onboarding, for proactive cluster health analysis
- before a major upgrade, while the cluster is healthy and has no running actions
- when opening or updating a support ticket
- when Redis Support requests diagnostics
- during reproducible failures, sync stalls, import stalls, FeatureSet errors, data inconsistency, or unexplained cluster instability

## Preferred Collection Scope

Choose the broadest practical scope:

1. Full package for all nodes and all databases.
2. If full collection is too large or fails, package all affected databases and nodes.
3. If cluster-level collection fails, collect a package from each active affected node and upload every generated archive.

## Generate From Cluster Manager

Use the Admin Console when it is available:

1. Open the Redis Software Cluster Manager.
2. Go to the Support area.
3. Start support package generation.
4. Choose full cluster, selected databases, selected nodes, or all nodes/databases according to the issue.
5. Download the generated `.tar.gz`.
6. Keep the browser alert or package filename for the ticket timeline.

UI labels changed across Redis Software versions. If the user cannot find the older two-step menu, have them look for the current single generate-package flow in the Support area.

## Generate From CLI

Use full command paths to avoid PATH issues:

```bash
/opt/redislabs/bin/rladmin cluster debug_info
```

If the default staging path has insufficient space, move debuginfo output to a larger filesystem:

```bash
/opt/redislabs/bin/rladmin cluster config debuginfo_path <new-path>
/opt/redislabs/bin/rladmin cluster debug_info
```

Before changing the path:

- confirm the filesystem has enough free space
- confirm the `redislabs` user can write there on every relevant node
- document the old path so it can be restored if required

If cluster-level generation still fails, collect per-node archives:

```bash
/opt/redislabs/bin/debuginfo
```

Upload every `.tar.gz` produced by each affected node, not only the first archive.

## Generate From REST API

Use REST API collection when automation or browser access is preferred:

| Scope | Endpoint |
| --- | --- |
| All nodes and databases | `GET /v1/cluster/debuginfo` |
| All nodes | `GET /v1/nodes/debuginfo` |
| Specific node | `GET /v1/nodes/<uid>/debuginfo` |
| All databases | `GET /v1/bdbs/debuginfo` |
| Specific database | `GET /v1/bdbs/<uid>/debuginfo` |

Use authenticated HTTPS access to the cluster API and avoid placing credentials in shell history, tickets, or chat.

## Add Live-State Diagnostics

For health, stability, maintenance, or active incident analysis, include command output captured near the issue time:

```bash
/opt/redislabs/bin/rladmin status extra all
/opt/redislabs/bin/rladmin cluster running_actions
```

If one database or shard is involved:

```bash
/opt/redislabs/bin/rladmin info db <db_id>
/opt/redislabs/bin/rladmin status shards
```

Also include:

- brief UTC timeline of symptoms and recent maintenance
- Redis Software version and target version if upgrade-related
- database IDs, shard IDs, and node IDs involved
- exact error text and timestamps

## Large Packages And Uploads

Use the upload path from the active Support ticket:

- Prefer a Support-provided secure upload link for full archives.
- If Support provides SFTP, use that for large diagnostics.
- If the portal or email path enforces a size limit, split the archive into parts that fit the current limit.

Common split command:

```bash
split --bytes=50M support_package.tar.gz support_package_part_
```

Upload all parts and tell Support the original filename plus the part count.

## Size Reduction

When the goal is troubleshooting rather than data recovery, and the collector supports it, consider excluding large persistence artifacts:

- `--skip_aof`
- `--skip_db_backups`

Use these only with collectors that document them, such as Kubernetes log-collection scripts or equivalent tools. Do not pass them to `rladmin cluster debug_info`.

## Failure Handling

| Failure | Action |
| --- | --- |
| Not enough space in `/tmp` or debuginfo path | Configure a larger `debuginfo_path`, verify permissions, and rerun. |
| Cluster-level package fails | Run `/opt/redislabs/bin/debuginfo` on each affected node and upload every archive. |
| Upload fails | Use Support-provided SFTP or split the archive according to the active upload limit. |
| Shards are resyncing or state-machine work is active | Wait for stable roles and no running actions before collecting when possible. |
| Package generation repeatedly fails | Collect live `rladmin` outputs, node logs from the relevant window, and escalate with failure text. |

## Cleanup

Support packages are not always automatically removed from the configured debuginfo path. Each run can leave a uniquely named archive.

Before cleanup:

1. Confirm upload is complete and Support no longer needs local copies.
2. Confirm the exact `debuginfo_path`.
3. List matching old archives.
4. Ask for explicit confirmation before removing files.

## Response Shape

When advising a user, provide:

1. The best collection method for their access path.
2. The exact package scope to collect.
3. The extra live command outputs needed.
4. The upload method and split guidance if large.
5. Any cleanup or retry instructions, with confirmation before deletion.
