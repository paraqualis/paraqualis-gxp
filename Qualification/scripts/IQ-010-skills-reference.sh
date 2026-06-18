#!/usr/bin/env bash
# IQ-010 / IQ-AI-011: Verify skill SKILL.md files and reference corpora;
#                      verify sub-agent frontmatter fields.
# Expected corpus files sourced from SKILL.md directives.
# Read-only. Emits PASS or FAIL.
set -uo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
FAILURES=0
echo "IQ-010 / IQ-AI-011  Skills, reference corpora, and sub-agent check"

for skill_dir in "$REPO_DIR/skills"/*/; do
  skill=$(basename "$skill_dir"); skill_md="$skill_dir/SKILL.md"
  if [ ! -f "$skill_md" ]; then echo "  FAIL  SKILL.md missing: $skill"; FAILURES=$((FAILURES+1)); continue; fi
  if grep -q "^name:" "$skill_md" && grep -q "^description:" "$skill_md"; then
    echo "  OK skill:   $skill (name + description found)"
  else
    echo "  FAIL skill: $skill missing name or description"; FAILURES=$((FAILURES+1))
  fi
done

for path in \
  "skills/gamp-advisor/reference/gamp5-category-framework.md" \
  "skills/gamp-advisor/reference/ai-ml-validation.md" \
  "skills/part11-advisor/reference/21-cfr-part-11.md"; do
  full="$REPO_DIR/$path"
  if [ -s "$full" ]; then echo "  OK corpus:  $path ($(wc -l < "$full" | tr -d ' ') lines)"
  else echo "  FAIL corpus: $path (missing or empty)"; FAILURES=$((FAILURES+1)); fi
done

for agent in "$REPO_DIR/agents"/*.md; do
  name=$(basename "$agent"); ok=1
  for field in "^description:" "^tools:" "^model:"; do
    grep -q "$field" "$agent" || { echo "  FAIL agent $name: missing ${field#^}"; FAILURES=$((FAILURES+1)); ok=0; }
  done
  [ $ok -eq 1 ] && echo "  OK agent:   $name (description + tools + model present)"
done

[ $FAILURES -eq 0 ] && { echo "PASS  All skills, corpora, and sub-agents verified"; exit 0; }
echo "FAIL  $FAILURES item(s) failed"
exit 1
