# Contributing to Operational Ontology Framework

Thanks for your interest. Here's how to contribute effectively.

## Getting Started

```bash
git clone https://github.com/fstech-digital/operational-ontology-framework.git
cd operational-ontology-framework
pip install -r requirements.txt
python -m pytest test_agent.py -v  # All tests should pass
```

## What We're Looking For

- **Bug fixes** with a test that reproduces the issue
- **New adapters** in `adapters.py` (Google, local models, etc.)
- **Improved templates** with better guidance
- **Documentation** improvements, especially real-world usage examples
- **Empirical data** from running the framework in production (boot failure rate, handoff recovery time)

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Add tests for any new functionality
3. Ensure all tests pass: `python -m pytest test_agent.py -v`
4. Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
5. Keep PRs focused. One concern per PR.

## Code Style

- Python 3.9+ compatible
- No external dependencies beyond what's in `requirements.txt` (the core framework is filesystem + git)
- Functions that don't need an LLM should be testable without one
- Prefer clarity over cleverness

## Reporting Issues

When reporting a bug, include:
- Python version and OS
- The command you ran
- Expected vs actual behavior
- Relevant contents of your `_pin.md` / `_spec.md` if applicable

For feature requests, describe the problem you're solving before proposing a solution.

## License

By contributing, you agree that your contributions will be licensed under [CC BY 4.0](LICENSE).
