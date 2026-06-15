---
name: redisgears-upgrade-dependency-recovery
description: "Recover RedisGears failures after Redis Enterprise upgrades caused by missing Python, JVM, shared-library, or application dependencies. Use when RedisGears fails to load, Gears scripts fail on some nodes, `ldd` shows `not found`, Python gears miss packages or `libpython`, JVM gears miss `libjvm` or `JAVA_HOME`, or cluster nodes have inconsistent runtime paths after upgrade."
---

# RedisGears Upgrade Dependency Recovery

Use this skill when RedisGears fails after a Redis Enterprise upgrade or node replacement because runtimes or libraries are missing or inconsistent.

## First Checks

1. Confirm RedisGears is actually used.
2. Identify engines in use:
   - Python.
   - JVM.
   - Both.
3. Identify affected nodes and whether failure is cluster-wide or node-specific.
4. Collect RedisGears version, Redis Enterprise version, OS version, and upgrade timeline.

## Dependency Audit

Run on every Redis Enterprise node that may host RedisGears:

```bash
ldd /path/to/redisgears.so
ldd /path/to/gears_python.so
ldd /path/to/gears_jvm.so
```

Look for `not found`. Any unresolved shared library must be installed or made available consistently on every node.

## Runtime Checks

Python engine:

- Confirm supported Python runtime version for the RedisGears release.
- Confirm `libpython3.x.so` is present and resolvable.
- Confirm required Python packages are installed for the correct interpreter and architecture.
- Capture package inventory with the environment-specific equivalent of `pip freeze`.

JVM engine:

- Confirm compatible JRE/JDK version.
- Confirm `libjvm.so` is present and resolvable.
- Confirm `JAVA_HOME` or the module/runtime configuration points to the intended runtime when required.

## Consistency Rules

All Redis Enterprise nodes should have identical:

- Runtime versions.
- Dependency paths.
- Directory structure.
- File ownership and permissions.
- Application package versions.
- OS/architecture compatibility for native extensions.

A common staging path is a dedicated dependency directory such as `/opt/redislabs/gears-deps/`, but use paths supported by the local deployment and Redis documentation.

## Remediation Workflow

1. Install missing OS libraries, Python runtime/packages, or JVM runtime on all nodes.
2. Make library paths resolvable through the system linker or a documented RedisGears configuration mechanism.
3. Run `ldconfig` only when using system linker paths and after validating the change with the platform owner.
4. Set permissions so Redis processes can read libraries and execute runtime binaries:
   - Directories commonly need execute permission.
   - Shared libraries must be readable.
   - Runtime binaries must be executable.
5. Re-run `ldd` on all nodes.
6. Restart the affected database/module path using the supported Redis Enterprise procedure if the module does not reload automatically.
7. Execute a known safe RedisGears test script and verify behavior on all nodes.

## Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| Module fails to load | Missing `.so` library | Check logs and rerun `ldd`; install missing dependency. |
| Python gears fail at runtime | Missing package or wrong Python/libpython | Verify interpreter, packages, and library path. |
| JVM gears fail to initialize | Missing/incompatible JRE/JDK or `libjvm` path | Install compatible runtime and configure path. |
| Works on some nodes | Node environment mismatch | Diff runtime paths, versions, and package lists across nodes. |
| Permission denied | Redis process cannot read/execute dependency | Fix ownership and modes consistently. |
| Still fails after dependencies installed | Unsupported version combination or module issue | Collect evidence and engage Redis Support. |

## Evidence To Collect

- Redis Enterprise and RedisGears versions.
- Engines used: Python/JVM.
- `ldd` output for Gears modules from each node.
- Redis logs showing module load/runtime errors.
- Python package inventory or JVM version/path details.
- Node-by-node dependency path/version comparison.
- Changes made during the Redis Enterprise upgrade.
