---
name: redis-cloud-heroku-tls-limitations
description: Use when a Redis Cloud Heroku add-on has no TLS toggle, a user cannot enable TLS on a Heroku-provisioned Redis Cloud database, `rediss://` fails for a Heroku Redis Cloud add-on, a security review requires encryption in transit for a Heroku app, or the user needs to migrate from a Heroku-managed Redis Cloud add-on to a directly managed Redis Cloud database with TLS enabled.
---

# Redis Cloud Heroku TLS Limitations

Use this skill when TLS is required for a Redis Cloud database that was provisioned through the Heroku add-on integration. Verify current Redis Cloud and Heroku add-on documentation before making final support claims.

## Core Decision

Redis Cloud databases created directly in the Redis Cloud Console can support TLS configuration. Heroku-provisioned Redis Cloud add-ons are managed through the Heroku add-on integration; in the source scenario, TLS cannot be enabled there and the TLS control is not exposed.

If TLS is mandatory for compliance or security policy, guide the user toward a directly managed Redis Cloud database and a controlled migration.

## Confirm It Is A Heroku Add-On

Check for:

- database was created from the Heroku Dashboard or Heroku CLI
- application receives Redis connection settings through Heroku config vars
- Redis Cloud Console shows a Heroku-managed context
- TLS or Security toggle is absent for that database
- `redis://` works but `rediss://` fails against the same old endpoint

If the database was created directly in Redis Cloud, use `redis-cloud-database-security-hardening` instead.

## Migration Path For TLS

1. Create a new Redis Cloud database directly in the Redis Cloud Console.
2. Enable TLS on the new database.
3. Download or configure the required CA certificate material if the client validates server certificates.
4. Test connectivity with `rediss://` or explicit client TLS settings from a controlled environment.
5. Choose a migration method:
   - backup and restore
   - application-level dual write or copy
   - live sync or replication tooling if supported for the environment
6. Update all application configuration to the new TLS-enabled endpoint.
7. Redeploy web dynos, workers, scheduled jobs, and one-off job definitions that read Heroku config vars.
8. Validate reads, writes, background jobs, connection pooling, latency, and error rates.
9. Decommission the old Heroku add-on only after the new database is stable.

## Common Mistakes

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `rediss://` still fails | App is still pointing at the Heroku add-on endpoint. | Verify hostname, port, and config vars. |
| TLS toggle is missing | Database is Heroku-managed. | Use a directly managed Redis Cloud database for TLS. |
| Certificate verification fails | Client does not trust the Redis Cloud CA bundle. | Configure CA trust according to the client library. |
| Web works but workers fail | Non-web dynos still use old config or were not redeployed. | Update every process type and scheduled job. |
| Security review remains blocked | Migration plan lacks proof. | Provide TLS endpoint, client config, certificate validation, and cutover evidence. |

## Response Pattern

When answering:

1. State whether the database appears Heroku-managed or directly managed.
2. Explain whether TLS can be configured in that control plane.
3. If TLS is required, outline the migration path and the data-movement option to evaluate.
4. Call out all app components that must receive the new connection string.
5. Define validation before old add-on decommissioning.
