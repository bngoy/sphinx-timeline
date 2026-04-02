# sphinx-timeline — Claude context

## Project overview

`sphinx-timeline` is a Sphinx extension that adds two RST directives —
`timeline` and `timeline-item` — for building changelog-style timelines
similar to Dagger's changelog page. It is CSS-only, theme-agnostic, and
ships light/dark mode support out of the box.

## Tech stack

| Layer | Tool |
|-------|------|
| Language | Python ≥ 3.9 |
| Build backend | setuptools (version read from `VERSION` file) |
| Package manager (local) | Pipenv |
| Package manager (CI) | uv |
| Linter / formatter | Ruff |
| Test framework | pytest |
| Documentation builder | Sphinx (alabaster theme for examples) |

## Repository structure

```
sphinx-timeline/
├── src/sphinx_timeline/
│   ├── __init__.py       # setup() — registers nodes, directives, CSS
│   ├── directives.py     # TimelineDirective, TimelineItemDirective
│   ├── nodes.py          # timeline + timeline_item nodes; HTML + LaTeX visitors
│   └── _static/
│       └── timeline.css  # all CSS (variables, layout, animation, dark mode)
├── docs/                 # runnable Sphinx example project
│   ├── conf.py
│   ├── index.rst
│   └── changelog.rst
├── tests/
│   ├── conftest.py       # build_html pytest fixture (full Sphinx build)
│   └── test_timeline.py  # 6 tests covering classes, labels, tags, CSS
├── .github/workflows/
│   ├── ci.yml            # lint (ruff) + test matrix on push / PR
│   ├── tag.yml           # auto-tag repo from VERSION on PR merge
│   └── release.yml       # build + publish to PyPI on tag push
├── VERSION               # single source of truth for the version number
├── Pipfile / Pipfile.lock
└── pyproject.toml        # setuptools config, ruff config, pytest config
```

## Dev commands

### Setup

```bash
# Pipenv
pipenv install --dev

# uv
uv sync --extra dev
```

### Run tests

```bash
pipenv run python -m pytest tests/ -v
# or
uv run pytest tests/ -v
```

### Lint and format

```bash
# check only
ruff check src tests
ruff format --check src tests

# auto-fix
ruff check src tests --fix
ruff format src tests
```

### Build example docs

```bash
pipenv run sphinx-build docs public
# or
uv run sphinx-build docs public
```

### Build the package

```bash
uv build
# output: dist/sphinx_timeline-X.Y.Z.tar.gz + .whl
```

## Key conventions

- **BEM class naming** — all HTML classes use the `sphinx-timeline` prefix:
  `sphinx-timeline`, `sphinx-timeline__sidebar`, `sphinx-timeline__item--released`, etc.
- **CSS custom properties** — all design tokens live as `--tl-*` variables in
  `timeline.css`. They fall back to `--pst-*` (pydata-sphinx-theme) then to
  hardcoded values.
- **Docutils visitor pattern** — HTML is generated via `visit_*/depart_*`
  functions registered with `app.add_node()`. Never mutate the node tree in
  visitors.
- **No JavaScript** — the extension is intentionally CSS-only. Animation uses
  a `@keyframes` pulse on a `::after` pseudo-element.
- **Version source of truth** — the `VERSION` file is the only place the
  version number lives. `pyproject.toml` reads it via
  `[tool.setuptools.dynamic]`. `__version__` in `__init__.py` is resolved at
  runtime via `importlib.metadata`.

## Testing workflow

The `build_html` fixture in `conftest.py` performs a full Sphinx HTML build
in a `tmp_path` directory for every test. Tests assert on the raw HTML output.
This integration-style approach catches regressions at the rendering level.

To run a single test:
```bash
pytest tests/test_timeline.py::test_tags_rendered -v
```

## CI/CD summary

| Workflow | Trigger | What it does |
|----------|---------|-------------|
| `ci.yml` | push / PR | Ruff lint + test matrix (Python 3.9–3.12) |
| `tag.yml` | PR merged to master | Reads `VERSION`, creates `vX.Y.Z` git tag |
| `release.yml` | tag `v*` pushed | `uv build` + `uv publish` → PyPI |
