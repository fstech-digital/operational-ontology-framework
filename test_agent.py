"""Tests for agent.py — pure functions only (no LLM calls)."""

import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from agent import (
    atomic_write,
    consolidate_facts,
    estimate_context_chars,
    find_open_tasks,
    latest_handoff,
    load_env,
    mark_task_done,
    parse_agent_response,
    read_file,
    validate_response,
)


# ---------------------------------------------------------------------------
# parse_agent_response
# ---------------------------------------------------------------------------

class TestParseAgentResponse:
    def test_flat_json(self):
        output = '{"result": "did X", "decision": "chose Y", "learned": "Z matters"}'
        parsed = parse_agent_response(output)
        assert parsed["result"] == "did X"
        assert parsed["decision"] == "chose Y"
        assert parsed["learned"] == "Z matters"

    def test_nested_json(self):
        """The old regex-based parser failed on nested objects."""
        output = '{"result": "did X", "details": {"count": 5}, "decision": "Y", "learned": "Z"}'
        parsed = parse_agent_response(output)
        assert parsed["result"] == "did X"
        assert parsed["details"] == {"count": 5}
        assert parsed["learned"] == "Z"

    def test_json_with_surrounding_text(self):
        output = 'Here is my response:\n{"result": "done", "decision": "A", "learned": "B"}\nEnd.'
        parsed = parse_agent_response(output)
        assert parsed["result"] == "done"

    def test_deeply_nested_json(self):
        output = '{"result": "ok", "meta": {"a": {"b": 1}}, "decision": "X", "learned": "Y"}'
        parsed = parse_agent_response(output)
        assert parsed["result"] == "ok"
        assert parsed["meta"]["a"]["b"] == 1

    def test_fallback_line_parsing(self):
        output = "Result: completed the migration\nDecision: used batch mode\nLearned: batch is 3x faster"
        parsed = parse_agent_response(output)
        assert "migration" in parsed["result"]
        assert "batch" in parsed["decision"]
        assert "faster" in parsed["learned"]

    def test_fallback_defaults(self):
        output = "Some unstructured text without any markers"
        parsed = parse_agent_response(output)
        assert parsed["result"] == output[:200]
        assert parsed["learned"] == "Task completed successfully"

    def test_empty_input(self):
        parsed = parse_agent_response("")
        assert parsed["learned"] == "Task completed successfully"

    def test_json_with_code_block(self):
        output = '```json\n{"result": "done", "decision": "A", "learned": "B"}\n```'
        parsed = parse_agent_response(output)
        assert parsed["result"] == "done"


# ---------------------------------------------------------------------------
# find_open_tasks
# ---------------------------------------------------------------------------

class TestFindOpenTasks:
    def test_finds_open_tasks(self):
        spec = "## Tasks\n- [x] Done task\n- [ ] Open task 1\n- [ ] Open task 2\n"
        tasks = find_open_tasks(spec)
        assert len(tasks) == 2
        assert tasks[0] == "- [ ] Open task 1"
        assert tasks[1] == "- [ ] Open task 2"

    def test_no_open_tasks(self):
        spec = "## Tasks\n- [x] Done 1\n- [x] Done 2\n"
        assert find_open_tasks(spec) == []

    def test_empty_spec(self):
        assert find_open_tasks("") == []

    def test_indented_tasks(self):
        spec = "  - [ ] Indented task\n    - [ ] Deeply indented"
        tasks = find_open_tasks(spec)
        assert len(tasks) == 2

    def test_ignores_non_checkbox_lines(self):
        spec = "- Regular bullet\n- [ ] Real task\n- [?] Weird syntax\n"
        tasks = find_open_tasks(spec)
        assert len(tasks) == 1

    def test_excludes_blocked_section(self):
        spec = (
            "## Tasks\n"
            "- [ ] Active task\n"
            "## Blocked\n"
            "- [ ] Blocked task — waiting on external\n"
            "## Notes\n"
        )
        tasks = find_open_tasks(spec)
        assert len(tasks) == 1
        assert tasks[0] == "- [ ] Active task"

    def test_resumes_after_blocked_section(self):
        spec = (
            "## Tasks\n"
            "- [ ] Task A\n"
            "## Blocked\n"
            "- [ ] Blocked task\n"
            "## Other Section\n"
            "- [ ] Task B\n"
        )
        tasks = find_open_tasks(spec)
        assert len(tasks) == 2
        assert "Task A" in tasks[0]
        assert "Task B" in tasks[1]


# ---------------------------------------------------------------------------
# mark_task_done
# ---------------------------------------------------------------------------

class TestMarkTaskDone:
    def test_marks_single_task(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("- [ ] Task A\n- [ ] Task B\n")
            f.flush()
            mark_task_done(f.name, "- [ ] Task A", "A was easy")
            content = Path(f.name).read_text()
            os.unlink(f.name)

        assert "- [x] Task A" in content
        assert "Learned: A was easy" in content
        assert "- [ ] Task B" in content  # B untouched

    def test_only_marks_first_occurrence(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("- [ ] Duplicate\n- [ ] Duplicate\n")
            f.flush()
            mark_task_done(f.name, "- [ ] Duplicate", "first one")
            content = Path(f.name).read_text()
            os.unlink(f.name)

        assert content.count("- [x]") == 1
        assert content.count("- [ ]") == 1

    def test_truncates_long_learned(self):
        long_text = "a" * 100 + "b" * 100 + "c" * 100  # 300 chars, distinct segments
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("- [ ] Task\n")
            f.flush()
            mark_task_done(f.name, "- [ ] Task", long_text)
            content = Path(f.name).read_text()
            os.unlink(f.name)

        learned_line = [l for l in content.splitlines() if "Learned:" in l][0]
        learned_value = learned_line.split("Learned: ", 1)[1]
        # Must be exactly 200 chars (first 200 of the 300-char input)
        assert len(learned_value) == 200
        assert learned_value == "a" * 100 + "b" * 100  # third segment (c*100) truncated


# ---------------------------------------------------------------------------
# latest_handoff
# ---------------------------------------------------------------------------

class TestLatestHandoff:
    def test_returns_latest_file(self):
        with tempfile.TemporaryDirectory() as d:
            hdir = Path(d) / "handoffs"
            hdir.mkdir()
            (hdir / "2026-01-01-0800.md").write_text("old handoff")
            (hdir / "2026-04-12-1500.md").write_text("latest handoff")
            result = latest_handoff(d)

        assert result == "latest handoff"

    def test_no_handoffs(self):
        with tempfile.TemporaryDirectory() as d:
            result = latest_handoff(d)
        assert result == "(no previous handoff)"

    def test_empty_handoffs_dir(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "handoffs").mkdir()
            result = latest_handoff(d)
        assert result == "(no previous handoff)"


# ---------------------------------------------------------------------------
# read_file
# ---------------------------------------------------------------------------

class TestReadFile:
    def test_reads_existing_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("hello")
            f.flush()
            assert read_file(f.name) == "hello"
            os.unlink(f.name)

    def test_missing_file_returns_empty(self):
        assert read_file("/tmp/nonexistent_oof_test_file.md") == ""


# ---------------------------------------------------------------------------
# estimate_context_chars
# ---------------------------------------------------------------------------

class TestEstimateContextChars:
    def test_basic_estimate(self):
        result = estimate_context_chars("pin" * 100, "facts" * 50, "handoff" * 30, ["a", "bb"])
        assert result == 500 + 300 + 250 + 210 + 3  # base + pin + facts + handoff + learnings

    def test_empty_learnings(self):
        result = estimate_context_chars("p", "", "", [])
        assert result == 500 + 1

    def test_none_learnings(self):
        result = estimate_context_chars("p", "", "", None)
        assert result == 500 + 1


# ---------------------------------------------------------------------------
# consolidate_facts
# ---------------------------------------------------------------------------

class TestConsolidateFacts:
    def test_promotes_learnings_to_facts(self):
        with tempfile.TemporaryDirectory() as d:
            facts_path = Path(d) / "_facts.md"
            facts_path.write_text("# Facts\n\n## Confirmed Patterns\n\n- existing fact\n")

            records = [
                {"learned": "API rate limit is 100/min"},
                {"learned": "Task completed successfully"},  # should be skipped
            ]
            consolidate_facts(d, records)

            content = facts_path.read_text()
            assert "API rate limit is 100/min" in content
            assert content.count("Task completed successfully") == 0  # filtered out
            assert "existing fact" in content  # preserved

    def test_creates_facts_file_if_missing(self):
        with tempfile.TemporaryDirectory() as d:
            records = [{"learned": "new discovery"}]
            consolidate_facts(d, records)

            content = (Path(d) / "_facts.md").read_text()
            assert "new discovery" in content
            assert "## Confirmed Patterns" in content

    def test_skips_when_no_learnings(self):
        with tempfile.TemporaryDirectory() as d:
            records = [{"learned": "Task completed successfully"}]
            consolidate_facts(d, records)
            assert not (Path(d) / "_facts.md").exists()

    def test_flags_stale_facts(self):
        with tempfile.TemporaryDirectory() as d:
            old_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
            facts_path = Path(d) / "_facts.md"
            facts_path.write_text(
                f"# Facts\n\n## Confirmed Patterns\n\n"
                f"- old fact (source: test, {old_date}, confidence: observed)\n"
            )

            records = [{"learned": "fresh insight"}]
            consolidate_facts(d, records)

            content = facts_path.read_text()
            assert "stale" in content
            assert "fresh insight" in content

    def test_does_not_double_flag_stale_consolidate(self):
        with tempfile.TemporaryDirectory() as d:
            old_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
            facts_path = Path(d) / "_facts.md"
            facts_path.write_text(
                f"# Facts\n\n## Confirmed Patterns\n\n"
                f"- already flagged (source: test, {old_date}, confidence: observed) ⚠️ stale — re-verify or remove\n"
            )

            records = [{"learned": "new stuff"}]
            consolidate_facts(d, records)

            content = facts_path.read_text()
            assert content.count("⚠️ stale") == 1  # not doubled


# ---------------------------------------------------------------------------
# atomic_write
# ---------------------------------------------------------------------------

class TestAtomicWrite:
    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.md")
            atomic_write(path, "hello world")
            assert Path(path).read_text() == "hello world"

    def test_overwrites_existing(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.md")
            Path(path).write_text("old")
            atomic_write(path, "new")
            assert Path(path).read_text() == "new"

    def test_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "sub", "dir", "test.md")
            atomic_write(path, "nested")
            assert Path(path).read_text() == "nested"

    def test_no_temp_files_left(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.md")
            atomic_write(path, "content")
            files = os.listdir(d)
            assert files == ["test.md"]  # no .tmp leftovers


# ---------------------------------------------------------------------------
# validate_response
# ---------------------------------------------------------------------------

class TestValidateResponse:
    def test_passes_valid_response(self):
        r = validate_response({"result": "did X", "decision": "chose Y", "learned": "Z"})
        assert r["result"] == "did X"
        assert r["decision"] == "chose Y"
        assert r["learned"] == "Z"

    def test_fills_missing_result(self):
        r = validate_response({})
        assert r["result"] == "(no result)"
        assert r["learned"] == "Task completed successfully"

    def test_truncates_long_fields(self):
        r = validate_response({"result": "x" * 3000, "learned": "y" * 300})
        assert len(r["result"]) == 2000
        assert len(r["learned"]) == 200

    def test_preserves_extra_fields(self):
        r = validate_response({"result": "ok", "learned": "L", "details": {"count": 5}})
        assert r["details"] == {"count": 5}

    def test_empty_strings_get_defaults(self):
        r = validate_response({"result": "", "learned": ""})
        assert r["result"] == "(no result)"
        assert r["learned"] == "Task completed successfully"


# ---------------------------------------------------------------------------
# mark_task_done — edge cases
# ---------------------------------------------------------------------------

class TestMarkTaskDoneEdgeCases:
    def test_task_not_found_is_noop(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("- [ ] Other task\n")
            f.flush()
            mark_task_done(f.name, "- [ ] Nonexistent task", "learned something")
            content = Path(f.name).read_text()
            os.unlink(f.name)
        assert "- [x]" not in content
        assert "- [ ] Other task" in content


# ---------------------------------------------------------------------------
# load_env — quote stripping
# ---------------------------------------------------------------------------

class TestLoadEnv:
    def test_strips_double_quotes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write('TEST_KEY_DQ="my-value"\n')
            f.flush()
            old_cwd = os.getcwd()
            os.chdir(os.path.dirname(f.name))
            os.rename(f.name, os.path.join(os.path.dirname(f.name), ".env"))
            env_path = os.path.join(os.path.dirname(f.name), ".env")
            try:
                os.environ.pop("TEST_KEY_DQ", None)
                load_env()
                assert os.environ.get("TEST_KEY_DQ") == "my-value"
            finally:
                os.chdir(old_cwd)
                os.unlink(env_path)
                os.environ.pop("TEST_KEY_DQ", None)

    def test_strips_single_quotes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("TEST_KEY_SQ='my-value'\n")
            f.flush()
            old_cwd = os.getcwd()
            os.chdir(os.path.dirname(f.name))
            os.rename(f.name, os.path.join(os.path.dirname(f.name), ".env"))
            env_path = os.path.join(os.path.dirname(f.name), ".env")
            try:
                os.environ.pop("TEST_KEY_SQ", None)
                load_env()
                assert os.environ.get("TEST_KEY_SQ") == "my-value"
            finally:
                os.chdir(old_cwd)
                os.unlink(env_path)
                os.environ.pop("TEST_KEY_SQ", None)

    def test_preserves_unquoted_values(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write("TEST_KEY_UQ=plain-value\n")
            f.flush()
            old_cwd = os.getcwd()
            os.chdir(os.path.dirname(f.name))
            os.rename(f.name, os.path.join(os.path.dirname(f.name), ".env"))
            env_path = os.path.join(os.path.dirname(f.name), ".env")
            try:
                os.environ.pop("TEST_KEY_UQ", None)
                load_env()
                assert os.environ.get("TEST_KEY_UQ") == "plain-value"
            finally:
                os.chdir(old_cwd)
                os.unlink(env_path)
                os.environ.pop("TEST_KEY_UQ", None)
