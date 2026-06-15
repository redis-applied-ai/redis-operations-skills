---
name: redis-software-certificate-warning-response
description: Use when Redis Software shows certificate expiration warnings such as cluster certs about to expire, node_cert_expiration_seconds alerts, node_cert_expires_in_seconds alerts, or warnings for cm, api, proxy, syncer, metrics_exporter, ldap_client, mtls_trusted_ca, internode encryption, Replica Of, Active-Active, SSO, or client-facing TLS certificate slots.
---

# Redis Software Certificate Warning Response

Use this skill when Redis Software reports a certificate is nearing expiry but traffic may still be working. For active TLS failures after expiration or partial rotation, use the TLS certificate expiration triage skill.

## Safety Rules

- Do not manually overwrite certificate files under `/etc/opt/redislabs`.
- Use supported Redis Software UI, `rladmin`, or REST API certificate update paths for the installed version.
- Stage replacement cert/key files in a temporary location and keep rollback material until validation passes.
- Identify the certificate slot before rotating anything.
- Treat syncer, Replica Of, Active-Active, internode, LDAP, SSO, and mTLS certificate changes as higher risk than a simple UI certificate warning.
- Verify current Redis Software certificate docs before using version-specific internode or REST API flows.

## First Classification

Collect:

- Redis Software version and deployment type
- warning text and where it appears: UI, alert, log, Prometheus, browser, client, Replica Of, CRDB, or monitoring
- certificate logical name if visible
- expiry timestamp and alert threshold
- affected endpoint or hostname
- whether clients, UI/API, replication, monitoring, or node operations are failing
- recent certificate rotation or CA chain changes

Before expiry, the warning is normally proactive. After expiry, route to active failure triage.

## Identify The Certificate Slot

Use metrics, UI, API, or direct inspection to find the logical certificate with the lowest time remaining.

Prometheus-style signals may include:

- `node_cert_expiration_seconds`
- `node_cert_expires_in_seconds`

Direct endpoint inspection:

```bash
openssl s_client -connect <host>:<port> -servername <host> -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -enddate -subject -issuer
```

File inspection, when you have the cert file:

```bash
openssl x509 -in <certificate.pem> -noout -enddate -subject -issuer
```

Compare expiry, issuer, subject, and SANs against the hostname or endpoint clients actually use.

## Slot Impact Matrix

| Slot | Surface | If Expired Or Mismatched |
| --- | --- | --- |
| `cm` | Cluster Manager UI | browser warnings or UI handshake failure |
| `api` | REST API | API clients fail TLS validation or handshake |
| `proxy` | database endpoints | Redis clients fail TLS validation or hostname checks |
| `syncer` | Replica Of and Active-Active sync | replication or CRDB sync can disconnect |
| `metrics_exporter` | monitoring scrape endpoint | Prometheus or monitoring HTTPS scrape fails |
| `ldap_client` | outbound LDAP auth | LDAP-backed sign-in can fail |
| `mtls_trusted_ca` | REST API mTLS trust | certificate-authenticated API clients can fail |
| internode encryption | control/data internode TLS | node join/replace or cluster communication can fail |
| SSO certificates | SAML SSO | SSO login or assertion trust can fail |

Warnings can persist after renewing common slots if another slot, often `metrics_exporter` or a specialized slot, still expires sooner.

## Renewal Direction By Slot

### UI And API: `cm`, `api`

Renew through the supported UI, `rladmin`, or REST API path.

```bash
rladmin cluster certificate set cm certificate_file /tmp/cm_cert.pem key_file /tmp/cm_key.pem
rladmin cluster certificate set api certificate_file /tmp/api_cert.pem key_file /tmp/api_key.pem
```

Validate using the same FQDN, VIP, or load balancer DNS that users and automation use.

### Client Traffic: `proxy`

Ensure SANs cover the database endpoint hostnames clients use.

```bash
rladmin cluster certificate set proxy certificate_file /tmp/proxy_cert.pem key_file /tmp/proxy_key.pem
```

Afterward, validate representative clients and update trust stores or sidecars if the CA changed.

### Replication: `syncer`, Replica Of, Active-Active

If source proxy or syncer certificates change, replication configurations may need immediate refresh.

For Replica Of:

- update the source cluster certificate
- update the destination Replica Of configuration and trust material
- verify sync resumes and logs no longer show TLS errors

For Active-Active:

- install the updated proxy or syncer certificates and CA chains on relevant clusters
- refresh affected CRDB configuration:

```bash
crdb-cli crdb update --crdb-guid <CRDB-GUID> --force
```

Run this once per affected CRDB and avoid unrelated CRDB update operations between certificate rotation and the refresh. Validate with CRDB health checks afterward.

### Metrics: `metrics_exporter`

Renew when monitoring HTTPS scrapes fail or warnings persist after other slots were renewed.

```bash
rladmin cluster certificate set metrics_exporter \
  certificate_file /tmp/metrics_exporter_cert.pem \
  key_file /tmp/metrics_exporter_key.pem
```

Validate from the monitoring system using the scrape hostname.

### LDAP, mTLS, SSO, Internode

Use the feature-specific Redis Software documentation and current version behavior. These slots can affect authentication, API access, node communication, and cluster stability. Do not handle them as generic proxy or UI certificates.

For customer-managed internode certificates, confirm:

- every node has the same trusted CA chain
- certificates are valid and include full chains
- node join/replace behavior is stable after renewal

## Partial Rotation Checks

Suspect a partial or mixed state when:

- some clients fail but others work
- browser warning persists after cm/api renewal
- Replica Of or CRDB breaks after proxy or syncer rotation
- metrics warnings remain after client-facing certs are updated
- nodes show different expiry dates for the same logical slot

Check every relevant slot and every node for the same expected certificate and expiry.

## Validation

After renewal:

- inspect the live endpoint certificate from the production hostname
- verify UI/API access
- run a Redis client TLS connection test
- confirm monitoring scrapes recover
- check Replica Of or CRDB health when replication certificates or proxy certs changed
- confirm certificate metrics no longer show the warning threshold breach
- watch logs for TLS handshake, hostname, CA, or expired-certificate errors

## Escalation Packet

Collect:

- warning text and first-seen time
- logical certificate name and expiry
- Redis Software version
- current certificate configuration summary from UI/API, with secrets removed
- endpoint hostnames and how clients connect
- metrics showing remaining lifetime by logical name
- recent certificate and CA chain changes
- Replica Of, CRDB, LDAP, SSO, mTLS, or internode features in use
- relevant TLS error logs if failures have started
