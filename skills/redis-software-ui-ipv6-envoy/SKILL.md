---
name: redis-software-ui-ipv6-envoy
description: Use when Redis Software Admin UI is unreachable on port 8443 after IPv6 was disabled or hardened on the node OS, Envoy appears running but does not bind the UI port, rlcheck reports localhost 8443 connectivity failure, envoy.log shows malformed IP address ::, or rladmin cluster config ipv6 must be aligned with host IPv6 support.
---

# Redis Software UI IPv6 Envoy Recovery

Use this skill when Redis Software Admin UI stops responding after IPv6 is disabled at the operating-system level while Redis Software still expects IPv6 support.

## Symptoms

Look for:

- Admin UI unreachable on port `8443`
- `supervisorctl status envoy` reports running, but the UI is still unavailable
- `rlcheck` reports connectivity failure to localhost on `8443`
- `envoy.log` contains malformed IPv6 address errors such as `::`
- issue appears after OS hardening, security updates, or IPv6 sysctl changes

## Read-Only Checks

Run:

```text
rlcheck
supervisorctl status envoy
ss -lntp | grep 8443
grep -i "malformed IP address\\|ipv6\\|8443" /var/opt/redislabs/log/envoy.log
```

Also confirm whether IPv6 is disabled at the OS level through the host's standard network configuration or sysctl state.

## Fix

If the host OS no longer supports IPv6 and Redis Software is still configured for IPv6, align Redis Software cluster configuration:

```text
rladmin cluster config ipv6 disabled
```

Then allow Envoy to reload and re-check the UI. Avoid broad restarts unless the service does not reload cleanly or Redis Software support guidance requires it.

## Verification

Confirm:

- `rlcheck` no longer fails on port `8443`
- port `8443` is listening
- Admin UI loads in the browser
- `envoy.log` no longer emits malformed IPv6 address errors
- cluster status remains healthy

## Re-Enable Path

If IPv6 is later restored and required on the hosts, align Redis Software configuration again:

```text
rladmin cluster config ipv6 enabled
```

Verify OS IPv6 support first; do not enable Redis Software IPv6 while the host OS still blocks it.

## Response Pattern

Answer with:

1. The likely mismatch: OS IPv6 disabled while Redis Software still expects IPv6.
2. Read-only checks for Envoy, port `8443`, and logs.
3. The `rladmin cluster config ipv6 disabled` remediation.
4. Verification commands and browser check.
