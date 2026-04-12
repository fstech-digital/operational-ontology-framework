#!/usr/bin/env python3
"""
Minimal Operational Ontology Agent
===================================
Demonstrates the Pin/Spec/Handoff cycle in ~100 lines.

Usage:
    python agent.py examples/customer-support

The agent will:
1. Boot  — Load Pin (rules) + Spec (tasks) + latest Handoff
2. Execute — Pick the first open task and work on it via LLM
3. Write-back — Mark task done in Spec, record learning
4. Handoff — Generate structured handoff for next session

Requires: ANTHROPIC_API_KEY in environment or .env file
"""

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


def find_first_open_task(spec: str):
    for line in spec.splitlines():
        if re.match(r"\s*- \[ \]", line):
            return line.strip()
    return None


def mark_task_done(spec_path: str, task_line: str, result: str):
    spec = Path(spec_path).read_text()
    done_line = task_line.replace("- [ ]", "- [x]")
    done_line += f"\n  - Learned: {result[:200]}"
    # Replace only the first occurrence to avoid duplicates
    spec = spec.replace(task_line, done_line, 1)
    Path(spec_path).write_text(spec)


def generate_handoff(project_dir: str, focus: str, decisions: str, results: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    date_slug = datetime.now().strftime("%Y-%m-%d-%H%M")
    handoff_dir = Path(project_dir) / "handoffs"
    handoff_dir.mkdir(exist_ok=True)

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


def run_cycle(project_dir: str):
    # --- BOOT ---
    print("\n=== BOOT ===")
    pin = read_file(os.path.join(project_dir, "_pin.md"))
    spec = read_file(os.path.join(project_dir, "_spec.md"))
    handoff = latest_handoff(project_dir)

    if not pin:
        print(f"  ERROR: No _pin.md found in {project_dir}")
        sys.exit(1)
    if not spec:
        print(f"  ERROR: No _spec.md found in {project_dir}")
        sys.exit(1)

    print(f"  Pin loaded: {len(pin)} chars")
    print(f"  Spec loaded: {len(spec)} chars")
    print(f"  Handoff loaded: {len(handoff)} chars")

    # --- EXECUTE ---
    print("\n=== EXECUTE ===")
    task = find_first_open_task(spec)
    if not task:
        print("  No open tasks. Cycle complete.")
        return

    print(f"  Task: {task[:80]}...")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ERROR: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"""You are an agent operating under the Operational Ontology Framework.

Your Pin (immutable rules):
{pin}

Previous handoff (context from last session):
{handoff}

Execute the task given to you. Be specific and actionable.
After completing, provide:
1. RESULT: What you did (1-2 sentences)
2. DECISION: Key decision made and why (1 sentence)
3. LEARNED: What future tasks should know (1 sentence)""",
        messages=[{"role": "user", "content": f"Execute this task:\n{task}"}],
    )

    output = response.content[0].text
    print(f"  Agent response:\n{output[:500]}")

    # --- WRITE-BACK ---
    print("\n=== WRITE-BACK ===")
    learned = ""
    for line in output.splitlines():
        if line.upper().startswith("LEARNED:") or line.upper().startswith("3."):
            learned = line.split(":", 1)[-1].strip() if ":" in line else line
            break
    if not learned:
        learned = "Task completed successfully"

    spec_path = os.path.join(project_dir, "_spec.md")
    mark_task_done(spec_path, task, learned)
    print(f"  Task marked done in _spec.md")

    # --- HANDOFF ---
    print("\n=== HANDOFF ===")
    focus = task[6:60] + "..."  # strip "- [ ] " prefix
    decisions = ""
    for line in output.splitlines():
        if line.upper().startswith("DECISION:") or line.upper().startswith("2."):
            decisions = line
            break
    results = f"- {task[:60]}: completed"

    generate_handoff(project_dir, focus, decisions or "See agent output", results)
    print("\n=== CYCLE COMPLETE ===\n")


if __name__ == "__main__":
    load_env()

    if len(sys.argv) < 2:
        print("Usage: python agent.py <project-directory>")
        print("Example: python agent.py examples/customer-support")
        sys.exit(1)

    project_dir = sys.argv[1]
    if not Path(project_dir).is_dir():
        print(f"Directory not found: {project_dir}")
        sys.exit(1)

    run_cycle(project_dir)
