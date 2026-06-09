pkg_folder := "tenable"
repo := "https://github.com/tenable/pyTenable"
snyk_org := "pytenable"
snyk_args := "--org='" + snyk_org + "' --remote-repo-url='" + repo + "'"
name := "pyTenable"


[parallel]
test-parallel: (test-py "3.12") (test-py "3.13") (test-py "3.14")

test: (test-py "3.12") (test-py "3.13") (test-py "3.14") 

docs:
    sphinx-build -M clean docs docs/_build
    sphinx-build -M html docs docs/_build

test-py version: (lint version) (unit-tests version) audit

lint version:
    #uv run --python {{version}} --isolated --group dev mypy {{pkg_folder}}
    #uv run --python {{version}} --isolated --group dev ty check {{pkg_folder}}
    uv run --python {{ version }} --isolated --group dev ruff check {{ pkg_folder }}

unit-tests version:
    uv run --python {{ version }} --isolated --group dev pytest -q --cov-fail-under 80

audit:
    # urllib3 1.x issues relating to the requirement
    # to install <2 for the development pipeline as
    # it relies on pytest-vcr and a lot of old VCR
    # recordings that break in newer versions. These
    # should be removed once the VCR requirement is
    # no longer necessary.
    uv audit -U --no-group test --no-group dev --no-group docs
    uv tool run --with "bandit[toml,baseline,sarif]" bandit -c pyproject.toml -r . -ll

snyk:
    snyk monitor {{ snyk_args }}
    snyk code test {{ snyk_args }} --severity-threshold=high --project-name="Code Analysis" --report {{ pkg_folder }}
