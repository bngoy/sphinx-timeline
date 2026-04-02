# sphinx-timeline

A Sphinx extension for building changelog-style timelines inspired by [Dagger's changelog](https://dagger.io/changelog).

[![CI](https://github.com/bngoy/sphinx-timeline/actions/workflows/ci.yml/badge.svg)](https://github.com/bngoy/sphinx-timeline/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/sphinx-timeline)](https://pypi.org/project/sphinx-timeline/)
[![Python](https://img.shields.io/pypi/pyversions/sphinx-timeline)](https://pypi.org/project/sphinx-timeline/)
[![License](https://img.shields.io/pypi/l/sphinx-timeline)](LICENSE)

## Features

- `timeline` directive — a version section with sidebar label and status dot
- `timeline-item` directive — a card with optional tag pills
- Two statuses: **released** (white card, solid border, green pulsing dot) and **development** (yellow card, dashed border, amber pulsing dot)
- CSS-only — no JavaScript required
- Theme-compatible via CSS custom properties (`--tl-*`), with automatic fallback to [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io) (`--pst-*`) variables
- Built-in light and dark mode support
- `prefers-reduced-motion` aware — animation respects accessibility settings

## Installation

```bash
pip install sphinx-timeline
```

## Quick start

**1.** Add the extension to your `conf.py`:

```python
extensions = ["sphinx_timeline"]
```

**2.** Use the directives in any `.rst` file:

```rst
.. timeline::
   :status: development

   .. timeline-item::
      :tags: performance

      **Project Theseus**

      The largest engine change since the project began.

.. timeline::
   :version: v1.2.0
   :date: Mar 19, 2026
   :status: released

   .. timeline-item::
      :tags: feature, cloud

      **Cloud Engines**

      Fully managed engines with auto-scaling and distributed caching.
      Run ``dagger --cloud`` and your pipelines execute in the cloud.

   .. timeline-item::

      **Stability fixes**

      Running inside a container with a mounted git worktree no longer crashes.
```

**3.** Build:

```bash
sphinx-build docs public
```

## Directive reference

### `.. timeline::` — version section

Creates a timeline entry with a sidebar label and a coloured pulsing dot.

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `:status:` | `released` \| `development` | `released` | Card style and dot colour |
| `:version:` | string | — | Version label in the sidebar (e.g. `v1.2.0`) |
| `:date:` | string | — | Date below the version (e.g. `Mar 19, 2026`) |

> When `:status: development` is used, the sidebar shows **"In development"** regardless of `:version:` and `:date:`.

### `.. timeline-item::` — card

Creates a card inside a `timeline` section. Accepts any RST content (paragraphs, code blocks, lists, links, etc.).

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `:tags:` | comma-separated string | — | Renders pill badges above the content (e.g. `:tags: cloud, performance`) |

## Customizing colours

Override `--tl-*` CSS variables in your theme's custom stylesheet:

```css
:root {
    --tl-color-released:    #22c55e;   /* green dot — released sections     */
    --tl-color-development: #f59e0b;   /* amber dot — development sections  */
    --tl-color-surface-dev: #fffbeb;   /* card background — development     */
    --tl-color-border-dev:  #fbbf24;   /* dashed border — development       */
    --tl-border-radius:     0.75rem;   /* card corner radius                */
    --tl-sidebar-width:     140px;     /* sidebar column width              */
}
```

Apply in `conf.py`:

```python
html_static_path = ["_static"]
html_css_files   = ["custom.css"]
```

### Full CSS variable reference

| Variable | Fallback chain | Description |
|----------|---------------|-------------|
| `--tl-color-released` | `--pst-color-success` → `#22c55e` | Released status dot |
| `--tl-color-development` | `--pst-color-warning` → `#f59e0b` | Development status dot |
| `--tl-color-text` | `--pst-color-text-base` → `#1a1a1a` | Primary text |
| `--tl-color-text-muted` | `--pst-color-text-muted` → `#6b7280` | Date / muted text |
| `--tl-color-border` | `--pst-color-border` → `#e5e7eb` | Card and line borders |
| `--tl-color-surface` | `--pst-color-surface` → `#ffffff` | Released card background |
| `--tl-color-surface-dev` | `#fffbeb` | Development card background |
| `--tl-color-border-dev` | `#fbbf24` | Development dashed border |
| `--tl-color-tag-bg` | `--pst-color-on-background` → `#f3f4f6` | Tag pill background |
| `--tl-color-tag-text` | `--pst-color-text-base` → `#374151` | Tag pill text |
| `--tl-color-tag-border` | `--pst-color-border` → `#d1d5db` | Tag pill border |
| `--tl-border-radius` | `0.75rem` | Card corner radius |
| `--tl-sidebar-width` | `140px` | Sidebar column width |
| `--tl-dot-size` | `12px` | Status dot diameter |

## Project structure

```
sphinx-timeline/
├── src/
│   └── sphinx_timeline/
│       ├── __init__.py       # Extension setup()
│       ├── directives.py     # TimelineDirective, TimelineItemDirective
│       ├── nodes.py          # Docutils nodes + HTML/LaTeX visitors
│       └── _static/
│           └── timeline.css  # All styles (variables, layout, animation)
├── docs/                     # Example Sphinx project
├── tests/                    # Pytest test suite
├── .github/workflows/        # CI, auto-tag, and PyPI release
├── VERSION                   # Single source of truth for the version
└── pyproject.toml
```

## Development setup

**Prerequisites:** Python ≥ 3.9, [Pipenv](https://pipenv.pypa.io) or [uv](https://docs.astral.sh/uv/).

### With Pipenv

```bash
git clone https://github.com/bngoy/sphinx-timeline.git
cd sphinx-timeline
pipenv install --dev
pipenv run python -m pytest tests/ -v
pipenv run sphinx-build docs public
```

### With uv

```bash
git clone https://github.com/bngoy/sphinx-timeline.git
cd sphinx-timeline
uv sync --extra dev
uv run pytest tests/ -v
uv run sphinx-build docs public
```

### Linting

```bash
# Check
pipenv run ruff check src tests

# Fix automatically
pipenv run ruff check src tests --fix
pipenv run ruff format src tests
```

## Releasing a new version

1. Update `VERSION` with the new version number
2. Open a pull request — merging it will automatically tag the repository
3. The tag push triggers the PyPI release workflow

## License

Apache 2.0 — see [LICENSE](LICENSE).
