---
name: redis-insight-support-router
description: Use when a user asks a broad Redis Insight question and you need to route it to onboarding, installation, database connection, data browsing, performance monitoring, DNS, TLS certificates, connection limits, 429 login errors, Docker image security, Kubernetes or Rancher installation issues, corrupted connection files, or unsupported Redis Insight use cases.
---

# Redis Insight Support Router

Use this skill to classify Redis Insight questions and choose the right diagnostic path. It is a router, not a replacement for product documentation. Verify current Redis Insight versions, packaging, container images, and supported deployment modes before giving version-specific guidance.

## Classify The Request

Route the user into one of these tracks:

- Onboarding: first use, install, basic configuration, connecting a database.
- Data management: browsing keys, editing data, viewing JSON or hashes, missing data display.
- Performance monitoring: latency, slow commands, metrics, and dashboards.
- Connectivity: refused connections, timeouts, endpoint changes, DNS lookup failures, network allowlists.
- TLS and security: certificates, CA chains, SNI, mTLS, secure container images, CVE questions.
- Quota and resource limits: max clients, too many concurrent connections, 429 login or API errors.
- Installation and deployment: desktop install, Docker, Kubernetes, Rancher, container startup failures.
- State and configuration files: corrupted or missing Redis Insight connection metadata.
- Feature limitations: unsupported connection patterns, automation expectations, and Redis Cloud role limitations.

## Intake Checklist

Ask for:

- Redis Insight version and deployment type
- operating system or Kubernetes distribution
- target Redis product: Redis Cloud, Redis Software, Kubernetes, or local Redis
- connection endpoint, port, TLS requirement, and authentication method
- exact error text and screenshot if UI-specific
- whether the issue affects all databases or one connection
- recent changes to endpoints, DNS, certificates, credentials, network policy, or browser profile

## Routing Guidance

- For first-time setup, use an onboarding and connection workflow.
- For connection failures, test network reachability, TLS configuration, ACL credentials, and endpoint correctness before changing Redis Insight settings.
- For DNS issues, compare hostname resolution from the Redis Insight runtime environment, not only from the user's laptop.
- For TLS errors, inspect CA trust, certificate hostname/SNI, certificate expiration, and whether Redis requires mTLS.
- For missing data display, confirm database selection, key pattern, data type, permissions, and whether the key exists from `redis-cli`.
- For max-client errors, inspect Redis server connection count, Redis Insight polling behavior, and other clients.
- For 429 errors, check retry behavior, automation loops, login/session behavior, and rate limiting.
- For container security questions, verify the currently published Redis Insight image and vulnerability status from official sources.

## Response Pattern

When answering:

1. Name the selected troubleshooting track.
2. Ask for only the missing evidence needed to proceed.
3. Provide the first two or three checks in order.
4. State when current product documentation or image metadata must be verified.
