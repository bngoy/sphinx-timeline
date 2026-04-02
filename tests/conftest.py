"""Pytest fixtures for sphinx-changelog-timeline tests."""

import shutil

import pytest
from sphinx.application import Sphinx


@pytest.fixture()
def build_html(tmp_path):
    """Build a minimal Sphinx project and return the output directory."""
    src = tmp_path / "src"
    src.mkdir()
    out = tmp_path / "out"

    # conf.py
    (src / "conf.py").write_text(
        'extensions = ["sphinx_changelog_timeline"]\nexclude_patterns = ["_build"]\n'
    )

    # index.rst with a simple timeline
    (src / "index.rst").write_text(
        "Test\n"
        "====\n"
        "\n"
        ".. timeline::\n"
        "   :version: v1.0.0\n"
        "   :date: Jan 1, 2026\n"
        "   :status: released\n"
        "\n"
        "   .. timeline-item::\n"
        "      :tags: feature, docs\n"
        "\n"
        "      **First feature**\n"
        "\n"
        "      Description of the first feature.\n"
        "\n"
        "   .. timeline-item::\n"
        "\n"
        "      **Second feature**\n"
        "\n"
        "      No tags here.\n"
        "\n"
        ".. timeline::\n"
        "   :status: development\n"
        "\n"
        "   .. timeline-item::\n"
        "      :tags: experimental\n"
        "\n"
        "      **Future work**\n"
        "\n"
        "      This is in development.\n"
    )

    app = Sphinx(
        srcdir=str(src),
        confdir=str(src),
        outdir=str(out),
        doctreedir=str(tmp_path / "doctrees"),
        buildername="html",
    )
    app.build()

    yield out, app

    shutil.rmtree(tmp_path, ignore_errors=True)
