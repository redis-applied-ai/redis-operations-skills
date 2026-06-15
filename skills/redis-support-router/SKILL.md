---
name: redis-support-router
description: Use when a Redis support question is about contacting Redis Support, opening or escalating support tickets, tracking ticket status, understanding support scope, checking known issues or open bugs, using the knowledge base, or contributing/reviewing support knowledge base articles, and the answer should route to the right support workflow or product-specific support skill.
---

# Redis Support Router

Use this skill to classify support-adjacent requests before applying a more specific Redis product or ticket workflow.

## Route By Request Type

| User need | Route |
| --- | --- |
| Find, update, or reply to an existing ticket | Use `redis-support-ticket-lookup`. |
| Open a new support case | Collect product, deployment, urgency, impact, evidence, and Support Portal access details. |
| Escalate an existing case | Ask for ticket number, business impact, production status, timeline, and missing decision or action. |
| Understand support priority or SLA | Verify current entitlement and official support terms; do not guess SLA commitments. |
| Determine what Redis supports | Classify product, deployment type, version, integration, and whether the issue is Redis-managed, customer-managed, client-code, network, or third-party. |
| Search known issues or open bugs | Collect exact version, product, feature, error text, and reproducible behavior before searching. |
| Use or improve the knowledge base | Treat as content workflow: article scope, audience, evidence, review owner, and stale/current status. |

## Intake Checklist

For any support routing response, gather:

- Redis product: Cloud, Software, Kubernetes, Open Source, Insight, Query Engine, or other
- environment: production, staging, local, region/provider if relevant
- affected account, subscription, database, cluster, or ticket ID with sensitive data redacted
- exact symptom, error, timestamps, and first occurrence
- business impact and urgency
- recent changes: maintenance, upgrade, deploy, certificate, network, billing, or access changes
- existing ticket number or whether a new ticket is needed

## Escalation Guidance

When the user asks to escalate, avoid generic pressure language. Provide a concise escalation packet:

1. Ticket number and current status.
2. Production impact, customer impact, and time sensitivity.
3. What answer or action is blocked.
4. Evidence already supplied.
5. Requested next step from Redis Support.

Do not promise a response time unless current support terms and entitlement have been verified.

## Known Issue Triage

Before treating something as a bug, confirm:

- exact Redis product and version
- deployment method and topology
- feature or command involved
- minimal reproduction or evidence
- whether the behavior started after upgrade, maintenance, or configuration change
- whether official docs or release notes describe the behavior

If the issue is product-specific, route to the corresponding product support router skill.

## Knowledge Base Contribution

Use a KB workflow only when the user is creating or revising support content. A good support article should define:

- customer symptom and search terms
- affected product and versions
- cause or decision logic
- step-by-step resolution
- safety warnings and escalation criteria
- validation steps
- review owner and freshness trigger
