---
name: redis-software-cluster-deployment
description: "Deploy Redis Software clusters after installation on all nodes. Use when the user asks to create a Redis Enterprise Software cluster, join nodes, choose Cluster Manager UI versus REST API versus rladmin deployment, run `/v1/bootstrap`, use `/v1/cluster/join`, run `rladmin cluster create`, validate `rladmin status`, or handle permanent cluster-name and license matching requirements."
---

# Redis Software Cluster Deployment

Use this skill to guide initial Redis Software cluster creation after Redis Software has been installed on every node that will join the cluster.

## Preflight Checks

- Redis Software is installed on all intended cluster nodes.
- Network connectivity is open between nodes.
- DNS/FQDN planning is complete.
- The cluster name matches the license agreement and is treated as permanent.
- Admin email and password are available through a secure channel; do not ask users to paste secrets into chat.
- Persistent storage path and rack-zone design are known if they will be configured during setup.

## Method Selection

| Method | Use when |
| --- | --- |
| Cluster Manager UI | Human-led setup, small deployments, or first-time onboarding. |
| REST API | Automated provisioning or repeatable deployment workflows. |
| `rladmin` CLI | Shell access is available and the operator prefers direct cluster commands. |

## Cluster Manager UI Workflow

1. Open `https://<node-ip>:8443` on the first node.
2. Choose `Create New Cluster`.
3. Enter the permanent cluster name, admin email, and admin password.
4. Submit the form and wait for initialization.
5. On each additional node, open the UI and choose `Join Cluster`.
6. Provide the first node IP and the same admin credentials.
7. Configure optional settings such as rack-zone awareness or persistent storage path if required.
8. Verify every node appears online.

## REST API Workflow

1. Bootstrap the first node with the supported payload:

   ```http
   POST https://<node-ip>:9443/v1/bootstrap
   ```

2. Join each additional node through the supported cluster-join request:

   ```http
   POST https://<node-ip>:9443/v1/cluster/join
   ```

3. Include the first node IP and admin credentials through the approved secret-handling path.
4. Apply optional cluster configuration through documented REST endpoints.
5. Verify cluster status through REST, UI, or `rladmin`.

## rladmin Workflow

Create the cluster on the first node:

```bash
rladmin cluster create name <cluster-name> username <admin-email> password '<admin-password>'
```

Join additional nodes:

```bash
rladmin cluster join username <admin-email> password '<admin-password>' nodes <first-node-ip>
```

Then verify:

```bash
rladmin status
rladmin cluster status
```

## Validation

Confirm:

- All expected nodes are online.
- No node is failed, unreachable, or pending join.
- Cluster name/FQDN matches the intended license and DNS plan.
- Rack-zone awareness and persistent storage path are configured as intended.
- Cluster Manager UI login works.
- The cluster is ready for database creation and security configuration.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| License or cluster name mismatch | Cluster name is permanent and may require rebuild if wrong. |
| Node cannot join | First node IP, credentials, firewall, node reachability, time sync, and installed version. |
| UI unreachable on port 8443 | Host firewall, service health, node IP, and browser TLS warning handling. |
| REST bootstrap fails | Payload, port 9443 reachability, credentials, and whether the node is already part of a cluster. |
| `rladmin status` incomplete | Join operation still running, node health, or inter-node communication issue. |

## Escalation Packet

Collect:

- Redis Software version on every node.
- Cluster name and license expectation.
- Deployment method used.
- Node IPs and hostnames.
- Failure step and exact error with credentials redacted.
- `rladmin status` and `rladmin cluster status`.
- Network/firewall checks for UI, REST, and inter-node traffic.
