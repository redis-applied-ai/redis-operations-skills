---
name: redis-pubsub-load-reduction
description: Use when Redis Pub/Sub causes high CPU, server load, network egress, output buffer growth, slow consumers, excessive subscriber connections, broad PSUBSCRIBE patterns, global Pub/Sub amplification in OSS Cluster, hot channels in Redis Software or Redis Cloud, or when choosing between Pub/Sub, Sharded Pub/Sub, Streams, Lists, or Sorted Sets.
---

# Redis Pub/Sub Load Reduction

Use this skill to diagnose and reduce CPU, network, and connection pressure caused by Redis Pub/Sub traffic. Start by proving Pub/Sub is the bottleneck and by identifying the deployment topology.

## Load Model

Pub/Sub cost grows with:

- message rate
- subscriber count per channel
- payload size
- pattern subscriptions
- slow subscribers and output buffers
- cluster-wide propagation behavior in the deployment

Use this mental model:

```text
cost ~= messages/sec * subscribers * payload size * topology multiplier
```

## Topology Matters

Redis OSS standalone:

- cost is mostly local fan-out, payload, and client output buffering.

Redis OSS Cluster:

- global `PUBLISH` and `SUBSCRIBE` can amplify traffic across the cluster.
- use Redis 7+ Sharded Pub/Sub (`SPUBLISH`, `SSUBSCRIBE`) for high-volume clustered channels when client and server support it.

Redis Software and Redis Cloud:

- channel names map to shards within a database.
- hot channels can concentrate CPU on a subset of shards.
- monitor per-shard CPU and egress, not only cluster averages.

## Evidence To Gather

Collect:

- Redis product and version
- standalone, OSS Cluster, Redis Software, or Redis Cloud topology
- message rate and average payload size
- subscriber count per hot channel
- use of `PSUBSCRIBE`
- client output buffer growth
- CPU and network usage per node or shard
- keyspace notification setting
- client connection counts and pool behavior

Commands to adapt:

```text
PUBSUB CHANNELS
PUBSUB NUMSUB <channel>
CLIENT LIST
INFO stats
CONFIG GET notify-keyspace-events
```

Use supported configuration APIs where direct `CONFIG` is restricted.

## Optimization Paths

Reduce fan-out:

- partition channels by tenant, region, topic, or shardable domain
- remove unnecessary global channels
- use a WebSocket or application fan-out layer for large user populations

Reduce per-message cost:

- publish IDs or references instead of large payloads
- aggregate high-frequency events
- batch or debounce publisher bursts

Reduce matching overhead:

- replace broad `PSUBSCRIBE` patterns with explicit channels
- avoid wildcard patterns in hot paths

Protect against slow consumers:

- ensure subscribers read continuously
- move heavy work off the read loop
- tune Pub/Sub output buffer limits where appropriate
- disconnect or isolate non-responsive subscribers

Scale intentionally:

- OSS Cluster with global Pub/Sub: migrate hot paths to Sharded Pub/Sub before adding shards.
- Redis Software or Redis Cloud: add shards or rebalance only after identifying hot-channel distribution.

## Use Another Data Structure When Needed

Pub/Sub is at-most-once and non-persistent. Recommend alternatives when the user needs:

- replay: Streams
- acknowledgments: Streams
- back-pressure: Streams
- durable queue: Lists or Streams
- priority queue: Sorted Sets

## Validation

After changes, confirm:

- hot-channel subscriber counts decreased
- pattern subscriptions narrowed or removed
- payload size decreased
- output buffers are stable
- CPU and network usage flatten during previous spike windows
- message loss expectations match the chosen data structure

## Response Pattern

Answer with:

1. The topology and likely Pub/Sub multiplier.
2. The measurements needed to prove it.
3. One application-level change and one topology-level change.
4. Whether Pub/Sub remains the right tool or Streams/another structure should be used.
