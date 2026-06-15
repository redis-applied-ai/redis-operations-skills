---
name: redis-crdb-credential-sync
description: "Resolve Redis Software Active-Active CRDB inter-cluster authentication errors after credential changes. Use when the user reports CRDB UI credential updates, `cluster1 is unable to connect to cluster2`, inter-cluster connection errors, authentication mismatch between CRDB participants, or needs a safe sequence for updating CRDB credentials across all participating clusters."
---

# Redis CRDB Credential Sync

Use this skill when CRDB credentials were changed on one participant and inter-cluster connectivity warnings appear even though the UI may show the databases as synchronized.

## Core Model

- CRDB inter-cluster authentication depends on matching credentials across participating clusters.
- Updating credentials through a UI can update the local database while not fully propagating the CRDB-layer credentials to every participant.
- A mismatch can produce warnings such as one cluster being unable to connect to another.
- Resolution requires updating credentials consistently on all CRDB participants.

## Safety Rules

- Treat credentials as secrets. Do not print passwords into logs, tickets, shell history, or chat.
- Plan credential changes during a maintenance window.
- Confirm all participating clusters and CRDB GUIDs before changing anything.
- Keep rollback credentials available through approved secret-handling procedures.

## Diagnosis Workflow

1. Identify the CRDB:
   - CRDB GUID.
   - Participating cluster names and instance IDs.
   - Which UI or API change was made and when.
2. Confirm symptoms:
   - Inter-cluster connection/authentication warning.
   - Affected direction, such as cluster A unable to connect to cluster B.
   - Whether replication and conflict-resolution metrics are otherwise normal.
3. Check whether credentials were updated on every participating cluster.
4. Decide update path:
   - Small deployment: manually update each participant through the UI.
   - Many CRDBs or participants: use `crdb-cli` with all participant credentials.

## Remediation

Manual UI approach:

1. Open each participating cluster.
2. Navigate to the CRDB configuration.
3. Set the credentials to the same intended username/password.
4. Save and repeat for every participant.
5. Verify inter-cluster warnings clear.

CLI approach:

```bash
crdb-cli crdb update \
  --crdb-guid <crdb-guid> \
  --credentials id=1,username=<instance_1_username>,password=<instance_1_password> \
  --credentials id=2,username=<instance_2_username>,password=<instance_2_password>
```

When using CLI, include every participating instance and handle secrets securely.

## Verification

- CRDB status is healthy on all clusters.
- No inter-cluster connection warnings remain.
- Replication and conflict-resolution metrics return to normal.
- Clients can authenticate with the intended credentials.

## Escalation Packet

Collect:

- CRDB GUID.
- Participant cluster names and instance IDs.
- Timestamp and method of credential update.
- Exact inter-cluster warning text.
- Sanitized `crdb-cli` command shape or UI steps used, with passwords redacted.
- Replication/connectivity status after remediation.
