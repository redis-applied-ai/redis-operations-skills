---
name: redis-k8s-tls-failure-troubleshooting
description: Use when Redis Enterprise for Kubernetes or OpenShift TLS fails due to missing or malformed Kubernetes Secrets, REDB tlsMode or tlsSecret issues, REC certificate references, admission webhook certificate errors, redis-cli missing TLS support, LoadBalancer/Ingress/Route passthrough or termination mismatch, wrong version number, no shared cipher, certificate verify failed, mTLS client certificate problems, or unsupported custom internode certificate assumptions.
---

# Redis Kubernetes TLS Failure Troubleshooting

Use this skill to troubleshoot Redis Enterprise for Kubernetes TLS failures. In Kubernetes deployments, TLS behavior is controlled by custom resources, Secrets, Services, Routes, Ingress, and the Redis Enterprise Operator, so UI-only changes may be reverted.

## Safety Rules

- Treat Kubernetes manifests or GitOps sources as authoritative when the operator manages the resource.
- Never ask for private keys, raw Secret values, or unredacted certificates in chat.
- Do not edit generated StatefulSet, webhook, or Service resources directly unless the installed operator docs require it.
- Verify current Redis Kubernetes release notes and supported distribution docs before making version or support claims.
- Do not assume custom internode certificate upload is supported for the installed operator; verify the exact release first.

## First Classification

Collect:

- Kubernetes distribution and version, or OpenShift version
- Redis Enterprise Operator version and REC/REDB names
- failing path: client-to-database, admin API/UI, admission webhook, ingress/route, sync/replication, or internode traffic
- exact error: `certificate verify failed`, `SSL handshake failed`, `wrong version number`, `no shared cipher`, timeout, or connection refused
- recent Secret, certificate, manifest, Helm, ingress, route, or operator changes
- whether TLS was configured through CR YAML, Helm values, UI, or API

## Secret And Manifest Checks

Inspect the target resources:

```bash
kubectl get rec <rec-name> -n <namespace> -o yaml
kubectl get redb <database-name> -n <namespace> -o yaml
kubectl get secret <tls-secret> -n <namespace> -o yaml
kubectl describe redb <database-name> -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
```

For TLS Secrets, verify the expected key names for the configured feature, commonly:

- `ca.crt`
- `tls.crt`
- `tls.key`

Do not decode key material in shared channels. If secure inspection is approved, validate the certificate and key on a controlled host.

Check REDB fields:

- `tlsMode`
- `tlsSecret`
- client authentication certificate references
- service name and port expected by clients

If UI or API TLS changes revert, update the REDB or REC manifest and reapply.

## Pod Mount And Operator Reconciliation

Check whether referenced Secrets are mounted and reconciled:

```bash
kubectl get pods -n <namespace> -o wide
kubectl describe pod <redis-pod> -n <namespace>
kubectl exec -it <redis-pod> -n <namespace> -- ls -l /opt/redislabs/config
kubectl logs deployment/redis-enterprise-operator -n <operator-namespace> --tail=200
```

Look for:

- missing Secret keys
- wrong namespace
- invalid Secret type or name
- reconciliation errors
- pod restarts after Secret changes
- RBAC/SCC errors on OpenShift

## Admission Webhook TLS

If creates or updates fail with webhook TLS errors, inspect the webhook service and certificate references:

```bash
kubectl get validatingwebhookconfiguration,mutatingwebhookconfiguration
kubectl get svc -n <operator-namespace>
kubectl describe svc <admission-service> -n <operator-namespace>
kubectl logs deployment/redis-enterprise-operator -n <operator-namespace> --tail=200
```

Check:

- admission service is the expected internal service type for the installed operator
- webhook CA bundle matches the serving certificate
- the operator pod is healthy and serving the webhook
- certificate rotation or Helm changes did not leave stale webhook configuration

## Client TLS Test From Inside The Cluster

Run from the same namespace and network policy path as the failing workload.

```bash
redis-cli -h <service-name> -p <port> --tls --cacert /path/to/ca.crt PING
```

For mTLS:

```bash
redis-cli -h <service-name> -p <port> --tls \
  --cacert /path/to/ca.crt \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  PING
```

If `redis-cli` does not recognize `--tls`, use a TLS-enabled Redis CLI build or a trusted container image that includes TLS support.

## Ingress, Route, And Load Balancer TLS

For external database access, identify whether TLS should be passthrough or terminated before Redis:

```bash
kubectl get svc,ingress -n <namespace>
kubectl describe svc <service-name> -n <namespace>
kubectl describe ingress <ingress-name> -n <namespace>
```

For OpenShift:

```bash
oc get route -n <namespace>
oc describe route <route-name> -n <namespace>
```

Check:

- passthrough mode preserves Redis TLS to the database endpoint
- termination mode presents a load-balancer or route certificate that clients trust
- SNI hostname matches the certificate SAN
- service port and target port match the intended TLS endpoint
- NetworkPolicy allows the client path
- DNS resolves to the intended ingress, route, or load balancer

## Certificate And Key Validation

On a secure host:

```bash
openssl x509 -in tls.crt -noout -subject -issuer -dates -ext subjectAltName
openssl s_client -connect <host>:<port> -servername <host> -showcerts </dev/null
```

Check:

- certificate is not expired
- SAN matches the client hostname
- CA chain is complete and trusted by the client
- key strength satisfies the node OS/OpenSSL policy
- certificate and key match
- client certificate has expected usage when mTLS is enabled

## Common Findings

| Symptom | Likely Cause | Next Action |
| --- | --- | --- |
| `certificate verify failed` | missing CA, wrong Secret, or untrusted issuer | update Secret and client trust path |
| `wrong version number` | TLS/plaintext mismatch or LB termination mismatch | align client TLS flag and ingress/route mode |
| `no shared cipher` | client and server cipher mismatch | update client runtime or adjust supported config after version check |
| webhook handshake failure | stale CA bundle or serving cert mismatch | inspect webhook config and operator logs |
| UI/API change reverts | operator reconciles from CR manifests | update REC/REDB YAML or GitOps source |
| connection timeout | Service, endpoint, DNS, network policy, or route issue | test from same pod network and inspect endpoints |

## Internode TLS Caveat

For internode encryption issues, first verify the installed operator release supports the requested custom certificate workflow. Some releases do not support customer-provided internode certificates through Kubernetes Secrets. If unsupported, revert unsupported manifest assumptions and focus on documented client, API, proxy, ingress, or route certificate paths.

## Escalation Packet

Collect redacted evidence:

- REC and REDB YAML
- Secret names, namespaces, key names, and certificate metadata
- operator version and Kubernetes/OpenShift version
- operator logs and Kubernetes events
- Service, Ingress, or Route YAML
- exact client error and `redis-cli` or `openssl s_client` result
- whether TLS settings are managed by Helm, GitOps, or direct manifests
