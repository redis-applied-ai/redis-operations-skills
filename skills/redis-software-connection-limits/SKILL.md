---
name: redis-software-connection-limits
description: Use when Redis Software reports ERR max number of clients reached, connection limits need tuning, shard maxclients versus proxy max-connections are confused, OSS Cluster mode multiplies connections, pub/sub exhausts shard connections, file descriptor limits must be checked, or rladmin tune db should be used instead of editing redis-base.conf.
---

# Redis Software Connection Limits

Use this skill to diagnose and tune Redis Software connection limits safely. Separate shard-level limits from proxy endpoint limits before changing anything.

## Core Model

- `maxclients` is a shard-level Redis process limit. The common default is 10000 per shard process; verify the live database setting.
- `max-connections` is a proxy endpoint limit for client connections to the database endpoint. A value of `0` commonly means unlimited; verify the live database setting.
- OSS Cluster mode in Redis Software still routes client traffic through the Redis Enterprise proxy.
- Cluster-aware clients can open connections across multiple shards, increasing total shard-level connection pressure.
- Pub/Sub can create dedicated proxy-to-shard connections and exhaust shard limits faster than simple command traffic.

## Read-Only Checks

Start with:

```text
rladmin info db db:<ID>
rladmin status database
```

Also inspect:

- current connected clients
- application instance count and pool size
- idle connection buildup
- Pub/Sub usage
- OSS Cluster mode setting
- proxy policy, especially all-nodes behavior
- OS file descriptor limits with `ulimit -n` and service-level limits

## Tuning Commands

Use supported `rladmin tune db` changes. Do not edit shard config files directly.

Shard-level connection limit:

```text
rladmin tune db db:<ID> maxclients <N>
```

Proxy endpoint connection limit:

```text
rladmin tune db db:<ID> max-connections <N>
```

Before raising either value, confirm the OS and Redis processes have file descriptor headroom beyond the target.

## Decision Flow

1. Confirm whether the error is from shard `maxclients` or proxy `max-connections`.
2. If the workload has excessive connection churn or unbounded pools, fix client behavior first.
3. If connections are legitimate and stable, calculate the expected per-shard and per-endpoint connection count.
4. Verify file descriptor headroom.
5. Increase the appropriate limit using `rladmin tune db`.
6. Monitor connection count, errors, latency, CPU, memory, and file descriptor usage after the change.

## Do Not Do

- Do not edit `redis-base.conf` or shard config files directly.
- Do not assume OSS Cluster mode bypasses the proxy.
- Do not raise limits aggressively without checking file descriptors.
- Do not treat idle connection accumulation as a capacity problem until client pooling is reviewed.

## Troubleshooting

- `ERR max number of clients reached`: check shard `maxclients`, proxy `max-connections`, file descriptors, and application pool behavior.
- Limit reached only with OSS Cluster mode: calculate connections per client process times shard count.
- Limit reached during Pub/Sub: account for dedicated Pub/Sub connections to shards.
- Limit returns after upgrade or migration: verify changes were made through `rladmin tune db`, not direct config edits.

## Response Pattern

Answer with:

1. Which connection limit is likely being hit.
2. The read-only commands to verify it.
3. Client-side connection behavior to review.
4. The supported `rladmin tune db` command if increasing the limit is justified.
5. File descriptor and monitoring checks after the change.
