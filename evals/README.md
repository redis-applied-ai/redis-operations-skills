# Redis Operations Skill Evals

This directory contains a fixture-backed harness for comparing a reasoning GPT model with and without Redis operations skills loaded.

## Run Locally

Use the fixture provider for a local smoke test that does not require an OpenAI API key:

```bash
uv run --with pydantic --with pyyaml python evals/run_skill_evals.py --scenario cloud-delete-prod-cache-no-backup --variant both
```

Use the OpenAI Agents SDK provider for real model evals:

```bash
OPENAI_EVAL_MODEL=<reasoning-gpt-model> \
uv run --with openai --with openai-agents --with pydantic --with pyyaml \
  python evals/run_skill_evals.py --provider openai --scenario cloud-delete-prod-cache-no-backup --variant both
```

Run the benchmark shape from `SPEC.md`:

```bash
OPENAI_EVAL_MODEL=<reasoning-gpt-model> \
uv run --with openai --with openai-agents --with pydantic --with pyyaml \
  python evals/run_skill_evals.py --provider openai --variant both --repetitions 5
```

Do not hardcode current model strings in this repository. Choose `OPENAI_EVAL_MODEL` from current official OpenAI model documentation at run time.

## Outputs

Runs write per-run JSON, per-run JSONL transcript traces, and summary artifacts under `evals/artifacts/<timestamp>/`.

Artifacts are ignored by git.
