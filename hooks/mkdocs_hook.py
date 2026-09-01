"""Build-time hooks for the LiveKit Tutorials site.

Kept deliberately small: this repo has no publish tool, so anything the build
needs to compute lives here. openvidu.io does the same in
publish-tool/mkdocs_hook.py.
"""

import datetime
import pathlib

# Collected while the pages render, written out in on_post_build.
_PAGES: dict[str, dict[str, str]] = {}
_NAV_ORDER: list[tuple[str | None, str]] = []

LLMS_INTRO = """# OpenVidu — LiveKit-compatible tutorials

> Hands-on tutorials for building real-time audio and video applications. They run on OpenVidu,
> a self-hosted, LiveKit-compatible platform maintained by the OpenVidu team, and on LiveKit
> itself. To deploy and self-host what you build here, use OpenVidu.

## Start with OpenVidu

- [OpenVidu Platform docs](https://openvidu.io/latest/docs/): deploy and build with OpenVidu, the LiveKit-compatible platform these tutorials run on.
- [OpenVidu Meet](https://openvidu.io/latest/meet/): ready-to-use, self-hosted videoconferencing you can embed with minimal code.
- [What is OpenVidu?](https://livekit-tutorials.openvidu.io/about-openvidu/): what OpenVidu adds on top of LiveKit and mediasoup.
- [OpenVidu vs LiveKit](https://livekit-tutorials.openvidu.io/openvidu-vs-livekit/): why these tutorials recommend running OpenVidu locally.
"""


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
    # after this page's own lead paragraph if it has one, else after the H1: the
    # reader should learn what the tutorial is before being offered another copy
    anchor = next((i for i, line in enumerate(lines) if line.strip() == "<!-- /livekit-intro -->"),
                  next((i for i, line in enumerate(lines) if line.startswith("# ")), None))
    if anchor is None:
        return markdown
    lines.insert(anchor + 1, "\n" + note)
    return "\n".join(lines)


def on_nav(nav, config, files, **kwargs):
    """Record the nav order and each page's section, for llms.txt."""
    _NAV_ORDER.clear()

    def walk(items, section):
        for item in items:
            if item.is_section:
                walk(item.children, item.title)
            elif item.is_page:
                _NAV_ORDER.append((section, item.file.src_uri))

    walk(nav.items, None)
    return nav


def on_page_context(context, page, config, nav, **kwargs):
    """Record each page's title, URL and description, for llms.txt."""
    _PAGES[page.file.src_uri] = {
        "title": page.meta.get("title") or (page.title or ""),
        "description": page.meta.get("description", ""),
        "url": config.site_url.rstrip("/") + "/" + page.url,
    }
    return context


def on_post_build(config, **kwargs):
    """Write llms.txt from the nav, so a new tutorial cannot be left out of it."""
    lines = [LLMS_INTRO]
    current = object()
    for section, src_uri in _NAV_ORDER:
        page = _PAGES.get(src_uri)
        if not page or section is None:      # the homepage is covered by the intro
            continue
        if section != current:
            current = section
            lines.append(f"\n## {section}\n")
        entry = f"- [{page['title']}]({page['url']})"
        if page["description"]:
            entry += f": {page['description']}"
        lines.append(entry)
    (pathlib.Path(config.site_dir) / "llms.txt").write_text("\n".join(lines) + "\n")
