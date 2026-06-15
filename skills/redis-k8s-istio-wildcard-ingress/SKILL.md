---
name: redis-k8s-istio-wildcard-ingress
description: "Troubleshoot Redis Enterprise for Kubernetes Istio ingress failures caused by partial wildcard hostnames. Use when REC reconciliation, Istio Gateway, VirtualService, or validation webhook errors mention partial wildcard, invalid host, `dbFqdnSuffix`, SNI, wildcard DNS, or external routing for Redis databases through Istio."
---

# Redis Kubernetes Istio Wildcard Ingress

Use this skill when Redis Enterprise Operator generates Istio routing resources that fail validation or external Redis/API access fails after configuring Istio ingress.

## Key Rule

Istio allows explicit FQDNs and full leftmost wildcard hosts such as `*.redis.example.com`. It rejects partial wildcards such as `*-redis.example.com`, `myhost-*.example.com`, and `foo.*.example.com`.

For Redis Enterprise Cluster manifests using Istio routing, set `ingressOrRouteSpec.dbFqdnSuffix` to a dot-prefixed subdomain:

```yaml
ingressOrRouteSpec:
  method: istio
  apiFqdnUrl: api.redis.example.com
  dbFqdnSuffix: .redis.example.com
```

Do not use a hyphenated suffix such as `-redis.example.com` with Istio, because generated database hosts can become invalid partial wildcard patterns.

## Triage Workflow

1. Confirm the routing method:

   ```bash
   kubectl get rec <rec-name> -n <namespace> -o yaml | yq '.spec.ingressOrRouteSpec'
   ```

2. Inspect reconciliation and webhook errors:

   ```bash
   kubectl describe rec/<rec-name> -n <namespace>
   kubectl get gateway,virtualservice -n <namespace>
   kubectl describe gateway <name> -n <namespace>
   kubectl describe virtualservice <name> -n <namespace>
   ```

3. Look for messages like `partial wildcard not allowed`, `configuration is invalid`, or invalid host/SNI patterns.
4. Check `dbFqdnSuffix`:
   - Good: `.redis.example.com`
   - Good: explicit database hostnames where supported
   - Bad for Istio: `-redis.example.com`
5. Confirm `apiFqdnUrl` is a fixed FQDN. Do not set it to a wildcard.
6. Verify DNS and TLS cover the resulting names, such as `api.redis.example.com` and `*.redis.example.com`.

## DNS and TLS Checks

Use wildcard or explicit DNS records that point to the Istio ingress gateway:

```bash
dig api.redis.example.com
dig db1.redis.example.com
```

Confirm SNI and certificate behavior:

```bash
openssl s_client -connect api.redis.example.com:443 -servername api.redis.example.com
openssl s_client -connect db1.redis.example.com:443 -servername db1.redis.example.com
```

If TLS fails after changing the suffix, update the certificate SANs and client trust path to match the new FQDNs.

## Routing Method Decision

| Requirement | Recommendation |
| --- | --- |
| Istio ingress required | Use explicit FQDNs or `*.example.com`-style leftmost wildcards only. |
| Existing naming requires partial wildcards | Use NGINX, HAProxy, or OpenShift Route instead of Istio. |
| OpenShift environment | Consider Route for simpler wildcard behavior. |
| Strict SNI/TLS routing | Keep API and database names predictable and covered by DNS/certificates. |

## Verification

The fix is complete when:

- REC reconciliation no longer reports Istio validation webhook failures.
- Gateway and VirtualService resources are created and accepted.
- DNS resolves for API and database FQDNs.
- TLS handshakes succeed with the expected SNI.
- Redis clients can connect through the externally routed database endpoint.
