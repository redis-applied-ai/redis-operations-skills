---
name: redis-software-cluster-naming
description: "Choose and validate a Redis Software cluster name before deployment. Use when the user is naming a Redis Enterprise cluster, requesting a license, planning DNS/FQDNs, creating the first node, or troubleshooting license validation caused by cluster-name mismatch, length, casing, special characters, or DNS conflicts."
---

# Redis Software Cluster Naming

Use this skill before Redis Software cluster creation or license request. The cluster name is permanent after creation and affects licensing, DNS, node FQDNs, and database endpoints.

## Naming Rules

- Choose before creating the first node.
- Treat the name as immutable after cluster creation.
- Match the Redis Software license value exactly.
- Keep the name at or below 64 characters.
- Use only lowercase letters, numbers, hyphens, and periods.
- Avoid spaces, underscores, uppercase letters, and special characters.
- Ensure the name is unique across the user's infrastructure.

## Workflow

1. Ask for the intended environment and domain:
   - Production, staging, development, or test.
   - Public or internal DNS zone.
   - Ownership/control of the domain.
2. Propose a clear FQDN-style cluster name:
   - Example: `redis-prod.example.com`.
   - Example: `redis-staging.internal`.
3. Validate the proposed name:
   - Length <= 64 characters.
   - Allowed characters only.
   - Lowercase.
   - Uniqueness in DNS/infrastructure inventory.
   - Exact value intended for license generation.
4. Explain derived names:
   - Node FQDNs commonly follow the cluster domain, such as `node1.<cluster-name>`.
   - Database endpoint names and ports derive from cluster configuration.
5. Before deployment:
   - Confirm the final cluster name with the user.
   - Request or verify the Redis Software license uses the exact name.
   - Use the same name when creating the first node.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| License validation fails | Cluster name does not exactly match license | Compare exact strings, including case and punctuation. |
| License cannot be generated | Name exceeds 64 characters | Shorten before requesting license. |
| DNS or endpoint confusion | Name conflicts with existing infrastructure | Choose a unique name and validate DNS plan. |
| Clients cannot resolve endpoints | DNS zone or node FQDN plan incomplete | Verify node and database endpoint DNS records. |
| User wants to rename an existing cluster | Cluster name is immutable | Plan migration/rebuild rather than rename. |

## Safety Checks

- Do not tell the user a cluster can be renamed in place.
- Do not request a license until the final cluster name is confirmed.
- For current license-generation constraints or naming rules, verify Redis guidance if there is any doubt.

## Final Answer Pattern

When recommending a name, include:

- Proposed cluster name.
- Length and allowed-character validation.
- License exact-match reminder.
- DNS/node endpoint implication.
- A confirmation question before the user requests a license or creates the first node.
