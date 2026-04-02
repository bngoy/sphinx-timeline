"""sphinx-changelog-timeline — A Sphinx extension to build changelog-style timelines."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _get_version
from pathlib import Path

from .directives import TimelineDirective, TimelineItemDirective
from .nodes import (
    depart_timeline_html,
    depart_timeline_item_html,
    depart_timeline_item_latex,
    depart_timeline_latex,
    timeline,
    timeline_item,
    visit_timeline_html,
    visit_timeline_item_html,
    visit_timeline_item_latex,
    visit_timeline_latex,
)

try:
    __version__ = _get_version("sphinx-changelog-timeline")
except PackageNotFoundError:
    __version__ = "unknown"

_STATIC_DIR = Path(__file__).parent / "_static"


def _add_static_path(app):
    app.config.html_static_path.append(str(_STATIC_DIR))


def setup(app):
    app.add_node(
        timeline,
        html=(visit_timeline_html, depart_timeline_html),
        latex=(visit_timeline_latex, depart_timeline_latex),
    )
    app.add_node(
        timeline_item,
        html=(visit_timeline_item_html, depart_timeline_item_html),
        latex=(visit_timeline_item_latex, depart_timeline_item_latex),
    )
    app.add_directive("timeline", TimelineDirective)
    app.add_directive("timeline-item", TimelineItemDirective)
    app.add_css_file("timeline.css")
    app.connect("builder-inited", _add_static_path)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
