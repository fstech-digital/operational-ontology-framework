#!/usr/bin/env python3
"""
Operational Ontology Agent — Reference Implementation
======================================================
Demonstrates the Pin/Spec/Handoff cycle.

Usage:
    python agent.py examples/customer-support
    python agent.py examples/customer-support --all
    python agent.py examples/customer-support --model claude-haiku-4-5-20251001

The agent will:
1. Boot     — Load Pin (rules) + Spec (tasks) + latest Handoff
2. Execute  — Pick open task(s) and work on them via LLM
3. Write-back — Mark task done in Spec, record learning
4. Handoff  — Generate structured handoff for next session

Options:
    --all       Execute all open tasks in sequence (default: one task)
    --model     Override model (default: MODEL env var or claude-sonnet-4-6)
    --dry-run   Boot and show tasks without calling the LLM

Requires: ANTHROPIC_API_KEY in environment or .env file
"""

import argparse
import json
import os
import re
import sys
import glob
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("Install anthropic SDK: pip install anthropic")
    sys.exit(1)

DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096


def load_env():
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())


def read_file(path: str) -> str:
    p = Path(path)
    return p.read_text() if p.exists() else ""


def latest_handoff(project_dir: str) -> str:
    pattern = os.path.join(project_dir, "handoffs", "*.md")
    files = sorted(glob.glob(pattern))
    return read_file(files[-1]) if files else "(no previous handoff)"


def find_open_tasks(spec: str) -> list:
    tasks = []
    for line in spec.splitlines():
        if re.match(r"\s*- \[ \]", line):
            tasks.append(line.strip())
    return tasks


def mark_task_done(spec_path: str, task_line: str, learned: str):
    spec = Path(spec_path).read_text()
    done_line = task_line.replace("- [ ]", "- [x]")
    done_line += f"\n  - Learned: {learned[:200]}"
    spec = spec.replace(task_line, done_line, 1)
    Path(spec_path).write_text(spec)


def parse_agent_response(output: str) -> dict:
    """Parse structured JSON from agent response, with fallback to text parsing."""
    # Try JSON first (preferred)
    json_match = re.search(r"\{[^{}]*\"result\"[^{}]*\}", output, re.DOTALL | re.IGNORECASE)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: line-by-line parsing
    parsed = {"result": "", "decision": "", "learned": ""}
    for line in output.splitlines():
        lower = line.lower().strip()
        if lower.startswith("result:") or lower.startswith('"result"'):
            parsed["result"] = line.split(":", 1)[-1].strip().strip('"').strip(",")
        elif lower.startswith("decision:") or lower.startswith('"decision"'):
            parsed["decision"] = line.split(":", 1)[-1].strip().strip('"').strip(",")
        elif lower.startswith("learned:") or lower.startswith('"learned"'):
            parsed["learned"] = line.split(":", 1)[-1].strip().strip('"').strip(",")

    if not parsed["learned"]:
        parsed["learned"] = "Task completed successfully"
    if not parsed["result"]:
        parsed["result"] = output[:200]

    return parsed


def generate_handoff(project_dir: str, focus: str, task_records: list):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_slug = datetime.now().strftime("%Y-%m-%d-%H%M")
    handoff_dir = Path(project_dir) / "handoffs"
    handoff_dir.mkdir(exist_ok=True)

    decisions = "\n".join(
        f"- {r['decision']}" for r in task_records if r.get("decision")
    ) or "- See agent output"

    results = "\n".join(
        f"- {r['task'][:80]}: {r['result'][:500]}" for r in task_records
    )

    content = f"""# Handoff — {now}

## Focus
{focus}

## Decisions (with reasoning)
{decisions}

## Tasks Executed
{results}

## Continuation
Next session should pick up the next open task in _spec.md.
"""
    path = handoff_dir / f"{date_slug}.md"
    path.write_text(content)
    print(f"  Handoff saved: {path}")


def execute_task(client, model: str, pin: str, facts: str, handoff: str, task: str, session_learnings: list = None) -> dict:
    """Execute a single task via LLM and return structured result."""
    facts_section = f"\nAccumulated facts (long-term memory):\n{facts}" if facts else ""
    learnings_section = ""
    if session_learnings:
        learnings_text = "\n".join(f"- {l}" for l in session_learnings)
        learnings_section = f"\nLearned earlier this session:\n{learnings_text}"
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=f"""You are an agent operating under the Operational Ontology Framework.

Your Pin (immutable rules):
{pin}
{facts_section}
{learnings_section}

Previous handoff (context from last session):
{handoff}

Execute the task given to you. Be specific and actionable.
Respond in JSON format:
{{
  "result": "What you did (1-2 sentences)",
  "decision": "Key decision made and why (1 sentence)",
  "learned": "What future tasks should know (1 sentence)"
}}""",
        messages=[{"role": "user", "content": f"Execute this task:\n{task}"}],
    )

    output = response.content[0].text
    parsed = parse_agent_response(output)
    parsed["task"] = task
    parsed["raw"] = output
    return parsed


def run_cycle(project_dir: str, model: str, run_all: bool = False, dry_run: bool = False):
    # --- BOOT (with Retrieval) ---
    print("\n=== BOOT ===")
    pin = read_file(os.path.join(project_dir, "_pin.md"))
    spec = read_file(os.path.join(project_dir, "_spec.md"))
    facts = read_file(os.path.join(project_dir, "_facts.md"))
    handoff = latest_handoff(project_dir)

    if not pin:
        print(f"  ERROR: No _pin.md found in {project_dir}")
        sys.exit(1)
    if not spec:
        print(f"  ERROR: No _spec.md found in {project_dir}")
        sys.exit(1)

    print(f"  Pin loaded: {len(pin)} chars")
    print(f"  Spec loaded: {len(spec)} chars")
    print(f"  Facts loaded: {len(facts)} chars" if facts else "  Facts: (none)")
    print(f"  Handoff loaded: {len(handoff)} chars")
    print(f"  Model: {model}")

    # --- FIND TASKS ---
    open_tasks = find_open_tasks(spec)
    if not open_tasks:
        print("\n  No open tasks. Cycle complete.")
        return

    tasks_to_run = open_tasks if run_all else open_tasks[:1]
    print(f"\n  Open tasks: {len(open_tasks)}")
    print(f"  Will execute: {len(tasks_to_run)} ({'--all' if run_all else 'first only'})")

    if dry_run:
        print("\n=== DRY RUN — tasks found ===")
        for i, t in enumerate(tasks_to_run, 1):
            print(f"  [{i}] {t[:80]}")
        return

    # --- EXECUTE ---
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ERROR: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    spec_path = os.path.join(project_dir, "_spec.md")
    task_records = []
    session_learnings = []  # Within-session knowledge accumulation

    for i, task in enumerate(tasks_to_run, 1):
        print(f"\n=== EXECUTE [{i}/{len(tasks_to_run)}] ===")
        print(f"  Task: {task[:80]}...")

        result = execute_task(client, model, pin, facts, handoff, task, session_learnings)
        task_records.append(result)

        print(f"  Result: {result['result'][:200]}")
        print(f"  Learned: {result['learned'][:200]}")

        # --- WRITE-BACK ---
        mark_task_done(spec_path, task, result["learned"])
        session_learnings.append(result["learned"])
        print(f"  Task marked done in _spec.md")

        # Reload spec for next task (it was modified)
        spec = read_file(spec_path)

    # --- HANDOFF ---
    print(f"\n=== HANDOFF ({len(task_records)} tasks completed) ===")
    focus = f"{len(task_records)} tasks executed in {project_dir}"
    generate_handoff(project_dir, focus, task_records)
    print("\n=== CYCLE COMPLETE ===\n")


def main():
    load_env()

    parser = argparse.ArgumentParser(
        description="Operational Ontology Agent — Pin/Spec/Handoff cycle"
    )
    parser.add_argument("project_dir", help="Path to project directory with _pin.md and _spec.md")
    parser.add_argument("--all", action="store_true", help="Execute all open tasks (default: first only)")
    parser.add_argument("--model", default=None, help=f"Model to use (default: MODEL env or {DEFAULT_MODEL})")
    parser.add_argument("--dry-run", action="store_true", help="Show tasks without calling LLM")
    args = parser.parse_args()

    if not Path(args.project_dir).is_dir():
        print(f"Directory not found: {args.project_dir}")
        sys.exit(1)

    model = args.model or os.environ.get("MODEL", DEFAULT_MODEL)
    run_cycle(args.project_dir, model=model, run_all=args.all, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
