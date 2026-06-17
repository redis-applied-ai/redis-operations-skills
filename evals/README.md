# Redis Operations Skill Evals

This directory contains a fixture-backed harness for comparing a reasoning GPT model with and without Redis operations skills loaded.

## Run Locally

Use the fixture provider for a local smoke test that does not require an OpenAI API key:

```bash
uv run --with pydantic --with pyyaml python evals/run_skill_evals.py --scenario cloud-delete-prod-cache-no-backup --variant both
```

Use the OpenAI Agents SDK provider for real model evals:

```bash
export OPENAI_API_KEY=<openai-api-key>
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

## GitHub Actions

The `Skill evals` workflow runs deterministic fixture checks and a live OpenAI smoke eval.

Configure the live eval credentials on the GitHub repository:

```bash
gh secret set OPENAI_API_KEY --repo redis-applied-ai/redis-operations-skills --body "$OPENAI_API_KEY"
gh variable set OPENAI_EVAL_MODEL --repo redis-applied-ai/redis-operations-skills --body "$OPENAI_EVAL_MODEL"
```

`OPENAI_EVAL_MODEL` may be stored as a secret instead of a variable if needed. The workflow fails if either value is missing, because the live job should not silently fall back to fixture mode.

## Outputs

Runs write per-run JSON, per-run JSONL transcript traces, and summary artifacts under `evals/artifacts/<timestamp>/`.

Artifacts are ignored by git.
