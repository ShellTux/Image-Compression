#!/bin/sh
set -e

find src -type f -name "*step[012345]_*.py" \
  | grep --invert-match test \
  | sort --unique \
  | while IFS= read -r script
do
  step="$(echo "$script" | grep --only-matching 'step[0-9]')"
  # echo "step = $step, script = $script"

  [ "$(find "docs/$step" -type f 2>/dev/null | wc --lines)" -ne 0 ] && continue

  echo "$script"
done \
  | parallel -j2 python {} --hide-figures 2>/dev/null
