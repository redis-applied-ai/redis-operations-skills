# Redis Operations Skills

Redis Operations Skills is a collection of Agent Skills for Redis platform operations, support triage, and production troubleshooting. The repository uses the open Agent Skills layout: each skill is a self-contained directory under `skills/` with a required `SKILL.md` file and optional bundled resources such as `scripts/`, `references/`, and `assets/`.

These skills are distilled operational workflows. They intentionally do not include source knowledge-base articles or full article copies.

## Repository Layout

```text
.
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── scripts/      # optional executable helpers
│       ├── references/   # optional detailed reference material
│       └── assets/       # optional templates or reusable assets
└── scripts/
    └── validate-skills.sh
```

At setup time, this repository contains 246 skill bundles.

## Topic Areas

The skills cover Redis operations across these areas:

- **Redis Cloud operations**: account setup, database creation, connection workflows, backups, alerts, monitoring, failover tests, maintenance notifications, API usage, Terraform behavior, version policy, Flex, Essentials, Pro, and platform orientation.
- **Redis Cloud billing and marketplace workflows**: invoices, payment failures, credit-card retries, cost reports, network transfer charges, post-cancellation billing, plan-change billing, AWS Marketplace, GCP Marketplace, private offers, ownership, permissions, and account deletion.
- **Redis Cloud security and access**: RBAC, Data ACLs, credential rotation, TLS, IP allow lists, VPC peering, private networking, authentication errors, account recovery, team access, SAML/SSO, and Okta troubleshooting.
- **Redis Software operations**: installation, cluster deployment, licensing, DNS, firewalls, storage, persistence, logging, auditing, monitoring, support packages, node maintenance, upgrades, rollback, certificate management, and cluster recovery.
- **Redis Enterprise for Kubernetes and OpenShift**: REC/REDB licensing, FQDN discovery, rack awareness, reconciliation behavior, degraded recovery, pod restart triage, secret/auth changes, TLS failures, Istio ingress, VKS support, and OpenShift-specific troubleshooting.
- **Active-Active and CRDB**: CRDB creation, resize, shard scaling, replication link failures, sync stalls, tombstone memory, credential sync, multi-key command guardrails, migration, flush safety, and participant reachability.
- **Search, Query Engine, Redis 8, and vector workloads**: index creation, document ingestion, `FT.EXPLAIN`, `FT.PROFILE`, `FT.DROPINDEX DD`, Redis 8 command deprecations, ACL category migration, RESP compatibility, JSON modeling, numeric/date precision, vector search architecture, RedisVL-oriented design, and faceted search.
- **Performance, capacity, and reliability**: high memory and high network usage, throughput sizing, right-sizing, hot keys, big keys, large keys, bulk deletion, slow log and `SCAN` diagnostics, connection surges, reconnect storms, Pub/Sub load, endpoint rebinding, failover validation, and latency reduction.
- **Data movement and recovery**: imports, large dataset validation, migration options, OSS-to-Redis Software migration, Sidekiq and CRDB migrations, shard-count reduction, AOF recovery after `FLUSHDB`, backup/restore workflows, and safe deletion.
- **Client and tool workflows**: Redis Insight onboarding, connection, DNS, data exploration, and performance monitoring; `redis-cli` on Windows through Docker or WSL; support-ticket lookup; and product support routing for Redis Cloud, Redis Software, Redis Open Source, Query Engine, Kubernetes, and Redis Insight.

## Using These Skills

Use the `skills/` directory as the canonical source of skill bundles.

For agents that can load an arbitrary skills directory, point the agent at `skills/`.

For Codex user-scope installation, copy or symlink selected skill directories into `$CODEX_HOME/skills` or `~/.codex/skills` when `CODEX_HOME` is unset.

For Codex repository-scope installation, copy or symlink selected skill directories into the target repository's `.agents/skills/` directory.

For Claude or other Agent Skills-compatible clients, install, upload, or package the desired skill directories according to that client's current skill-loading mechanism.

## Skill Authoring Conventions

- Keep one skill per focused operational workflow.
- Keep `SKILL.md` concise and action-oriented.
- Put required trigger coverage in the frontmatter `description`; agents use that field for discovery.
- Use `references/` only for detailed material that should be loaded conditionally.
- Use `scripts/` for repeatable checks or fragile procedures that benefit from deterministic execution.
- Do not copy full source articles into skills.
- Do not hard-code current pricing, cloud-provider support windows, marketplace behavior, or version support without live verification guidance.
- Treat destructive Redis, cloud, billing, and account operations as confirmation-sensitive.

## Validation

Validate all skill bundles after editing:

```bash
./scripts/validate-skills.sh
```

The script uses `SKILL_VALIDATOR` when set. Otherwise, it looks for Codex's local `quick_validate.py` from the `skill-creator` skill:

```bash
SKILL_VALIDATOR=/path/to/quick_validate.py ./scripts/validate-skills.sh
```

Validation should pass before publishing or installing updated skills.
