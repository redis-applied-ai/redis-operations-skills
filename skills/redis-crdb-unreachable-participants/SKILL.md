---
name: redis-crdb-unreachable-participants
description: Use when Redis Software Active-Active CRDB participants are unreachable, `crdb-cli crdb health-report` hangs or times out, CRDB links show disconnected/trying/error, syncer TLS connections fail with `SSL_connect failed`, CRDB endpoint DNS or load balancer mapping is wrong, a participant has no listener on the expected port, certificate rotation broke replication, credentials differ across participants, or a 3+ participant CRDB stops replicating when one region is down.
---

# Redis CRDB Unreachable Participants

Use this skill when Active-Active CRDB replication is blocked by participant reachability, DNS, listener, TLS, credential, or syncer behavior problems.

## Core Rule

Most unreachable participant incidents are network, DNS, TLS, endpoint, listener, or credential configuration problems rather than Redis data corruption. Validate those layers before considering participant removal, re-add, or database recovery.

## Required Context

Collect:

- CRDB GUID
- participating cluster names, instance IDs, regions, and Redis Software versions
- endpoint hostnames and ports used for CRDB replication
- whether a load balancer, route, or firewall sits between participants
- recent changes: certificate rotation, credential update, DNS, firewall, load balancer, upgrade, or region outage

## Layered Diagnostic Workflow

1. Identify the failing link:

   ```bash
   crdb-cli crdb health-report --crdb-guid <CRDB_GUID>
   ```

   Record links in disconnected, trying, error, or timeout state.

2. Test TLS reachability from every healthy participant to the failing participant endpoint:

   ```bash
   openssl s_client -connect <endpoint>:<port> -servername <endpoint>
   ```

   Use `-showcerts` when the certificate chain is suspect.

3. Verify DNS from every participant:

   ```bash
   dig <endpoint>
   nslookup <endpoint>
   ```

4. Verify bidirectional routing and firewall rules. Every participant that should replicate must be able to open the required TLS connection to the other participants.

5. On the target cluster, verify CRDB database and listener state:

   ```bash
   rladmin status db all
   rladmin status extra all
   ```

6. Check syncer logs for TLS, SNI, trust chain, listener, or credential errors.

## TLS And Certificate Checks

When TLS errors appear:

- confirm certificates are not expired
- confirm CA trust chain is available on all participants
- confirm the endpoint hostname matches SNI/certificate expectations
- confirm client/server certificates and private keys match where mutual TLS is configured

If proxy or syncer certificates were recently rotated, refresh CRDB configuration after verifying the change:

```bash
crdb-cli crdb update --crdb-guid <CRDB_GUID> --force
```

## Listener And Load Balancer Checks

For `no listener on <port>` or connection-refused symptoms:

- confirm the CRDB database is running on the target cluster
- confirm the expected endpoint exists and is bound to the expected port
- confirm any load balancer forwards to the CRDB listener, not a different Redis or management service
- confirm load balancer health checks and TLS profiles are not resetting replication traffic

## Credential Mismatch

If credentials were changed in one UI or cluster but not propagated to every participant, update CRDB configuration consistently. Do not expose passwords in chat, logs, or tickets.

Use documented CRDB credential update tooling with redacted placeholders, for example:

```bash
crdb-cli crdb update --crdb-guid <CRDB_GUID> --credentials id=<instance_id>,username=<user>,password=<password>
```

## Multi-Participant Behavior

For CRDBs with three or more participants, record whether one unreachable region also stops replication between healthy regions. Syncer resilience can be version- and configuration-dependent.

After network, DNS, listener, TLS, and credential checks pass, escalate with Redis Software versions and health reports if healthy regions do not continue replicating as expected.

## Recovery Validation

After the fix:

```bash
crdb-cli crdb health-report --crdb-guid <CRDB_GUID>
```

Confirm:

- all links are connected
- sync lag returns to expected range
- replication backlog drains
- syncer TLS/connectivity errors stop recurring
- application writes converge across participants

## Escalation Packet

Collect:

- CRDB GUID and participating cluster/region list
- Redis Software version for each cluster
- recent `crdb-cli crdb health-report`
- `openssl s_client` output from each source participant to each failing endpoint
- DNS results from all participants
- `rladmin status db all` and `rladmin status extra all`
- syncer logs around the failure
- load balancer, firewall, route, and certificate changes
- diagnostic bundles from all participating clusters if Support review is needed
