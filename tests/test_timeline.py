"""Tests for the sphinx-timeline extension."""

from pathlib import Path


def test_build_succeeds(build_html):
    """The Sphinx build should complete without warnings."""
    out, app = build_html
    index = out / "index.html"
    assert index.exists(), "index.html was not generated"


def test_timeline_classes_present(build_html):
    """Output HTML should contain the expected BEM classes."""
    out, _ = build_html
    html = (out / "index.html").read_text()

    assert "sphinx-timeline" in html
    assert "sphinx-timeline--released" in html
    assert "sphinx-timeline--development" in html
    assert "sphinx-timeline__item--released" in html
    assert "sphinx-timeline__item--development" in html


def test_version_and_date_rendered(build_html):
    """The sidebar should display version and date."""
    out, _ = build_html
    html = (out / "index.html").read_text()

    assert "v1.0.0" in html
    assert "Jan 1, 2026" in html


def test_development_label(build_html):
    """Development timelines should show 'In development'."""
    out, _ = build_html
    html = (out / "index.html").read_text()

    assert "In development" in html


def test_tags_rendered(build_html):
    """Tags should be rendered as pills with the correct class."""
    out, _ = build_html
    html = (out / "index.html").read_text()

    assert "sphinx-timeline__tag" in html
    assert "feature" in html
    assert "docs" in html
    assert "experimental" in html


def test_css_included(build_html):
    """The timeline CSS file should be referenced in the output."""
    out, _ = build_html
    html = (out / "index.html").read_text()

    assert "timeline.css" in html
