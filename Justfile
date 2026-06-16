set dotenv-load
pkg_folder := "tenable"
repo := "https://github.com/tenable/pyTenable"
snyk_org := "pytenable"
snyk_args := "--org='" + snyk_org + "' --remote-repo-url='" + repo + "'"
name := "pyTenable"


[parallel]
test-parallel: (test-py "3.14") (test-py "3.12") (test-py "3.13") (test-py "3.14")

test: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") 

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
    # urllib3 1.x issues relating to the requirement
    # to install <2 for the development pipeline as
    # it relies on pytest-vcr and a lot of old VCR
    # recordings that break in newer versions. These
    # should be removed once the VCR requirement is
    # no longer necessary.
    uv audit -U --no-group test --no-group dev --no-group docs \
        --ignore GHSA-2xpw-w6gg-jr37 \
        --ignore GHSA-38jv-5279-wg99 \
        --ignore GHSA-gm62-xv2j-4w53 \
        --ignore GHSA-pq67-6m6q-mj2v \
        --ignore GHSA-qccp-gfcp-xxvc \
        --ignore PYSEC-2026-141
    uv tool run --with "bandit[toml,baseline,sarif]" bandit -c pyproject.toml -r . -ll

snyk:
    snyk monitor {{ snyk_args }}
    snyk code test {{ snyk_args }} --severity-threshold=high --project-name="Code Analysis" --report {{ pkg_folder }}

publish:
    uv build
    uv publish
    rm -rf dist/
