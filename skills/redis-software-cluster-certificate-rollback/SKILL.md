---
name: redis-software-cluster-certificate-rollback
description: Use when rolling back or replacing Redis Software cluster certificates, reverting from a CA-signed certificate to self-signed, generating a new self-signed certificate, uploading PEM certificate and private key in Cluster Manager, validating SAN and key usage, fixing TLS failures after certificate replacement, or deciding whether reinstallation is necessary.
---

# Redis Software Cluster Certificate Rollback

Use this skill when a Redis Software cluster needs to revert from a custom certificate to a self-signed or replacement certificate. Treat this as certificate replacement, not true rollback.

## Core Rule

Redis Software does not retain previously installed certificates for later rollback. If the prior certificate and key were not backed up, generate and upload a new compatible certificate instead of expecting a restore button.

## Safety Checks

Before changing certificates:

- confirm Cluster Manager admin access
- schedule a maintenance window if clients depend on TLS
- back up the currently installed certificate and private key if accessible
- protect private keys and never paste them into chat or tickets
- confirm client trust stores can be updated
- collect current node hostnames and endpoint names used by clients

## Certificate Requirements

The replacement certificate must include:

- correct Subject Alternative Names for cluster nodes and client-facing hostnames
- matching private key
- appropriate key usage and extended key usage
- compatible key strength and format
- CA chain if a CA is used

For versions with a Redis Software certificate-generation script, prefer the supported script. For older versions, use OpenSSL only with the documented Redis Software certificate structure.

## Replacement Workflow

1. Generate a new certificate and key that match Redis Software requirements.
2. Validate certificate SANs and key pairing before upload.
3. In Cluster Manager, open the certificate management area.
4. Upload the server certificate, private key, and CA certificate if applicable.
5. Apply changes and allow TLS configuration to reload.
6. Update client trust stores if the CA or self-signed certificate changed.

## Validation

After replacement:

```text
redis-cli --tls -h <host> -p <port>
```

Also confirm:

- cluster health is normal
- all nodes are reachable
- inter-node communication works
- clients trust the new certificate or CA
- SAN matches the hostname clients use
- mTLS clients still present trusted client certificates if required

## Troubleshooting

- Clients cannot connect: check trust store, CA chain, SAN hostname match, and certificate/key pairing.
- Nodes report TLS errors: ensure all node DNS names are in SAN and certificate extensions are correct.
- Private key mismatch: regenerate or locate the correct key; do not force upload incompatible materials.
- Considering reinstall: only for full rebuild scenarios, because reinstalling removes cluster configuration.

## Response Pattern

Answer with:

1. Whether the request is true rollback or replacement.
2. The certificate generation path for the Redis Software version.
3. Key SAN, key usage, and trust-store checks.
4. Upload and validation steps.
5. When reinstall is unnecessary or too disruptive.
