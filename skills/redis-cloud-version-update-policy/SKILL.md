---
name: redis-cloud-version-update-policy
description: Use when explaining Redis Cloud database Redis version updates, minor auto-upgrades, major upgrade control, STS or LTS lifecycle behavior, maintenance-window upgrade timing, replication impact, EOL-driven upgrades, or customer opt-out behavior for Redis Cloud Essentials and Pro databases.
---

# Redis Cloud Version Update Policy

Use this skill to explain Redis Cloud database version maintenance and to help customers reason about upgrade impact. Because lifecycle and plan behavior can change, verify the current Redis Cloud policy, console state, API output, or support notice before giving definitive dates or product commitments.

## Core Positioning

- Redis Cloud manages supported Redis versions to keep databases on maintained releases.
- Major version upgrades are customer-controlled and should not be presented as automatic unless current policy explicitly says so.
- Minor and patch updates may be handled through Redis Cloud maintenance processes within the same major version.
- The database's deployed Redis version should be checked in the Console, API, or Terraform state before advising next steps.

## Decision Flow

1. Identify the current database version, target version, plan type, replication setting, and subscription maintenance window.
2. Confirm whether the user is asking about:
   - automatic minor updates
   - a required lifecycle or EOL update
   - a major version upgrade
   - maintenance timing or expected impact
   - opt-out or scheduling control
3. Verify the current lifecycle policy for the specific major and minor versions involved.
4. Explain control boundaries:
   - Major upgrades require customer action.
   - Minor updates may be managed automatically depending on version, lifecycle status, and plan.
   - Patch fixes are generally treated as backward-compatible maintenance.
5. Map the operational impact to replication:
   - Replication enabled: no planned downtime is expected, but brief latency spikes can occur during failover.
   - No replication: expect downtime during shard restart.

## STS And LTS Framing

When discussing support categories:

- Explain STS as shorter-lived minor releases intended to move forward as new minors become available.
- Explain LTS as longer-lived minor releases intended for customers who prefer fewer changes.
- Do not hardcode support dates from memory. Check current Redis Cloud lifecycle information before saying a version is in support, near EOL, or EOL.

## Customer Control Notes

When the user asks whether they can disable automatic minor updates:

1. Determine whether the database is Redis Cloud Pro, Essentials, Flex, marketplace-linked, or another current plan type.
2. Check the database or subscription settings in the Console or API if available.
3. State that opt-out behavior is plan- and policy-dependent, then provide the exact current control path if verified.
4. If a database is on an EOL minor version, explain that Redis Cloud may require an upgrade to keep the service on a supported release.

## Support And Communication

For upgrade-impact questions, ask for:

- subscription ID and database ID
- current Redis version
- plan type
- replication enabled or disabled
- configured maintenance window
- notice or email text, if the user received one
- workload sensitivity to failover, latency spikes, or reconnects

## Response Pattern

Answer with:

1. The version-control boundary: major versus minor or patch.
2. The verified policy status for the user's database and plan.
3. The maintenance-window behavior.
4. Expected impact based on replication.
5. Next action: schedule, opt out if supported, test client failover behavior, or open support with collected IDs and notice details.
