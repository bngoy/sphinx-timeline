# sphinx-timeline

A Sphinx extension for building changelog-style timelines inspired by [Dagger's changelog](https://dagger.io/changelog).

## Features

- Two directives: `timeline` (a version section) and `timeline-item` (a card)
- Two statuses: `released` (white card, solid border, green dot) and `development` (yellow card, dashed border, amber dot)
- Optional tag pills per item
- CSS-only — no JavaScript
- Theme-compatible via CSS custom properties (`--tl-*`), with automatic fallback to [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io) (`--pst-*`) variables
- Built-in light and dark mode support

## Installation

```bash
pip install sphinx-timeline
```

## Quick start

Add the extension to your `conf.py`:

```python
extensions = ["sphinx_timeline"]
```

Then use the directives in any `.rst` file:

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

   .. timeline-item::

      **Stability fixes**

      Running inside a container with a mounted git worktree no longer crashes.
```

## Directives

### `.. timeline::`

Creates a timeline section with a sidebar label and a vertical dot marker.

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `:status:` | `released`, `development` | `released` | Controls the card style and dot color |
| `:version:` | any string | — | Version label shown in the sidebar (e.g. `v1.2.0`) |
| `:date:` | any string | — | Date shown below the version (e.g. `Mar 19, 2026`) |

When `:status: development` is set, the sidebar shows **"In development"** regardless of `:version:` and `:date:`.

### `.. timeline-item::`

Creates a card inside a `timeline` section. Accepts any RST content.

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `:tags:` | comma-separated string | — | Renders pill badges above the card content (e.g. `:tags: cloud, performance`) |

## Customizing colors

The extension uses `--tl-*` CSS custom properties. Override them in your theme's custom CSS to match your brand:

```css
:root {
    --tl-color-released:    #22c55e;   /* green dot — released sections */
    --tl-color-development: #f59e0b;   /* amber dot — in-development sections */
    --tl-color-surface-dev: #fffbeb;   /* card background for development items */
    --tl-color-border-dev:  #fbbf24;   /* dashed border for development items */
    --tl-border-radius:     0.75rem;
    --tl-sidebar-width:     140px;
}
```

All variables fall back to `--pst-*` values when [pydata-sphinx-theme](https://pydata-sphinx-theme.readthedocs.io) or [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io) is active.

### Full variable reference

| Variable | Fallback | Description |
|----------|----------|-------------|
| `--tl-color-released` | `--pst-color-success` / `#22c55e` | Released dot color |
| `--tl-color-development` | `--pst-color-warning` / `#f59e0b` | Development dot color |
| `--tl-color-text` | `--pst-color-text-base` / `#1a1a1a` | Primary text |
| `--tl-color-text-muted` | `--pst-color-text-muted` / `#6b7280` | Date and muted text |
| `--tl-color-border` | `--pst-color-border` / `#e5e7eb` | Card and line borders |
| `--tl-color-surface` | `--pst-color-surface` / `#ffffff` | Released card background |
| `--tl-color-surface-dev` | — / `#fffbeb` | Development card background |
| `--tl-color-border-dev` | — / `#fbbf24` | Development card dashed border |
| `--tl-color-tag-bg` | `--pst-color-on-background` / `#f3f4f6` | Tag pill background |
| `--tl-color-tag-text` | `--pst-color-text-base` / `#374151` | Tag pill text |
| `--tl-color-tag-border` | `--pst-color-border` / `#d1d5db` | Tag pill border |
| `--tl-border-radius` | — / `0.75rem` | Card corner radius |
| `--tl-sidebar-width` | — / `140px` | Width of the sidebar column |

## Development

**Prerequisites:** Python 3.9+, [Pipenv](https://pipenv.pypa.io)

```bash
git clone https://github.com/bngoy/sphinx-timeline.git
cd sphinx-timeline

# Install all dependencies (extension + dev tools + test themes)
pipenv install --dev

# Run tests
pipenv run python -m pytest tests/ -v

# Build the example docs
pipenv run sphinx-build -b html docs docs/_build/html
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
