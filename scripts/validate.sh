#!/usr/bin/env bash
# Validates every skills/*/SKILL.md against the Agent Skills spec
# (https://agentskills.io/specification) plus this repo's house rules.
# No dependencies beyond POSIX tools; runs on macOS bash 3.2.
set -u
cd "$(dirname "$0")/.." || exit 1

fail=0
count=0

for f in skills/*/SKILL.md; do
  if [ ! -e "$f" ]; then
    echo "FAIL: no skills/*/SKILL.md found"
    exit 1
  fi
  count=$((count + 1))
  dir=$(basename "$(dirname "$f")")

  if [ "$(head -n 1 "$f")" != "---" ]; then
    echo "FAIL $f: missing YAML frontmatter"
    fail=1
    continue
  fi

  fm=$(awk 'NR==1{next} /^---$/{exit} {print}' "$f")
  name=$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -n 1)
  rawdesc=$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -n 1)
  case "$rawdesc" in
    \"*\") desc=$(printf '%s' "$rawdesc" | sed -e 's/^"//' -e 's/"$//' -e 's/\\"/"/g') ;;
    *)
      desc="$rawdesc"
      # An unquoted YAML scalar cannot contain ': ' or ' #': real parsers reject the file and installers skip the skill.
      case "$rawdesc" in *": "*|*" #"*) echo "FAIL $f: description must be double-quoted (contains ': ' or ' #')"; fail=1 ;; esac ;;
  esac

  [ -n "$name" ] || { echo "FAIL $f: name is missing"; fail=1; }
  [ -n "$desc" ] || { echo "FAIL $f: description is missing (must be a single line)"; fail=1; }

  if ! printf '%s' "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$'; then
    echo "FAIL $f: name '$name' must be lowercase a-z, 0-9, single hyphens"
    fail=1
  fi
  [ "${#name}" -le 64 ] || { echo "FAIL $f: name is ${#name} chars (max 64)"; fail=1; }
  [ "$name" = "$dir" ] || { echo "FAIL $f: name '$name' != directory '$dir'"; fail=1; }
  [ "${#desc}" -le 1024 ] || { echo "FAIL $f: description is ${#desc} chars (max 1024)"; fail=1; }

  case "$desc" in
    "Use when"*) ;;
    *) echo "FAIL $f: description should start with 'Use when'"; fail=1 ;;
  esac

  lines=$(wc -l < "$f" | tr -d ' ')
  [ "$lines" -le 500 ] || { echo "FAIL $f: $lines lines (max 500 — move detail to references/)"; fail=1; }
done

if [ "$fail" -eq 0 ]; then
  echo "OK: $count skill(s) valid"
fi
exit "$fail"
