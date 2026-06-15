---
name: redis-software-tls-certificate-expiration-triage
description: Use when Redis Software or Redis Enterprise Software TLS connections fail due to expired, rotated, mismatched, or partially updated certificates, including UI/API access failures, database proxy TLS errors, syncer or metrics exporter cert expiry, internode encryption certificate trust-chain issues, client mTLS failures, certificate chain loops, OCSP errors, or client truststore problems after renewal.
---

# Redis Software TLS Certificate Expiration Triage

Use this skill when Redis Software TLS failures may be caused by expired or partially renewed certificates. The goal is to identify certificate scope, prove expiration or trust-chain failure, renew through supported paths, and verify clients after rotation.

## Safety Rules

- Never ask users to paste private keys, keystores, or unredacted certificates with sensitive subject details into chat.
- Treat certificate replacement as a production change; keep rollback material until all paths validate.
- Do not mix certificate scopes. UI/API, proxy, syncer, metrics, client mTLS, and internode certificates can fail differently.
- Verify current Redis Software docs and version behavior before using version-specific certificate APIs.
- For internode or customer-managed CA chains, validate consistency on every node before restarting services.

## First Classification

Collect:

- Redis Software version and deployment type
- failing path: UI, REST API, database endpoint, syncer, metrics scrape, node join, node replace, client mTLS, or internode traffic
- exact TLS error text and timestamp
- whether certificates were recently renewed, partially deployed, or expired
- whether all nodes received the same certificate and CA chain
- whether clients, sidecars, load balancers, or truststores were updated

## Inspect Certificate Expiration

On Redis Software nodes, inspect presented and stored certificates without exposing keys:

```bash
for file in $(find /etc/opt/redislabs -name '*_cert.pem'); do
  echo "$file"
  openssl x509 -in "$file" -noout -subject -issuer -dates
done
```

For remote endpoints, inspect what the service presents:

```bash
openssl s_client -connect <host>:<port> -servername <host> -showcerts </dev/null
```

Check:

- `notAfter` date
- subject/SAN covers the endpoint hostname
- issuer and intermediate chain are expected
- chain has no repeated certificate loop
- extended key usage matches the certificate role
- all Redis nodes have consistent files for the same certificate scope

## Scope Matrix

| Failure Surface | Likely Certificate Scope | Checks |
| --- | --- | --- |
| Admin UI unavailable | cluster manager or API certificate | browser error, REST API TLS handshake, cert expiry |
| REST API on 9443 fails | API certificate or truststore | `openssl s_client`, API client CA bundle |
| Redis clients fail TLS | proxy/database endpoint certificate | endpoint hostname/SAN, client CA trust, TLS mode |
| Active-Active or ReplicaOf sync fails | syncer certificate or trust chain | syncer logs, peer trust, version compatibility |
| Prometheus target fails | metrics exporter certificate | scrape logs, CA bundle, metrics exporter status |
| node join/replace fails | internode encryption or customer-managed CA chain | identical CA chain on all nodes, node logs |
| mTLS client auth fails | client certificate or client CA trust | client cert expiry, EKU, CA trust, revocation policy |

## Supported Renewal Path

Use the broad credential/certificate rotation skill when planning a non-emergency rotation. During an incident:

1. Identify the failing certificate scope.
2. Generate or obtain replacement certificate, key, and full chain using the environment's approved CA process.
3. Install only through supported Redis Software UI, CLI, or REST API paths for that certificate type.
4. Apply the same required material across all nodes.
5. Restart or reload only the services required by the supported procedure.
6. Restart or reload clients that cache certificates or trust material.
7. Validate every affected path.

For external Redis Software certificates, the `rladmin cluster certificate set` pattern may apply:

```bash
rladmin cluster certificate set <certificate-name> certificate_file <cert.pem> key_file <key.pem>
```

Confirm the exact certificate name and supported scope for the installed Redis Software version before running it. Do not use an external-certificate command as a substitute for internode certificate procedures.

## Internode And Customer-Managed CA Chains

For customer-managed internode certificates, check:

- every node has the same trusted CA chain
- renewed certificates propagated to every participating node
- node join, replacement, and handshake failures started after certificate rotation or upgrade
- certificates have required SANs and key usages for internode traffic

If internode trust is inconsistent, fix the chain consistency first. Avoid repeated node replacement attempts until the CA chain and node certificates are aligned.

## Client-Side Follow-Up

After Redis certificates are renewed, clients may still fail until they reload trust material.

Check:

- application containers or services restarted after truststore update
- Java JKS/PKCS12 bundles include the new CA/intermediate
- `redis-cli` or SDK was built with TLS support
- connection uses the endpoint hostname that matches certificate SANs, not a raw IP
- service mesh, proxy, or load balancer certificates are also renewed if they terminate TLS

## Monitoring And Prevention

Add expiry visibility for all relevant certificate surfaces:

- scrape or script days-until-expiry for Redis node certificate files and externally presented endpoints
- alert owners before expiration with enough time for CA issuance and change approval
- track certificate owner, issuing CA, renewal mechanism, and rollback location
- monitor `node_cert_expiration_seconds` when available in the Redis Software Prometheus metrics
- schedule post-renewal validation from representative clients

## Common Findings

| Finding | Meaning | Fix |
| --- | --- | --- |
| only one certificate renewed | partial rotation left another path expired | identify all failing scopes and renew each supported cert |
| chain contains duplicate entries | clients may reject the chain | rebuild the full chain without loops |
| OCSP warning with self-signed material | revocation checks are not available | use CA-issued certificates when policy requires OCSP |
| client truststore still has old CA | Redis is fixed but clients reject it | update truststores and restart clients |
| hostname validation fails | certificate SAN does not match endpoint | use the correct FQDN or reissue cert with correct SANs |

## Validation

Validate both Redis and client views:

```bash
openssl s_client -connect <host>:<port> -servername <host> </dev/null
rladmin status issues_only
```

Confirm:

- presented certificates are not expired
- full chain validates from representative clients
- UI, API, database endpoints, syncer, and metrics paths work as applicable
- node join/replace and internode handshakes are stable
- no new certificate warnings appear in logs or monitoring

## Escalate When

- UI/API access is blocked and supported certificate replacement cannot be executed
- internode certificates expired or CA chains differ across nodes
- nodes cannot join or replace after rotation
- multiple certificate scopes expired at once
- private keys, truststores, or persistence locations are suspected to be missing
- data-path TLS and control-plane TLS are failing simultaneously
