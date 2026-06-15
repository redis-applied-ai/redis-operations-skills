#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="${SKILL_VALIDATOR:-}"

if [[ -z "$validator" ]]; then
  for candidate in \
    "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" \
    "$HOME/.codex/skills/skill-creator/scripts/quick_validate.py" \
    "$HOME/.claude/skills/skill-creator/scripts/quick_validate.py"
  do
    if [[ -f "$candidate" ]]; then
      validator="$candidate"
      break
    fi
  done
fi

if [[ -z "$validator" || ! -f "$validator" ]]; then
  cat >&2 <<'EOF'
Could not find quick_validate.py.
Set SKILL_VALIDATOR to the validator path, for example:
  SKILL_VALIDATOR=/path/to/quick_validate.py ./scripts/validate-skills.sh
EOF
  exit 1
fi

if [[ ! -d "$repo_root/skills" ]]; then
  echo "No skills directory found at $repo_root/skills" >&2
  exit 1
fi

python_cmd=(python3)
if ! python3 - <<'PY' >/dev/null 2>&1
import yaml
PY
then
  if command -v uv >/dev/null 2>&1; then
    python_cmd=(uv run --quiet --with pyyaml python)
  else
    cat >&2 <<'EOF'
quick_validate.py requires PyYAML.
Install PyYAML for python3 or install uv so this script can run:
  uv run --with pyyaml python
EOF
    exit 1
  fi
fi

validated=0
while IFS= read -r -d '' skill_dir; do
  "${python_cmd[@]}" "$validator" "$skill_dir" >/dev/null
  printf 'valid %s\n' "${skill_dir#$repo_root/}"
  validated=$((validated + 1))
done < <(find "$repo_root/skills" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

printf 'validated %d skill directories\n' "$validated"
