---
name: redis-azure-acre-amr-connection-limits
description: "Triage Azure Redis Enterprise connection storms and health-check load differences between ACRE and AMR, including VM-level connection caps, dmcproxy CPU saturation, proxy restart loops, SLO degradation without shard failure, load balancer per-source limits, health-check concurrency, idle timeout tuning, OS file descriptor and backlog checks, `ss -antp` source analysis, and deciding when AMR-enforced connection ceilings or Support escalation are needed."
---

# Redis Azure ACRE And AMR Connection Limits

Use this skill when Redis deployments on Azure show high connection counts, proxy instability, health-check amplification, or questions about ACRE versus AMR per-VM connection behavior. Verify current Azure/Redis platform behavior, SKU limits, and Support guidance before treating any numeric threshold as a hard limit.

## Core Model

| Platform | Working Model | Operator Responsibility |
| --- | --- | --- |
| ACRE | No platform-enforced per-VM connection cap in the scenario covered by this guidance. Connections can keep increasing until VM, OS, proxy, or network resources saturate. | Enforce limits at application, load balancer, OS, and operational policy layers. |
| AMR | Platform-enforced per-VM connection caps can reject or throttle excess connections before proxy saturation. | Confirm current cap and scale horizontally or request adjustment when legitimate traffic exceeds it. |

Do not confuse this with Redis Software database `maxclients` tuning. If the error is `ERR max number of clients reached`, use `redis-software-connection-limits` as well.

## Immediate Triage

1. Confirm platform: ACRE or AMR.
2. Identify whether symptoms are connection-related:
   - connected clients rising quickly
   - proxy CPU spikes
   - `dmcproxy` restart loops
   - health-check failures or noisy probes
   - SLO degradation while shards remain healthy
   - new connections rejected or throttled
3. Check per-VM connection counts and proxy CPU.
4. Check load balancer, reverse proxy, and health-check configuration.
5. Classify the traffic pattern:
   - stable long-lived connections
   - burst connection creation
   - failed connection attempts
   - `SYN_RECV`, `TIME_WAIT`, or `CLOSE_WAIT` accumulation
   - one source or many sources

## ACRE Mitigation

On ACRE, control connection growth outside the Redis VM before redeploying or restarting affected nodes.

Application layer:

- Enable and right-size connection pools.
- Reuse connections; avoid burst-style connect/disconnect behavior.
- Tune idle, connect, read, and write timeouts.
- Apply per-service max connection limits.

Load balancer or reverse proxy:

- Set maximum concurrent connections per backend VM.
- Apply per-source connection limits where supported.
- Enable rate limiting or request queuing.
- Tune idle timeouts to clear stale connections without forcing reconnect storms.
- Reduce health-check concurrency.

OS and VM:

- Check file descriptor limits such as `ulimit -n` and `fs.file-max`.
- Check backlog settings such as `net.core.somaxconn`.
- Monitor backlog queues and connection states.
- Watch for ephemeral port exhaustion.

Do not redeploy an affected VM until traffic has been throttled or pooled; otherwise the replacement can re-enter the same proxy saturation pattern.

## AMR Mitigation

On AMR, platform caps are part of the protection model.

1. Confirm the current per-VM cap and enforcement behavior with Support or current platform documentation.
2. If legitimate traffic exceeds the cap, scale horizontally or adjust architecture rather than relying on retries alone.
3. Ensure clients use retries with exponential backoff and jitter.
4. Verify that health checks and load balancers do not create unnecessary connection pressure.
5. If a cap adjustment is needed, provide Support with service, region, peak connections, desired cap, and traffic justification.

## Health Check Optimization

Health checks can amplify connection volume when every probe opens a new connection or probes too frequently.

Optimize probes:

- Increase probe interval where SLO permits.
- Reduce concurrent probes per backend.
- Use lightweight endpoints or commands.
- Set short but realistic timeouts.
- Reuse connections when the health-check system supports it.
- Avoid routing health checks through paths that trigger expensive Redis work.

## Investigation Commands And Evidence

On a VM, inspect connection state and source distribution:

```bash
ss -antp
```

Review:

- remote IP distribution
- `ESTAB`, `SYN_RECV`, `TIME_WAIT`, and `CLOSE_WAIT`
- proxy logs and restart events
- load balancer request and health-check logs
- connected-client metrics per VM
- proxy CPU and memory
- shard health, to confirm whether degradation is proxy-side rather than data-shard failure

## Threshold Guidance

Use numeric thresholds only as investigation heuristics, not platform guarantees:

- Small VMs can become risky well before larger SKUs.
- Around 10k connections per VM on small 2-core shapes should trigger closer inspection.
- Around 15k connections per VM should be treated as high risk for proxy instability unless live evidence proves headroom.
- Always verify current SKU, proxy metrics, and Support guidance before declaring a fixed limit.

## Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| ACRE VM has very high connections but no immediate rejection | No platform cap is protecting the VM | Add load-balancer and app-level limits before redeploying. |
| `dmcproxy` restarts under connection load | Proxy CPU or resource saturation | Throttle traffic, reduce health checks, inspect source distribution, then recover VM if needed. |
| SLO degrades while shards look healthy | Proxy path overloaded before shard failure | Focus on proxy CPU, connection states, and load balancer behavior. |
| New connections rejected on AMR | Platform cap or throttling is active | Confirm cap, reduce connection pressure, or scale horizontally. |
| Health checks dominate connections | Probe interval/concurrency too aggressive | Reduce probe count, reuse connections, and use lightweight checks. |
| Connections accumulate in abnormal states | Client, network, timeout, or LB behavior | Tune idle/read/write timeouts and inspect source IPs. |
| Traffic appears routed unexpectedly | LB health-check or routing policy issue | Compare backend pools, probe path, and observed source/destination distribution. |

## Support Packet

Collect:

- Platform: ACRE or AMR.
- Service name, region, and VM SKU.
- Peak connections per VM and time window.
- Proxy CPU and restart timeline.
- Shard health during the event.
- Load balancer and health-check configuration summary.
- Source IP distribution from `ss -antp` or LB logs.
- Recent deploys, traffic changes, scaling changes, or health-check changes.
- For AMR: current cap, desired cap, and traffic justification.

## Response Shape

When helping a user:

1. Confirm ACRE versus AMR first.
2. Separate proxy connection overload from shard/database failure.
3. For ACRE, prioritize edge throttling, pooling, and health-check reduction before VM redeploy.
4. For AMR, verify the current cap and recommend horizontal scaling or Support adjustment when needed.
5. Provide the evidence packet needed for Support if instability, cap adjustment, or unexpected routing remains.
