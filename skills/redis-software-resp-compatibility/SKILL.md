---
name: redis-software-resp-compatibility
description: "Configure and troubleshoot RESP2 and RESP3 compatibility in Redis Enterprise Software. Use when the user asks how to enable or disable RESP3 with `rladmin`, set `resp3_default`, pin Go-Redis or Lettuce to RESP2, debug `HELLO` or `NOPROTO` errors, handle client disconnects after RESP3 changes, use sharded Pub/Sub or client-side caching, or plan RESP behavior during Redis Software upgrades."
---

# Redis Software RESP Compatibility

Use this skill when Redis Enterprise Software protocol negotiation affects clients, features, or upgrades.

## Core Model

RESP2 is the compatibility baseline. RESP3 enables newer protocol behavior and features, but clients must explicitly support it and may receive different response shapes.

When RESP3 is enabled on a database, RESP2 clients can still connect; clients negotiate protocol with `HELLO`. Disabling RESP3 can disconnect clients currently using RESP3.

Some clients issue `HELLO` automatically during connection startup. A working `redis-cli` test that stays on RESP2 does not prove application clients can negotiate RESP3.

## Database Configuration

Enable RESP3:

```bash
rladmin tune db db:<id> resp3 enabled
```

Disable RESP3:

```bash
rladmin tune db db:<id> resp3 disabled
```

REST API shape:

```json
{
  "resp3": true
}
```

For Active-Active databases, confirm all participating databases support the intended RESP configuration before changing it.

## HELLO Diagnostics

Check cluster and database settings:

```bash
rladmin info cluster
rladmin info db <database-name-or-db:id>
rladmin status extra all
```

Look for the database `resp3` setting, the cluster `resp3_default` policy for new databases, and the database Redis version. Verify current Redis Software RESP compatibility docs before relying on a specific version threshold.

Test protocol negotiation from a credential-safe shell:

```text
HELLO 3
HELLO 2
HELLO
```

If authentication is required, authenticate first or use inline `HELLO` auth with the correct username:

```text
HELLO 3 AUTH <username> <password>
```

Do not paste real credentials into chat, tickets, or shell history.

## Default For New Databases

Set cluster policy for future databases only:

```bash
rladmin tune cluster resp3_default disabled
```

REST API shape:

```json
{
  "resp3_default": false
}
```

Changing the default does not automatically change existing databases.

## Client Guidance

Pin clients to RESP2 during migrations when:

- The application has not validated RESP3 response structures.
- Client wrappers or Search/JSON extensions expect RESP2.
- You are upgrading Redis and clients in stages.
- RESP3 push messages or tracking invalidations are not handled.

Go-Redis shape:

```go
redis.NewClient(&redis.Options{
    Addr: "host:port",
    Protocol: 2,
})
```

Lettuce shape:

```java
client.setOptions(ClientOptions.builder()
    .protocolVersion(ProtocolVersion.RESP2)
    .build());
```

Verify exact client option names against the installed client version.

## Feature Requirements

| Feature | RESP guidance |
| --- | --- |
| Basic Redis commands | RESP2 is broadly compatible. |
| Sharded Pub/Sub | Requires RESP3 support. |
| Client-side caching/tracking features | Typically require RESP3 and compatible Redis/client versions. |
| Mixed 7.x/8.x environments | Pin RESP2 unless RESP3 is fully validated across clients and wrappers. |

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Client disconnects after disabling RESP3 | Client negotiated RESP3 and was forced off | Restart client and pin RESP2 or re-enable RESP3. |
| `ERR unknown command 'HELLO'` | Server or proxy path does not support the client's negotiation path | Confirm Redis Software/database version and pin client to RESP2 if upgrade is not immediate. |
| `HELLO` or `NOPROTO` errors | Client/server protocol mismatch | Confirm Redis Software version, database RESP3 setting, and client support. |
| `NOAUTH Authentication required` during `HELLO` | Client negotiated before authenticating or omitted inline auth | Use `AUTH` first or `HELLO 3 AUTH <username> <password>`. |
| `ERR syntax error` | Invalid `HELLO` syntax or missing auth fields | Recheck argument order and username/password mode. |
| `redis-cli` works but app fails | CLI stayed on RESP2 while app defaults to RESP3 | Inspect app client protocol option and pin RESP2 or enable RESP3 deliberately. |
| Sharded Pub/Sub unavailable | RESP3 disabled or unsupported client | Enable RESP3 and use a compatible client. |
| Client-side caching fails | RESP3 or feature version not available | Verify Redis Software and client support before enabling. |
| Application parsing errors | RESP3 response shapes differ from RESP2 | Pin RESP2 or update parsing/client wrapper. |
| New DB behaves differently than old DB | `resp3_default` differs from existing DB settings | Check per-database `resp3` and cluster default policy. |

## Change Plan

1. Inventory client libraries and versions.
2. Decide per database whether RESP3 is required.
3. Stage client changes before database protocol changes.
4. Recycle connection pools after changing RESP settings.
5. Monitor disconnects, protocol errors, and application parsing failures.

## Evidence To Collect

- Redis Enterprise Software version.
- Database `resp3` setting and cluster `resp3_default`.
- Database Redis version from `rladmin status extra all`.
- Client library names and versions.
- Protocol mode configured in the client.
- Exact `HELLO`, `NOPROTO`, disconnect, or parsing error.
- Whether auth is sent before `HELLO`, inline with `HELLO`, or not at all.
- Whether features such as sharded Pub/Sub or client-side caching are required.
