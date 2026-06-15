---
name: redis-software-iptables-notrack
description: Use when Redis Software traffic is affected by iptables, nftables, stateful firewall rules, connection tracking, CT --notrack, UNTRACKED state, Redis port ranges 3333-3339 or 10000-19999, rlec_supervisor startup tuning, systune.sh, or the systune_skip_iptables.flag behavior.
---

# Redis Software iptables Notrack

Use this skill when Redis Software adds firewall rules that bypass connection tracking for Redis ports and custom firewall rules stop matching expected connection states.

## What Happens

Redis Software can add `iptables` raw-table rules at startup to disable connection tracking on Redis service ports. This reduces kernel overhead for high-throughput Redis traffic, but stateful firewall rules that match only `NEW` or `ESTABLISHED` may not match packets that are marked untracked.

Typical affected port groups:

- `3333-3339` for internal cluster communication
- `10000-19999` for Redis database endpoints

Verify the actual ports for the cluster before changing rules.

## Read-Only Inspection

Start by checking the raw table directly:

```text
iptables -nvL -t raw
iptables -S -t raw
```

Do not rely only on default `iptables -L` output, because raw-table rules may be missed.

Also collect:

- Redis Software version
- host OS and firewall manager
- whether `iptables` or `nftables` is authoritative
- custom firewall rules for Redis ports
- dropped packet logs
- whether the issue appears after Redis Software service startup or node reboot

## Decision Flow

1. Confirm Redis traffic is being marked with `CT --notrack`.
2. Confirm the failing custom firewall rule depends on tracked states such as `NEW` or `ESTABLISHED`.
3. Choose one remediation:
   - Keep Redis Software performance tuning and allow `UNTRACKED` traffic in custom firewall rules.
   - Disable Redis Software iptables injection if the environment requires stateful tracking for those ports.
4. Validate connectivity between cluster nodes and client endpoints after changes.

## Preferred Remediation

When security policy allows it, preserve Redis Software performance tuning and update custom firewall rules to include `UNTRACKED` for Redis ports.

Example shape:

```text
-A INPUT -p tcp -m state --state NEW,UNTRACKED -m tcp --dport 3333:3339 -j ACCEPT
-A INPUT -p tcp -m state --state NEW,UNTRACKED -m tcp --dport 10000:19999 -j ACCEPT
```

Adapt to the environment's firewall manager and rule ordering.

## Disable Injection

If stateful inspection is mandatory, use the Redis Software-supported skip flag for the installed version and configuration directory. Confirm the exact path from the node's Redis Software configuration before creating the file.

Treat this as an operational change:

- record the reason
- apply consistently across relevant nodes
- restart or schedule service changes according to Redis Software procedures
- monitor throughput and latency after disabling notrack behavior

## Response Pattern

When answering:

1. Explain that the rules live in the raw table.
2. Provide read-only inspection commands.
3. Identify whether the failure is stateful-rule mismatch.
4. Recommend `UNTRACKED` rule support first when acceptable.
5. Present the skip-flag option with performance and change-management caveats.
