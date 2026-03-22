#!/bin/bash
# Ralph Stop Hook — intercepts Claude exit, re-injects prompt if loop is active

RALPH_STATE_FILE="/tmp/ralph_loop_state.json"

if [ ! -f "$RALPH_STATE_FILE" ]; then
  exit 0  # No active Ralph loop — let Claude exit normally
fi

PROMPT=$(python3 -c "import json,sys; d=json.load(open('$RALPH_STATE_FILE')); print(d['prompt'])")
COMPLETION=$(python3 -c "import json,sys; d=json.load(open('$RALPH_STATE_FILE')); print(d['completion_promise'])")
MAX_ITER=$(python3 -c "import json,sys; d=json.load(open('$RALPH_STATE_FILE')); print(d.get('max_iterations', 50))")
CURRENT=$(python3 -c "import json,sys; d=json.load(open('$RALPH_STATE_FILE')); print(d.get('iteration', 0))")
NEXT=$((CURRENT + 1))

# Check if completion promise was output
if grep -q "$COMPLETION" /tmp/ralph_last_output.txt 2>/dev/null; then
  echo "✅ Ralph loop complete after $CURRENT iterations."
  rm -f "$RALPH_STATE_FILE" /tmp/ralph_last_output.txt
  exit 0
fi

# Check max iterations
if [ "$NEXT" -gt "$MAX_ITER" ]; then
  echo "⚠️ Ralph loop hit max iterations ($MAX_ITER). Stopping."
  rm -f "$RALPH_STATE_FILE"
  exit 0
fi

# Increment iteration counter
python3 -c "
import json
d = json.load(open('$RALPH_STATE_FILE'))
d['iteration'] = $NEXT
json.dump(d, open('$RALPH_STATE_FILE', 'w'))
"

echo "🔄 Ralph iteration $NEXT / $MAX_ITER — re-injecting prompt..."

# Re-inject prompt into Claude (block exit, return prompt as next input)
cat "$RALPH_STATE_FILE" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d['prompt'])
"
exit 2  # Exit code 2 = block exit and re-inject
