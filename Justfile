set dotenv-load
pkg_folder := "tenable"
repo := "https://github.com/tenable/pyTenable"
snyk_org := "pytenable"
snyk_args := "--org='" + snyk_org + "' --remote-repo-url='" + repo + "'"
name := "pyTenable"


[parallel]
test-parallel: (test-py "3.14") (test-py "3.12") (test-py "3.13") (test-py "3.14")

test: (test-py "3.12") (test-py "3.13") (test-py "3.14") 

docs:
    sphinx-build -M clean docs docs/_build
    sphinx-build -M html docs docs/_build

test-py version: (lint version) (unit-tests version) audit

lint version:
    #uv run --python {{version}} --isolated --group dev mypy {{pkg_folder}}
    #uv run --python {{version}} --isolated --group dev ty check {{pkg_folder}}
    uv run                     \
        --python {{ version }} \
        --isolated             \
        --group dev            \
        ruff check {{ pkg_folder }}

unit-tests version:
    uv run                     \
        --python {{ version }} \
        --isolated             \
        --group dev            \
        pytest -q --cov-fail-under 80

partial-tests path:
    uv run                           \
        --isolated                   \
        --group dev                  \
        pytest tests/{{ path }}      \
            -q -vv                   \
            --cov-fail-under 95      \
            --cov=tenable/{{ path }} \
            --cov-report term-missing:skip-covered

audit:
    uv audit -U --no-group test --no-group dev --no-group docs
    uv tool run --with "bandit[toml,baseline,sarif]" bandit -c pyproject.toml -r . -ll

snyk:
    snyk monitor {{ snyk_args }}
    snyk code test {{ snyk_args }} --severity-threshold=high --project-name="Code Analysis" --report {{ pkg_folder }}

publish:
    uv build
    uv publish
    rm -rf dist/
