---
name: redis-software-802-upgrade-troubleshooting
description: Use when troubleshooting Redis Software 8.0.2 upgrade failures, hangs, mixed-version clusters, `running_actions`, CRDB FeatureSet errors such as `bad_featureset_version` or OLD CRDB FEATURESET VERSION, unsupported custom modules such as RedisGraph or RedisGears v2, OLD REDIS VERSION display after upgrade, missing `/opt/redislabs/bin` PATH, TLS/SAN/CA issues, Kubernetes operator 8.0.2 upgrade failures, license rejection, buffer sizing, or known 8.0.2 build limitations.
---

# Redis Software 8.0.2 Upgrade Troubleshooting

Use this skill after a Redis Software 8.0.2 upgrade fails, hangs, or leaves the cluster in a suspicious state. For planning a clean upgrade, use `redis-software-802-upgrade`; for rollback or recovery decisions, use `redis-software-802-rollback-recovery`.

## Current-State Rule

All build numbers, fixed-build recommendations, supported OS/platforms, module support, Kubernetes operator behavior, and rollback guidance must be verified against current Redis release notes before production action.

## Initial State Capture

Run before remediation:

```bash
rladmin status extra all
rladmin cluster running_actions
rladmin status databases extra all
rladmin info
```

Review logs:

```text
/var/opt/redislabs/log/cluster_wd.log
/var/opt/redislabs/log/supervisord.log
/var/opt/redislabs/log/redis-<id>.log
```

Proceed only after you know whether the failure is node upgrade, database upgrade, CRDB, module, TLS, Kubernetes, license, or environment related.

## Common Failure Matrix

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Upgrade hangs | Pending `running_actions`, unhealthy shards, wrong node order, or mixed versions | Wait for or resolve actions; validate health; follow official node order. |
| CRDB `bad_featureset_version` or OLD CRDB FEATURESET VERSION | Participating clusters are on different builds or module config not synced | Upgrade all CRDB sites to the same intended build, then update CRDB module config. |
| Rolling upgrade stalls with custom modules | Unsupported custom modules remain | Remove or replace unsupported modules before retrying. |
| `OK, OLD REDIS VERSION` after upgrade | Release-specific cosmetic or stale status behavior | Verify actual version with database extra status; check fixed build guidance. |
| CLI commands missing | `/opt/redislabs/bin` not in PATH after upgrade | Add supported path configuration or call commands by full path; restart supervisor only when appropriate. |
| TLS handshake failures | SAN, CA chain, expiry, or trust mismatch | Re-upload full chain and validate hostname/SAN. |
| Kubernetes REC/REDB stuck | Operator, CRD, PVC, resource, permission, or module issue | Inspect operator logs, pods, PVCs, CRDs, and running actions. |
| License rejected | Expired, wrong, or FQDN-mismatched license | Apply a renewed matching license. |
| Buffer too small for dataset | Replica/sync buffer insufficient for upgrade | Increase buffer according to current guidance before retry. |

## CRDB FeatureSet Repair

Use only after every participating cluster is upgraded and healthy:

```bash
crdb-cli crdb update --crdb-guid <guid> --update-db-config-modules true
```

Do not run module/FeatureSet updates while participants are mixed-version, unhealthy, or still upgrading.

## Module Handling

Redis 8 bundles core capabilities such as Search, JSON, TimeSeries, and Bloom-style probabilistic features. The source baseline says custom modules such as RedisGraph and RedisGears v2 are unsupported in Redis Software 8.0.2 and can stall upgrades.

Before upgrade retry:

- inventory modules on every database
- remove or migrate unsupported modules
- verify database version compatibility
- confirm current release notes for custom module behavior

## Kubernetes Checks

For Redis Enterprise for Kubernetes:

```bash
kubectl get rec,redb,pods,pvc -n <namespace>
kubectl describe rec <name> -n <namespace>
kubectl logs deploy/<operator-deployment> -n <operator-namespace>
```

Check operator/CRD version, PVC capacity, pod CrashLoopBackOff or Terminating state, storage class behavior, permissions, and unsupported modules or certificate features.

## Known Limitation Handling

Treat source build-specific notes as investigation hints:

- early-build cosmetic old-version status
- memory/RSS regressions in specific builds
- binary downgrade unsupported
- OS deprecations blocking install
- custom internode certificate restrictions in specific Kubernetes releases
- Redis 8.0 Flash versus Redis 8.2/Flex differences

Verify the exact target patch level and current release notes before recommending a fixed build or workaround.

## Post-Fix Validation

Confirm:

```bash
rladmin status extra all
rladmin cluster running_actions
rladmin info
```

Also verify:

- all databases active and healthy
- CRDB instances synced
- Cluster Manager has no red alerts
- clients authenticate and run representative commands
- monitoring/Prometheus/Datadog metrics continue flowing
- no unexpected running actions remain

## Escalation Packet

Collect:

- current and target Redis Software build
- upgrade method and node order
- `rladmin` state outputs and running actions
- database versions and modules
- CRDB GUIDs and participant versions if Active-Active is involved
- Kubernetes operator/CRD/pod/PVC state if applicable
- exact error text and logs
- license status
- backup and restore readiness
