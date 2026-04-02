"""Custom docutils nodes and HTML/LaTeX visitors for sphinx-timeline."""

from docutils import nodes


class timeline(nodes.General, nodes.Element):
    """Node representing a timeline section (released or in-development)."""


class timeline_item(nodes.General, nodes.Element):
    """Node representing a single item/card within a timeline."""


# ---------------------------------------------------------------------------
# HTML visitors
# ---------------------------------------------------------------------------


def visit_timeline_html(self, node):
    status = node.get("status", "released")
    version = node.get("version", "")
    date = node.get("date", "")

    self.body.append(f'<div class="sphinx-timeline sphinx-timeline--{status}">')

    # Sidebar: marker (label + dot) + vertical line
    self.body.append('<div class="sphinx-timeline__sidebar">')
    self.body.append('<div class="sphinx-timeline__marker">')

    # Label
    self.body.append('<div class="sphinx-timeline__label">')
    if status == "development":
        self.body.append('<span class="sphinx-timeline__version">In development</span>')
    else:
        if version:
            self.body.append(f'<span class="sphinx-timeline__version">{version}</span>')
        if date:
            self.body.append(f'<span class="sphinx-timeline__date">{date}</span>')
    self.body.append("</div>")  # end label

    # Dot
    self.body.append('<div class="sphinx-timeline__dot"></div>')
    self.body.append("</div>")  # end marker

    # Vertical line
    self.body.append('<div class="sphinx-timeline__line"></div>')
    self.body.append("</div>")  # end sidebar

    # Content area
    self.body.append('<div class="sphinx-timeline__content">')


def depart_timeline_html(self, node):
    self.body.append("</div>")  # end content
    self.body.append("</div>")  # end sphinx-timeline


def visit_timeline_item_html(self, node):
    status = node.parent.get("status", "released") if node.parent else "released"
    self.body.append(
        f'<div class="sphinx-timeline__item sphinx-timeline__item--{status}">'
    )

    tags = node.get("tags", [])
    if tags:
        self.body.append('<div class="sphinx-timeline__tags">')
        for tag in tags:
            self.body.append(f'<span class="sphinx-timeline__tag">{tag}</span>')
        self.body.append("</div>")


def depart_timeline_item_html(self, node):
    self.body.append("</div>")  # end item


# ---------------------------------------------------------------------------
# LaTeX visitors (simple fallback)
# ---------------------------------------------------------------------------


def visit_timeline_latex(self, node):
    status = node.get("status", "released")
    version = node.get("version", "")
    date = node.get("date", "")

    if status == "development":
        self.body.append("\n\\textbf{In development}\n\n")
    else:
        label_parts = []
        if version:
            label_parts.append(version)
        if date:
            label_parts.append(date)
        if label_parts:
            self.body.append(f"\n\\textbf{{{' — '.join(label_parts)}}}\n\n")


def depart_timeline_latex(self, node):
    self.body.append("\n")


def visit_timeline_item_latex(self, node):
    tags = node.get("tags", [])
    if tags:
        tag_str = ", ".join(tags)
        self.body.append(f"\\textit{{{tag_str}}}\n\n")


def depart_timeline_item_latex(self, node):
    self.body.append("\n")
