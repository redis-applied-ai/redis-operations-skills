---
name: redis-k8s-secret-auth-connection-failures
description: Use when Redis Enterprise for Kubernetes applications fail to connect after Kubernetes Secret, REDB authentication, passwordless access, ACL/user, TLS certificate, service, DNS, or network policy changes, especially WRONGPASS, NOAUTH, NOPERM, auth failed, timeout, disconnect, stale Secret, application pods not restarted, or REDB/operator reconciliation issues.
---

# Redis Kubernetes Secret Auth Connection Failures

Use this skill when Redis for Kubernetes connectivity breaks after a credential, Secret, TLS, or access-mode change. The main job is to prove whether the failure is caused by Redis database auth, the Kubernetes Secret source, the application reload path, or network/TLS routing.

## Safety Rules

- Never ask for raw passwords, private keys, or complete connection strings with embedded secrets.
- Decode Secrets only in approved secure environments and do not paste decoded values into tickets or chat.
- Treat Kubernetes custom resources and GitOps manifests as the source of truth when reconciliation is active.
- Do not rotate credentials repeatedly until you know which workload is still using which Secret.

## Initial Classification

Collect:

- namespace, REC name, REDB or REAADB name, service name, and port
- exact error: `WRONGPASS`, `NOAUTH`, `NOPERM`, TLS failure, timeout, or disconnect
- recent change: Secret update, REDB auth change, passwordless toggle, TLS/cert update, service or network policy change, app deployment change
- how the application reads credentials: env var, mounted Secret, external secret manager, Helm values, config file, or sidecar
- whether the failing pod restarted after the Secret changed

## Check Redis And Kubernetes Desired State

Inspect database and cluster health before focusing on the application:

```bash
kubectl get redb <database-name> -n <namespace> -o yaml
kubectl get rec -n <namespace>
kubectl get pods -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

Then identify the Secret references from both sides:

```bash
kubectl get secret <database-secret> -n <namespace> -o yaml
kubectl get deployment <app-deployment> -n <namespace> -o yaml
kubectl get pod <app-pod> -n <namespace> -o yaml
```

Verify:

- the REDB references the intended Secret name and namespace
- the Secret has the expected key shape for the installed operator and database spec
- the application reads the same intended credential source
- external-secret controllers or GitOps tools have reconciled the latest value
- database and application auth modes match: password-only, username/password, or passwordless

## Restart Cached Clients

Kubernetes Secret updates do not guarantee a running process reloads credentials. Restart every Redis client workload that may cache auth or TLS material:

```bash
kubectl rollout restart deployment/<deployment-name> -n <namespace>
kubectl rollout status deployment/<deployment-name> -n <namespace>
kubectl get pods -n <namespace> -o wide
```

Include workers, sidecars, scheduled jobs, migration jobs, monitoring agents, and long-lived admin tools.

## Prove The Network Path

Run `redis-cli` from the same namespace and network policy scope as the failing workload. Prefer an application pod or a temporary debug pod with the same egress path.

Password-only auth:

```bash
redis-cli -h <service-name> -p <port> -a '<password>' PING
```

Username and password:

```bash
redis-cli -h <service-name> -p <port> --user <username> -a '<password>' PING
```

TLS:

```bash
redis-cli -h <service-name> -p <port> --tls --cacert /path/to/ca.pem --user <username> -a '<password>' PING
```

Interpretation:

- `PONG`: Redis, service, DNS, and network path are likely good; focus on application config, secret reload, URL encoding, client TLS flags, and stale pods.
- `WRONGPASS`: wrong value, wrong user mode, stale Secret, or Redis auth mode mismatch.
- `NOAUTH`: client is not sending credentials even though Redis requires them.
- `NOPERM`: auth succeeded, but ACL or role permissions are insufficient.
- timeout or disconnect: check Service, Endpoints, NetworkPolicy, DNS, TLS mode, and database health.

## Service, DNS, Network, And TLS Checks

```bash
kubectl get svc,endpoints -n <namespace>
kubectl describe svc <service-name> -n <namespace>
kubectl get networkpolicy -n <namespace>
kubectl logs <app-pod> -n <namespace>
kubectl logs deployment/<operator-deployment> -n <operator-namespace>
```

Check:

- service name and port in the application match the current database service
- endpoints exist and point to healthy Redis pods
- DNS resolves from the failing pod
- NetworkPolicy permits app-to-Redis traffic
- client TLS settings match the database TLS mode
- client trusts the correct CA and uses the expected SNI or hostname when required

## Common Fix Paths

| Symptom | Likely Cause | Next Action |
| --- | --- | --- |
| `WRONGPASS` after Secret update | running pod still has old value | restart every client workload and verify pod age |
| `WRONGPASS` with new Secret | REDB and app read different Secret sources | align Secret references and GitOps/external-secret sources |
| `NOAUTH` | client no longer sends auth | restore auth fields or change database auth mode intentionally |
| passwordless mode fails | client still sends `AUTH` | remove username/password/auth config from the client |
| TLS handshake error | TLS mode or CA mismatch | update client TLS flags and mounted CA material, then restart client pods |
| timeout | service, endpoints, DNS, network policy, or database health | test from same namespace and inspect service/endpoints/events |

## Evidence To Preserve

Collect redacted artifacts:

- REDB or REAADB YAML and status
- referenced Secret name, namespace, key names, and last update time
- application deployment YAML showing env vars or mounts, with secret values removed
- pod restart time and rollout history
- service, endpoint, DNS, network policy, and TLS settings
- exact application/client error
- `redis-cli` result from the same network path
- REC status and operator logs when reconciliation looks unhealthy
