# /ralph-loop

Start a Ralph autonomous build loop. Claude will iterate on the given prompt file until the completion promise is output or max iterations is reached.

## Usage

```
/ralph-loop <prompt_file> [--max-iterations N] [--completion-promise TEXT]
```

## What it does

1. Loads the prompt from the specified markdown file
2. Saves loop state to `/tmp/ralph_loop_state.json`
3. Executes the prompt
4. The Stop hook intercepts exit and re-injects the prompt
5. Repeats until completion promise is found in output or max iterations hit

## Arguments

- `prompt_file` — path to a `.md` file containing the full task prompt
- `--max-iterations` — safety limit (default: 50)
- `--completion-promise` — exact string that signals task completion

## Example

```
/ralph-loop .claude/prompts/phase2.md --max-iterations 30 --completion-promise "PHASE_2_COMPLETE"
```
