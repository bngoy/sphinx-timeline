"""Sphinx directives for timeline and timeline-item."""

from docutils.parsers.rst import Directive, directives

from .nodes import timeline, timeline_item


class TimelineDirective(Directive):
    """A timeline section grouping multiple timeline items.

    Usage::

        .. timeline::
           :version: v1.0.0
           :date: Mar 19, 2026
           :status: released

           .. timeline-item::
              :tags: feature

              **My feature title**

              Description of the feature.
    """

    has_content = True
    option_spec = {
        "version": directives.unchanged,
        "date": directives.unchanged,
        "status": lambda arg: directives.choice(arg, ("released", "development")),
    }

    def run(self):
        node = timeline()
        node["status"] = self.options.get("status", "released")
        node["version"] = self.options.get("version", "")
        node["date"] = self.options.get("date", "")
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class TimelineItemDirective(Directive):
    """A single card/block within a timeline section.

    Usage::

        .. timeline-item::
           :tags: cloud, performance

           **Card title**

           Card description with any RST content.
    """

    has_content = True
    option_spec = {
        "tags": directives.unchanged,
    }

    def run(self):
        node = timeline_item()
        raw_tags = self.options.get("tags", "")
        node["tags"] = [t.strip() for t in raw_tags.split(",") if t.strip()]
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]
