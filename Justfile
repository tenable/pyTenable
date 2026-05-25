pkg_folder := "tenable"


[parallel]
test-parallel: (test-py "3.14") (test-py "3.12") (test-py "3.13") (test-py "3.14")

test: (test-py "3.11") (test-py "3.12") (test-py "3.13") (test-py "3.14") 

docs:
    sphinx-build -M clean docs docs/_build
    sphinx-build -M html docs docs/_build

test-py version: (lint version) (unit-tests version) #audit

lint version:
    uv run --python {{version}} --isolated --group dev mypy {{pkg_folder}}
    uv run --python {{version}} --isolated --group dev ty check {{pkg_folder}}
    uv run --python {{version}} --isolated --group dev ruff check {{pkg_folder}}

unit-tests version:
    uv run --python {{version}} --isolated --group dev pytest -q --cov-fail-under 80

audit:
    uv audit --no-group test --no-group dev --no-group docs
