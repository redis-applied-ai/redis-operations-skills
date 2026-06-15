---
name: redis8-customer-managed-internode-certificates
description: Use when troubleshooting Redis Software 8 customer-managed internode encryption certificates, CPINE or DPINE certificate uploads, internode TLS handshake failures, node join or replacement failures after customer-managed certificate rotation, RSA key requirements, weak key errors, incomplete CA chains, mismatched certificate/private key pairs, fallback to self-signed internode certificates, `node_cert_expiration_seconds`, or Redis Enterprise for Kubernetes custom INE support questions.
---

# Redis 8 Customer-Managed Internode Certificates

Use this skill for customer-managed certificates that secure Redis Software internode encryption, including control-plane and data-plane internode traffic. Verify current Redis Software and Redis Enterprise for Kubernetes release notes before relying on version-specific support behavior.

## Safety Rules

- Never ask users to paste private keys, full PEM bundles, keystores, or secrets into chat.
- Treat certificate rotation as a production change unless the environment is disposable.
- Keep the previous known-good certificate and key pair securely available for rollback.
- Validate certificate/key/chain before upload.
- Confirm client and node trust stores before switching from self-signed to CA-issued material.

## Scope

Use this skill for internode encryption certificate issues such as:

- CPINE or DPINE customer-managed certificate upload
- node-to-node TLS handshake failures
- cluster communication errors after certificate rotation
- node join or replace failures after enabling customer-managed certificates
- unexpected fallback to self-signed internode certificates

For client-facing cluster certificates or generic credential rotation, use `redis-software-credential-certificate-rotation` or `redis-software-cluster-certificate-rollback`.

## Certificate Requirements To Verify

Check:

- certificate and private key are PEM formatted
- private key matches the certificate
- full chain is present: leaf, intermediate, and root as required by the deployment
- certificate is not expired and not near the product's fallback threshold
- SANs and names match node and endpoint expectations
- key type and strength are supported by the Redis Software and OS/OpenSSL combination
- source-derived baseline: RSA keys only, with at least 2048 bits for modern RHEL/OpenSSL environments

Do not assume ECDSA, short RSA keys, or incomplete chains are acceptable without current-version confirmation.

## Common Error Interpretation

| Error | Likely meaning | Action |
| --- | --- | --- |
| `x509: certificate signed by unknown authority` | Missing or wrong CA chain/trust store. | Install or upload the correct CA chain. |
| `remote error: tls: bad certificate` | Key/cert mismatch or incomplete chain. | Validate key pairing and bundle order. |
| `tls: handshake failure` | TLS version, cipher, or certificate compatibility issue. | Check TLS/cipher compatibility and cert attributes. |
| `certificate verify failed` | Expired cert, SAN mismatch, or trust problem. | Check expiry, SAN, and CA chain. |
| `cluster join failed: unable to establish secure channel` | Joining node lacks matching trust/cert material. | Align node trust and certificate configuration. |
| `certificate verify failed: key too weak` | RSA key below accepted strength. | Replace with a supported stronger RSA key. |
| `no shared cipher` | Cipher mismatch. | Verify supported cipher suites and TLS versions. |
| `wrong version number` | Client/server protocol mismatch or missing TLS flag. | Confirm the caller uses TLS correctly. |

## Upload And Rotation Checks

Before upload:

```bash
openssl x509 -in <cert.pem> -noout -text
openssl rsa -in <key.pem> -check -noout
```

Confirm key/cert match with approved local tooling; do not expose key material.

Upload through the supported UI, CLI, or REST API path for the Redis Software version, such as the cluster certificate API when applicable. If the API rejects the upload, fix the bundle before retrying; do not bypass validation.

After upload:

- confirm propagation to all nodes
- check `rladmin status` and internode communication health
- inspect TLS errors in node and cluster logs
- verify no unexpected fallback to self-signed certificates occurred

## Expiration And Monitoring

Monitor:

- `node_cert_expiration_seconds`
- `customer_managed_ine_certificates`
- UI or monitoring alerts for certificate expiry and fallback state

Source-derived behavior says UI expiry alerts can begin around 45 days before expiry and fallback to self-signed can occur near the final days before expiry. Treat exact thresholds as version-specific and verify current docs before setting production alert policy.

## Kubernetes Caveat

The source baseline says Redis Enterprise for Kubernetes `8.0.2-2` does not support custom internode encryption certificates. Verify current REK release notes before answering any Kubernetes custom INE support question.

## Escalation Packet

Collect with secrets redacted:

- Redis Software or REK version
- certificate scope: CPINE, DPINE, client-facing, or other
- upload method and API/UI validation response
- certificate metadata: issuer, subject, SANs, expiry, key type, key size, chain length
- exact TLS or join error text
- affected nodes and whether fallback occurred
- `rladmin status` and relevant TLS/node logs
- whether previous working certificate material is available
