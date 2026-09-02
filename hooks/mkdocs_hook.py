"""Build-time hooks for the LiveKit Tutorials site.

Kept deliberately small: this repo has no publish tool, so anything the build
needs to compute lives here. openvidu.io does the same in
publish-tool/mkdocs_hook.py.
"""

import datetime
import logging
import re
import subprocess
from pathlib import Path

from mkdocs.exceptions import PluginError

_log = logging.getLogger(f"mkdocs.hooks.{Path(__file__).stem}")


def on_config(config, **kwargs):
    """Replace {year} in the footer copyright with the build year.

    It was hard-coded, and had been reading "2025" since January.
    """
    if config.copyright and "{year}" in config.copyright:
        config.copyright = config.copyright.replace("{year}", str(datetime.date.today().year))
    return config


_SNIPPET_REF = re.compile(r'^\s*--8<--\s+"([^"]+)"', re.M)


def _git_dates(root: Path) -> dict[str, str] | None:
    """{repository-relative path: date of its last commit}, or None when git cannot answer.

    None means "leave MkDocs' build date alone": a shallow clone reports the fetched
    commit for every path, and no git at all is an ordinary way to build.
    """
    try:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=root,
                                 capture_output=True, text=True, check=True).stdout.strip()
        if shallow == "true":
            _log.info("Shallow clone: sitemap <lastmod> falls back to the build date.")
            return None
        log = subprocess.run(["git", "log", "--format=%x00%cs", "--name-only", "--",
                              "docs", "shared"],
                             cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        _log.info("Could not read dates from git (%s): <lastmod> falls back to the build date.",
                  error)
        return None
    dates: dict[str, str] = {}
    current = None
    for line in log.splitlines():
        if line.startswith("\x00"):
            current = line[1:]
        elif line and current:
            dates.setdefault(line, current)
    return dates


def on_env(env, config, files, **kwargs):
    """Set each page's `update_date`, which `overrides/sitemap.xml` publishes as `<lastmod>`.

    MkDocs sets it to the build date for every page, which asserts that the whole site
    changed on every publish. A page's date is the newest commit among its own file and
    every snippet it includes (transitively), so editing a shared snippet dates every page
    that renders it. `on_env` because MkDocs renders the theme's static templates —
    `sitemap.xml` among them — before the pages.
    """
    root = Path(config["docs_dir"]).resolve().parent
    dates = _git_dates(root)
    if dates is None:
        return env

    snippets = (config.get("mdx_configs") or {}).get("pymdownx.snippets") or {}
    bases = [Path(base).resolve().relative_to(root) for base in snippets.get("base_path") or ()]

    def newest(path: str, seen: set[str]) -> str:
        if path in seen:
            return ""
        seen.add(path)
        date = dates.get(path, "")
        try:
            text = (root / path).read_text(encoding="utf8")
        except OSError:
            return date
        for ref in _SNIPPET_REF.findall(text):
            for base in bases:
                snippet = f"{base}/{ref}"
                if (root / snippet).is_file():
                    date = max(date, newest(snippet, seen))
                    break
        return date

    dated = 0
    for file in files.documentation_pages():
        if file.page is None or file.generated_by is not None:
            continue
        date = newest(f"{Path(config['docs_dir']).name}/{file.src_uri}", set())
        if date:
            file.page.update_date = date
            dated += 1
    _log.info("sitemap <lastmod>: %d pages dated from git.", dated)
    return env


_GLIGHTBOX_JS = re.compile(r'<script src="([^"]*glightbox\.min\.js)"></script>')
_GLIGHTBOX_INIT = '<script id="init-glightbox">'
_GLIGHTBOX_HREF_MARKER = "element.setAttribute('href', img.src)"
_GLIGHTBOX_HREF_LOOP = re.compile(
    r"document\.querySelectorAll\('\.glightbox'\)\.forEach\(function\(element\) \{.*?\}\);\n",
    re.S,
)
_GLIGHTBOX_SUBSCRIBE = "document$.subscribe(()=>{ lightbox.reload(); });"


def _instant_safe_hrefs(output: str) -> str:
    """Refill the lightbox hrefs on every instant navigation.

    With the privacy plugin enabled (every build except `CI=false` ones), mkdocs-glightbox
    emits its `.glightbox` anchors without `href` and fills them from each image's `src` in
    a loop that runs once per full page load. `navigation.instant` swaps the content in
    without a page load, so pages navigated to had bare anchors and opened empty slides.
    The loop moves into the `document$` subscription, which fires on the initial load and
    on every instant navigation, before the plugin's own `lightbox.reload()` rescan.
    """
    if _GLIGHTBOX_HREF_MARKER not in output:
        return output  # privacy disabled: the anchors carry their hrefs from the build
    loop = _GLIGHTBOX_HREF_LOOP.search(output)
    if loop is None or _GLIGHTBOX_SUBSCRIBE not in output:
        raise PluginError(
            "mkdocs-glightbox changed the shape of its privacy-mode init script, so its "
            "href-filling no longer survives instant navigation. Update _instant_safe_hrefs "
            "in hooks/mkdocs_hook.py to the new shape."
        )
    wrapped = f"const fillGlightboxHrefs = () => {{\n{loop.group(0)}}};\n"
    output = output[: loop.start()] + wrapped + output[loop.end():]
    return output.replace(
        _GLIGHTBOX_SUBSCRIBE,
        "document$.subscribe(()=>{ fillGlightboxHrefs(); lightbox.reload(); });",
    )


def on_post_page(output, page, config, **kwargs):
    """Move the glightbox library out of `<head>` and make its init instant-navigation-safe.

    The plugin injects its ~57 KB script there synchronously on every page, blocking first
    paint. It is only needed by the `#init-glightbox` script at the end of `<body>`, so it
    loads there instead. Ported from openvidu.io's hook, without the instance handover:
    this site has no custom gallery script, so the plugin's own init stays in charge.
    """
    match = _GLIGHTBOX_JS.search(output)
    if match is None or _GLIGHTBOX_INIT not in output:
        return None
    output = output[: match.start()] + output[match.end():]
    init_pos = output.find(_GLIGHTBOX_INIT)
    return _instant_safe_hrefs(output[:init_pos] + match.group(0) + output[init_pos:])


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
