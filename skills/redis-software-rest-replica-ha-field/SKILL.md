---
name: redis-software-rest-replica-ha-field
description: Use when Redis Software REST API database creation or update rejects replica_ha, slave_ha, or another replica high-availability field, especially with POST /v1/bdbs, bdb JSON payload validation, SDK examples that differ from HTTP API schema, Kubernetes REDB ReplicaHA confusion, or cluster-level versus database-level Replica HA configuration.
---

# Redis Software REST Replica HA Field

Use this skill when a Redis Software REST API payload fails because the replica high-availability field name does not match the REST API version being called.

## Core Rule

Match the JSON payload to the actual HTTP API endpoint version exposed by the cluster, not to a generic SDK example or newer documentation snippet. Verify the current REST schema for the Redis Software release before changing automation broadly.

## Diagnostic Flow

1. Capture the endpoint path, for example `POST /v1/bdbs`.
2. Capture the exact validation error.
3. Inspect the request body for `replica_ha`, `slave_ha`, or similar HA fields.
4. Check the REST API schema for that endpoint and Redis Software version.
5. Change only the field name needed to match the schema.
6. Retry in a non-production or safe workflow if possible.

## Field Guidance

For older `/v1` style bdb endpoints, the accepted field may be:

```json
{
  "slave_ha": true
}
```

Do not use:

```json
{
  "replica_ha": true
}
```

unless the cluster's REST API version explicitly documents and accepts it.

## Configuration Scope

Replica high availability can require both:

- cluster-level Replica HA capability or policy
- database-level HA setting

In Kubernetes, enabling Replica HA at the Redis Enterprise Cluster level does not necessarily enable it for every RedisEnterpriseDatabase resource. Check the operator resource fields and the Redis Enterprise API behavior for the deployed version.

## Escalation Conditions

Escalate or verify with support when:

- the documented schema and live API behavior disagree
- the API version appears correct but the field is still rejected
- Replica HA is accepted in the payload but not active in the database
- Active-Active behavior differs from the requested database setting

## Response Pattern

Answer with:

1. The API endpoint version being called.
2. The field name accepted by that endpoint.
3. The corrected JSON fragment.
4. A reminder to verify cluster-level and database-level Replica HA state.
5. Escalation criteria if the schema and live behavior conflict.
