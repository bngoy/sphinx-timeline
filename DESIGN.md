# sphinx-timeline — Design document

## Problem statement

Sphinx documentation often needs to present a project's history — releases,
features in progress, and breaking changes — in a way that is both visually
rich and easily authored in RST. Existing solutions require either raw HTML
directives (hard to maintain) or external JavaScript libraries (incompatible
with Sphinx's static-file model). `sphinx-timeline` fills this gap with a
pure RST + CSS approach that integrates naturally with the Sphinx ecosystem.

---

## Architecture

```
Author writes RST
      │
      ▼
┌─────────────────────┐
│  TimelineDirective  │  ←  parses :status:, :version:, :date:
│  TimelineItem­      │  ←  parses :tags:
│  Directive          │
└────────┬────────────┘
         │ creates docutils nodes
         ▼
┌────────────────────┐
│  timeline node     │  attrs: status, version, date
│  timeline_item node│  attrs: tags[]
└────────┬───────────┘
         │ Sphinx traverses node tree
         ▼
┌──────────────────────────┐
│  visit_*/depart_* funcs  │  registered via app.add_node()
└────────────┬─────────────┘
             │ writes HTML strings
             ▼
┌─────────────────────────┐
│  HTML output            │  + timeline.css injected via app.add_css_file()
└─────────────────────────┘
```

---

## HTML output structure

```html
<div class="sphinx-timeline sphinx-timeline--released">

  <!-- Left column: sidebar -->
  <div class="sphinx-timeline__sidebar">
    <div class="sphinx-timeline__marker">
      <div class="sphinx-timeline__label">
        <span class="sphinx-timeline__version">v1.2.0</span>
        <span class="sphinx-timeline__date">Mar 19, 2026</span>
      </div>
      <div class="sphinx-timeline__dot"></div>   <!-- pulsing ring via ::after -->
    </div>
    <div class="sphinx-timeline__line"></div>    <!-- vertical rule -->
  </div>

  <!-- Right column: stacked cards -->
  <div class="sphinx-timeline__content">

    <div class="sphinx-timeline__item sphinx-timeline__item--released">
      <div class="sphinx-timeline__tags">
        <span class="sphinx-timeline__tag">cloud</span>
      </div>
      <!-- nested RST content rendered normally by Sphinx -->
    </div>

  </div>
</div>
```

For `status=development` the root class becomes `sphinx-timeline--development`
and every item gets `sphinx-timeline__item--development`.

---

## 10 design decisions

### 1. Two-directive hierarchy instead of a flat list

**Decision:** Use a parent `timeline` + child `timeline-item` directive pair.

**Rationale:** A single flat directive would require re-specifying the status
on every item. The parent/child model mirrors how RST already works (e.g.
`toctree` / entries, `tabs` / `tab`) and keeps the version metadata in one
place per section.

**Trade-off:** Authors must nest correctly. A `timeline-item` outside a
`timeline` produces no error — the node renders but inherits no status. This
is acceptable; Sphinx extensions conventionally trust author intent.

---

### 2. CSS-only — no JavaScript

**Decision:** All interactivity (animation, dark mode) is handled purely in
CSS via `@keyframes`, CSS custom properties, and media queries.

**Rationale:** Sphinx builds static HTML. Injecting JavaScript creates
ordering dependencies, Content Security Policy issues, and maintenance burden.
CSS loads synchronously with the page and has zero runtime risk.

**Trade-off:** Advanced interactivity (collapsible items, filtering by tag) is
not possible without JS. This is an intentional scope constraint.

---

### 3. BEM class naming with `sphinx-timeline` prefix

**Decision:** All classes follow BEM: `sphinx-timeline`, `sphinx-timeline__sidebar`,
`sphinx-timeline__item--released`.

**Rationale:** Sphinx themes (pydata, book, alabaster, RTD) all include
Bootstrap or custom resets that may collide with generic class names. A
project-specific prefix namespaces the extension completely.

**Trade-off:** Verbose class names. Acceptable for a library; authors never
write these classes directly.

---

### 4. `--tl-*` CSS custom properties as the theming layer

**Decision:** Every design token is a CSS variable in the `--tl-*` namespace,
with fallback chains: `--tl-color-released: var(--pst-color-success, #22c55e)`.

**Rationale:** This allows three levels of override with zero configuration:
(a) pydata/book themes override automatically via `--pst-*`, (b) users can
override individual tokens in `custom.css`, (c) hardcoded values guarantee
correct rendering on any unknown theme.

**Trade-off:** Variables defined in `:root` are global. A future version may
scope them to `.sphinx-timeline` if conflicts arise.

---

### 5. `setuptools` as build backend with `VERSION` as single source of truth

**Decision:** `pyproject.toml` declares `dynamic = ["version"]` and reads from
the `VERSION` plain-text file via `[tool.setuptools.dynamic]`.

**Rationale:** Keeping the version in one file makes it easy for CI to read,
tag, and bump without parsing Python or TOML. setuptools supports `file:`
version sources natively — no plugins required.

**Trade-off:** `hatchling` (the previous backend) does not support plain-text
file version sources without a custom hook, so we switched. The trade-off is
a slightly less modern build backend, compensated by the simplicity of VERSION.

---

### 6. `importlib.metadata` for `__version__` at runtime

**Decision:** `__init__.py` resolves `__version__` via `importlib.metadata.version()`
rather than reading VERSION at runtime.

**Rationale:** The VERSION file is only present in the source tree, not in an
installed wheel. Reading it at runtime would break for users who install via
pip. `importlib.metadata` reads the version from the installed package
metadata, which is always correct regardless of install method.

**Trade-off:** `__version__` is `"unknown"` in editable installs where the
package metadata is not yet generated. This is a known limitation of editable
installs in some edge cases.

---

### 7. `prefers-reduced-motion` disables the pulse animation

**Decision:** The dot glow animation is suppressed for users with
`prefers-reduced-motion: reduce` set in their OS accessibility settings.

**Rationale:** Continuously animated elements can cause problems for users
with vestibular disorders or epilepsy. WCAG 2.1 guideline 2.3.3 recommends
honoring this preference.

**Trade-off:** None — the timeline is fully functional without the animation.

---

### 8. CSS Grid for the two-column layout

**Decision:** The sidebar + content layout uses `display: grid` with
`grid-template-columns: var(--tl-sidebar-width) 1fr`.

**Rationale:** CSS Grid is the cleanest way to express a "fixed sidebar,
fluid content" layout. It collapses gracefully to a single column at 768 px
via a media query without JavaScript.

**Trade-off:** CSS Grid is not supported in IE 11. This is acceptable — Sphinx
itself dropped IE 11 support in Sphinx 5.

---

### 9. LaTeX visitors as simple text fallback

**Decision:** The LaTeX visitors emit bold labels and italic tags but make no
attempt to reproduce the visual timeline layout.

**Rationale:** LaTeX output (`sphinx-build -b latex`) is typically used for
PDF export. Reproducing a pixel-accurate timeline in LaTeX would require
complex TikZ or tabular code and would be fragile across LaTeX distributions.
A readable textual fallback serves the primary use case (PDF changelogs).

**Trade-off:** The LaTeX output is not visually equivalent to HTML. This is
documented behaviour.

---

### 10. Integration-style tests via full Sphinx builds

**Decision:** The test suite uses a `build_html` pytest fixture that performs
a complete `sphinx-build` in a temporary directory and asserts on the raw HTML
output.

**Rationale:** Unit-testing docutils visitors in isolation requires mocking
the translator object, which is complex and brittle. A full build test catches
regressions at every layer: directive parsing, node construction, visitor
output, and CSS injection.

**Trade-off:** Tests are slower than unit tests (~1 s per test vs. milliseconds).
The suite has 6 tests and runs in under 2 seconds total — acceptable.

---

## CI/CD pipeline

```
developer opens PR
        │
        ▼
┌──────────────────────────────┐
│  ci.yml                      │
│  ├─ ruff check + format      │  ← must pass before merge
│  └─ pytest (3.9, 3.10,       │
│            3.11, 3.12)       │
└──────────────────────────────┘
        │ PR merged to master
        ▼
┌──────────────────────────────┐
│  tag.yml                     │
│  └─ reads VERSION            │
│     creates git tag vX.Y.Z   │
└──────────────┬───────────────┘
               │ tag push triggers
               ▼
┌──────────────────────────────┐
│  release.yml                 │
│  ├─ uv build                 │  builds sdist + wheel
│  └─ uv publish               │  → PyPI (PYPI_API_TOKEN)
└──────────────────────────────┘
```
