---
name: redis-software-specific-version-download
description: "Request and safely use a specific or older Redis Enterprise Software installer. Use when the user needs a Redis Software version or build not shown in the download portal, must reinstall a node to rejoin a cluster, is recovering a failed cluster, needs exact version/build matching, sees only newer releases in the portal, or must ask Redis Support for a direct installer package."
---

# Redis Software Specific Version Download

Use this skill when a user needs a Redis Software installer for a specific version or build, especially during recovery or node rejoin work.

## Current-State Rule

Do not infer installer availability, latest versions, or support status from memory. Check the Redis download portal or ask Redis Support for the exact current answer when the request depends on availability.

## Core Rule

For node rejoin, cluster recovery, or disk-failure recovery, install the exact same Redis Software version and build as the existing cluster unless following a supported upgrade procedure.

Do not install a newer visible version just because the desired build is missing from the portal.

## When a Specific Build Is Required

- Reinstalling a node to rejoin an existing cluster.
- Recovering a cluster after disk or node failure.
- Restoring version consistency during recovery.
- Matching package build across all cluster nodes.
- Support-directed remediation requiring a named installer.

## Workflow

1. Determine the exact cluster version and build.
2. Confirm OS version and package type.
3. Check the Redis Software download portal first.
4. If the portal does not show the needed version/build, open a Redis Support ticket.
5. Request the exact installer and explain the recovery or rejoin reason.
6. Do not proceed with an alternate version unless Redis Support or official upgrade docs confirm the path.

## Support Request Details

Provide:

- Exact Redis Software version and build, for example `7.8.6-253`.
- Operating system and version, for example RHEL 8 or RHEL 9.x.
- Package type if known.
- Cluster version currently running.
- Reason for request: node rejoin, cluster recovery, disk failure recovery, or other support-directed work.
- Any case/ticket or outage context.

## Verification Before Install

Confirm:

- Installer filename and checksum if provided.
- OS compatibility.
- Package architecture.
- Existing cluster version and build.
- Whether the operation is recovery, rejoin, or upgrade.
- Backup/support package status before making recovery changes.

## Troubleshooting

| Situation | Action |
| --- | --- |
| Portal only shows newer versions | Request the matching build from Redis Support. |
| Unsure which build the cluster uses | Check cluster/node version before requesting. |
| Support declines arbitrary legacy version | Ask for a supported recovery or upgrade path. |
| Installer mismatch discovered | Stop before joining node; get the correct build. |
| Node will not rejoin | Recheck version/build, OS, cluster health, and recovery procedure. |

## Escalation Packet

Collect:

- Cluster name and Redis Software version/build.
- Node role and reason for reinstall.
- OS version and architecture.
- Desired installer version/build.
- Download portal result.
- Recovery timeline and urgency.
- Any current Redis Support ticket.
