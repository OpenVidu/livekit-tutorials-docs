"""Build-time hooks for the LiveKit Tutorials site.

Kept deliberately small: this repo has no publish tool, so anything the build
needs to compute lives here. openvidu.io does the same in
publish-tool/mkdocs_hook.py.
"""

import datetime

from mkdocs.exceptions import PluginError


def on_config(config, **kwargs):
    """Replace {year} in the footer copyright with the build year.

    It was hard-coded, and had been reading "2025" since January.
    """
    if config.copyright and "{year}" in config.copyright:
        config.copyright = config.copyright.replace("{year}", str(datetime.date.today().year))
    return config


# openvidu.io publishes the same tutorials OpenVidu-first. Linking each page to
# its counterpart interlinks the two copies (issue #38) and gives a reader who
# is already on OpenVidu the version written for them.
_CROSS_LINK_ROOT = "https://openvidu.io/latest/docs/tutorials/"
_COUNTERPART = {
    "tutorials/advanced-features/recording-basic.md": "advanced-features/recording-basic-s3/",
    "tutorials/advanced-features/recording-advanced.md": "advanced-features/recording-advanced-s3/",
}


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Add the openvidu.io counterpart link under each tutorial's H1."""
    src = page.file.src_uri
    if not src.startswith("tutorials/"):
        return markdown
    target = _COUNTERPART.get(src)
    if target is None:
        target = src[len("tutorials/"):].removesuffix(".md").removesuffix("/index") + "/"
        if src.endswith("/index.md"):
            target = src[len("tutorials/"):-len("index.md")]
    note = (f'!!! info "Running OpenVidu?"\n\n'
            f'    OpenVidu is a self-hosted, LiveKit-compatible platform. If that is what you are '
            f'running, read the '
            f'[OpenVidu version of this tutorial :fontawesome-solid-external-link:'
            f'{{.external-link-icon}}]({_CROSS_LINK_ROOT}{target}'
            f'?utm_source=livekit-tutorials&utm_medium=referral&utm_campaign=tutorial-cross-link)'
            f'{{:target="_blank"}}.')
    lines = markdown.split("\n")
    h1 = next((i for i, line in enumerate(lines) if line.startswith("# ")), None)
    if h1 is None:
        return markdown
    lines.insert(h1 + 1, "\n" + note)
    return "\n".join(lines)


def _one_line(value) -> str:
    """A frontmatter value as a single line, so it cannot break llms.txt's one-entry-per-line."""
    return " ".join(str(value).split())


def _required(meta, key: str, src_uri: str) -> str:
    value = meta.get(key)
    if not value or not str(value).strip():
        raise PluginError(
            f"'{src_uri}' is listed in the llmstxt sections but has no `{key}` in its "
            f"frontmatter. Every exported page needs a `title` and a `description`: together "
            f"they are the line that tells an assistant whether to read the page."
        )
    return _one_line(value)


def on_page_content(html, page, config, **kwargs):
    """Use the page's own `title` and `description` frontmatter for its llms.txt entry.

    Ported from openvidu.io's publish-tool/mkdocs_hook.py. Both halves stop llms.txt taking
    its text from somewhere other than the page:

    * **The description** would be the value written beside the path in mkdocs.yml — the same
      sentence maintained twice, and a glob entry can only carry *one* description for every
      page it matches.
    * **The title** would be `page.title`, which MkDocs resolves as the *nav label* first —
      clear beside its parent in a sidebar, useless in a flat list.

    Ordering is guaranteed: `hooks` handlers run after the plugins' for the same event, which
    is what lets this overwrite `_md_pages`, filled in during the plugin's own
    `on_page_content`.
    """
    plugin = config["plugins"].get("llmstxt")
    if plugin is None:
        return None

    # Both are private, and both are read in the plugin's `on_post_build`:
    #   `_sections`  {section title: {src_uri: description}}, built in its `on_files`
    #   `_md_pages`  {src_uri: _MDPageInfo(title, path_md, md_url, content)}, built in its
    #                `on_page_content`
    # Their shape is asserted rather than skipped quietly, so a plugin upgrade that renames
    # either fails the build instead of publishing an llms.txt full of nav labels and no
    # descriptions.
    sections = getattr(plugin, "_sections", None)
    exported = getattr(plugin, "_md_pages", None)
    if not isinstance(sections, dict) or not isinstance(exported, dict):
        raise PluginError(
            "mkdocs-llmstxt no longer exposes `_sections` and `_md_pages`, so llms.txt entries "
            "cannot be taken from the pages. Update hooks/mkdocs_hook.py to the new API."
        )

    src_uri = page.file.src_uri
    listed = [pages for pages in sections.values() if src_uri in pages]
    if not listed:
        return None

    meta = page.meta or {}
    title = _required(meta, "title", src_uri)
    description = _required(meta, "description", src_uri)

    for pages in listed:
        pages[src_uri] = description

    info = exported.get(src_uri)
    if info is None:  # pragma: no cover - the plugin records every page it selected
        raise PluginError(
            f"mkdocs-llmstxt selected '{src_uri}' but did not record it, so its llms.txt title "
            "would keep the nav label. Update hooks/mkdocs_hook.py to the new API."
        )
    exported[src_uri] = info._replace(title=title)
    return None
