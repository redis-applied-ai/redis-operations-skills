---
name: redis-k8s-rec-fqdn
description: "Determine and validate the FQDN for a Redis Enterprise Cluster deployed on Kubernetes. Use when the user asks for REC FQDN format, Redis Enterprise Kubernetes license FQDN, `kubectl get rec -A`, service DNS, `svc.cluster.local`, CoreDNS troubleshooting, Discovery Service on port 8001, or license mismatch caused by REC name or namespace."
---

# Redis Kubernetes REC FQDN

Use this skill to determine the Fully Qualified Domain Name for a Redis Enterprise Cluster custom resource and validate it before licensing or service-discovery work.

## FQDN Rule

For the default Kubernetes DNS domain, construct the REC FQDN as:

```text
<rec-name>.<namespace>.svc.cluster.local
```

If the Kubernetes cluster uses a custom service DNS suffix, verify the suffix before changing the FQDN. For Redis Enterprise licensing, confirm the expected suffix with current Redis guidance before requesting or applying a license.

## Discovery Workflow

1. List REC resources:

   ```bash
   kubectl get rec -A
   ```

2. Record the REC `NAME` and `NAMESPACE`.
3. Build the FQDN:

   ```text
   <rec-name>.<namespace>.svc.cluster.local
   ```

4. Verify the matching service exists:

   ```bash
   kubectl get svc -n <namespace>
   ```

5. From a pod in the cluster, test DNS resolution:

   ```bash
   nslookup <rec-name>.<namespace>.svc.cluster.local
   dig <rec-name>.<namespace>.svc.cluster.local
   ```

6. Use the verified FQDN when applying an FQDN-bound Redis Enterprise license.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| FQDN does not resolve | REC name, namespace, service name, and Kubernetes DNS health. |
| License fails with FQDN mismatch | License was generated for a different REC name, namespace, or DNS suffix. |
| Multiple clusters appear similar | Confirm namespace and REC name; avoid duplicate naming assumptions. |
| Custom DNS suffix is present | Verify cluster service domain and Redis Enterprise licensing expectations before applying. |
| CoreDNS issue suspected | Check DNS pods in `kube-system`, such as kube-dns or CoreDNS deployment health. |
| DNS is restricted | Consider Redis Enterprise Discovery Service, Sentinel-compatible API on port 8001, if appropriate. |

## Commands

```bash
kubectl get rec -A
kubectl get svc -n <namespace>
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

If the DNS label selector differs in the cluster, inspect DNS components directly:

```bash
kubectl get pods -n kube-system | grep -Ei 'coredns|kube-dns'
```

## Best Practices

- Use unique REC names per namespace.
- Do not rename an existing REC casually; it changes the FQDN and can invalidate FQDN-bound licensing.
- Build the FQDN dynamically in scripts from REC name and namespace.
- Verify DNS resolution before license requests, license application, and upgrades.

## Escalation Packet

Collect:

- Kubernetes cluster name/context.
- REC name and namespace.
- Constructed FQDN.
- `kubectl get rec -A` output.
- `kubectl get svc -n <namespace>` output.
- In-cluster `nslookup` or `dig` result.
- Kubernetes DNS suffix if non-default.
- License error text if licensing failed.
