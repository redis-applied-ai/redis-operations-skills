---
name: redis-software-tls-handshake-troubleshooting
description: Use when Redis Software TLS or SSL connections fail with handshake errors, wrong version number, certificate verify failed, tlsv1 alert, no shared cipher, weak key errors, redis-cli missing --tls support, endpoint SSL mode confusion, DNS/SNI mismatch, protocol or cipher suite incompatibility, mTLS certificate/key mismatch, or internode TLS CA-chain problems.
---

# Redis Software TLS Handshake Troubleshooting

Use this skill to diagnose Redis Software TLS failures that are not only certificate expiration. Work from the client symptom to the server-side TLS configuration, then validate certificate, protocol, cipher, DNS, and tooling compatibility.

## Safety Rules

- Never ask for private keys, passwords, client certificates, full HAR files, or unredacted packet captures in chat.
- Do not disable certificate validation in production as a fix; use it only as a controlled diagnostic if the user understands the risk.
- Verify installed Redis Software version and current docs before changing cluster TLS protocol or cipher settings.
- Treat TLS setting changes as production changes because clients may disconnect immediately.

## Symptom Classification

Collect the exact error and client/tool:

- `SSL handshake failed`
- `wrong version number`
- `certificate verify failed`
- `tlsv1 alert`
- `no shared cipher`
- `EE certificate key too weak`
- `Unrecognized option or bad number of args for: --tls`
- timeout or immediate disconnect after enabling TLS

Also collect:

- endpoint host and port, without credentials
- whether database endpoint TLS is required, optional, or disabled
- whether mTLS/client certificate auth is used
- client library and version
- OS/OpenSSL policy, especially on hardened Linux distributions
- recent certificate, endpoint, DNS, load balancer, or Redis Software upgrade changes

## Confirm Redis Software TLS Mode

On a Redis Software node:

```bash
rladmin status endpoints
rladmin info cluster
rladmin status issues_only
```

Check:

- endpoint SSL/TLS mode for the target database
- cluster minimum data/control TLS versions
- configured cipher lists or cipher suites
- whether proxy, control plane, or internode TLS is the failing path
- component health if logs suggest proxy or cluster-manager failure

If the endpoint does not require TLS, a TLS client can fail. If the endpoint requires TLS, a plaintext client can fail with misleading `wrong version number` or disconnect errors.

## Verify Client Tooling

For `redis-cli`, confirm the binary supports TLS:

```bash
redis-cli --help | grep -- --tls
```

If `--tls` is not recognized, use a TLS-enabled Redis CLI build or a trusted container/image that includes TLS support. Do not treat that as a Redis server failure.

Basic TLS test:

```bash
redis-cli -h <hostname> -p <port> --tls --cacert <ca.crt> PING
```

mTLS test:

```bash
redis-cli -h <hostname> -p <port> --tls \
  --cacert <ca.crt> \
  --cert <client.crt> \
  --key <client.key> \
  PING
```

Add auth flags only through a credential-safe method.

## Network, DNS, And SNI

From the same host or pod as the failing client:

```bash
dig <hostname>
nslookup <hostname>
nc -vz <hostname> <port>
openssl s_client -connect <hostname>:<port> -servername <hostname> -showcerts </dev/null
```

Check:

- the hostname resolves to the intended Redis endpoint
- firewall and routing allow the target port
- the client uses the FQDN covered by the certificate SAN, not a raw IP
- SNI is sent when the endpoint or certificate routing requires it
- load balancers or proxies are not terminating TLS with a different certificate

## Certificate And Key Checks

Inspect public certificate details:

```bash
openssl x509 -in <server.crt> -noout -subject -issuer -dates -ext subjectAltName
```

Check key strength when the private key can be inspected securely on the owning host:

```bash
openssl rsa -in <server.key> -text -noout | head
```

For certificate/key mismatch, verify the public modulus or use the environment's approved certificate tooling. Do not move private keys into chat or tickets.

Common checks:

- certificate is not expired
- SAN includes the endpoint hostname
- full CA chain is trusted by the client
- certificate and private key match
- RSA key size and algorithm satisfy the OS crypto policy
- client certificate has expected key usage if mTLS is enabled

If expiration is the primary issue, switch to `redis-software-tls-certificate-expiration-triage`.

## Protocol And Cipher Compatibility

Use `rladmin info cluster` and client/OpenSSL output to compare:

- client-supported TLS versions
- Redis Software minimum TLS versions
- cipher suites allowed by Redis Software
- OS crypto policy restrictions
- Java, OpenSSL, Node, Go, or Python runtime TLS defaults

Examples:

- `no shared cipher`: align client and server cipher support or update the client runtime.
- `wrong version number`: confirm TLS is enabled on both sides and the client is not speaking plaintext to a TLS-only endpoint.
- `tlsv1 alert`: inspect `openssl s_client` details and Redis logs for the specific alert reason.
- weak key errors: replace the certificate with a key that satisfies current OS and security policy.

## Log Sources

Review time-aligned Redis Software logs:

```bash
grep -iE "tls|ssl|handshake|cipher|certificate|verify|x509" /var/opt/redislabs/log/*.log
```

Useful files often include:

- `dmcproxy.log` for database endpoint TLS failures
- `event_log.log` for cluster events
- `cluster_wd.log` for cluster health and internode issues
- database or shard logs when the failure is data-path specific

## Internode TLS And CA Chain

For node join, node replacement, or internode handshake failures:

- verify whether customer-managed internode certificates are enabled
- confirm every node has the same trusted CA chain
- confirm renewed certificates propagated to all nodes
- compare node logs around the join or replace attempt
- verify current Redis Software docs for the installed version before changing internode certificate settings

Do not repeatedly attempt node replacement until CA chain consistency is proven.

## Response Shape

When helping a user, provide:

1. The most likely TLS failure class.
2. The exact client and server-side check to run next.
3. Whether this is client tooling, certificate trust, endpoint mode, protocol/cipher, DNS/SNI, or internode TLS.
4. The smallest safe fix.
5. Validation commands after the fix.
