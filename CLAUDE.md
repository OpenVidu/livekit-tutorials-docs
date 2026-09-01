# CLAUDE.md

Source of <https://livekit-tutorials.openvidu.io> — MkDocs Material (pinned 9.7.6), one branch
(`main`), deployed by `mkdocs gh-deploy` from a **manual** workflow run. There is no versioning,
no `mike`, no publish tool and no redirect map here; if you are looking for those, you are
thinking of [openvidu.io](https://github.com/OpenVidu/openvidu.io).

## The one rule that matters

**The tutorials are published twice.** Every page under `docs/tutorials/` and every snippet in
`shared/tutorials/` also exists in openvidu.io's repo (`docs/docs/tutorials/`, and the same
`shared/tutorials/` path — snippet includes resolve against `shared/`, so the `--8<--` lines
match verbatim). This site is LiveKit-first, because it exists to win LiveKit-brand search
traffic; openvidu.io is OpenVidu-first. **Everything else must match**, and a script checks it:

```bash
tools/sync-check.py --openvidu-io ../openvidu.io
```

Run it after touching anything under `docs/tutorials/` or `shared/`. It compares all 43 page and
snippet pairs, normalizes the differences that are intentional (listed at the top of the script,
and in [README.md](README.md)) and reports anything else. **A change here that is not mirrored
there is a bug**, and vice versa — the two copies had silently drifted for over a year before
this check existed.

Never resolve a report by widening the script's exceptions unless the difference is genuinely
deliberate; then say why in the same commit.

## Link forms

| Target | Form | Example |
|---|---|---|
| A page on this site | relative, with `.md` | `[x](../application-server/index.md)` |
| An asset from a page | relative, with `.md`-style path | `![alt](../../assets/images/…)` |
| An asset from a `shared/` snippet | root-absolute (a snippet is included at more than one depth) | `![alt](/assets/images/…)` |
| openvidu.io | absolute, **version-less** `/latest/` | `https://openvidu.io/latest/docs/reference/webhooks/` |
| Tutorial source code | `github.com/OpenVidu/openvidu-livekit-tutorials/tree/master/…` (buttons; code-fence `title=` captions use `/blob/master/…`) — this site is unversioned, so it tracks `master` (openvidu.io pins the release tag) | |

Every link that leaves this site gets `{:target="_blank"}` **and** the icon
`:fontawesome-solid-external-link:{.external-link-icon}` — including links to openvidu.io, which
from here are external. Button links (`{ .md-button … }`) and local links (`http://localhost:…`,
the reader's own machine) do not get the icon.

Conversion links to openvidu.io (the announce band, the two funnel pages, the deploy step, the
footer) carry `utm_source=livekit-tutorials&utm_medium=referral` plus a `utm_campaign` naming the
placement. Plain in-tutorial reference links stay untagged.

## Frontmatter

Every page needs a unique `title` (≤45 chars — Material appends `" - LiveKit Tutorials"`) and a
unique `description` (100–160 chars). Checked by `tools/sync-check.py --frontmatter`.

## Structure

- `nav` in `mkdocs.yml` is a literal tree: a new page goes in `nav` or in `not_in_nav`.
- `overrides/` lives at the repo root, **not** under `docs/` — inside `docs_dir` MkDocs would
  publish the templates.
- `shared/` snippets render inside several pages; grep for the snippet's `--8<--` usages before
  editing one.
- `hooks/mkdocs_hook.py` stamps the copyright year, injects the counterpart box, and feeds the
  `llmstxt` plugin each page's own title and description — a page listed in the llmstxt
  sections without both **fails the build**. Add build-time computation there.
- Pins live in `Dockerfile` and `.github/workflows/publish-web.yaml` and **must match
  openvidu.io's** (mkdocs 1.6.1, material 9.7.6, pymdown-extensions 11.0.1, pygments 2.19.2,
  glightbox 0.5.2, llmstxt 0.5.0): the two sites render the same Markdown, so a version drift
  is a rendering drift.

## The build rule

`mkdocs build --strict` must pass with **zero WARNINGs** (the publish workflow deploys with
`--strict`). Anchor `INFO` lines about
`#run-openvidu-locally` and `#deploy-openvidu` are `pymdownx.tabbed` tab anchors that MkDocs'
validator cannot see — expected, do not chase them.

## Publishing

**Merging to `main` publishes nothing.** The live site changes only when the
[Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml)
workflow is run by hand on `main`. A tutorial change usually also needs openvidu.io's own publish
so the two copies stay in step — see [README.md](README.md).

## Commands

| Task | Command |
|---|---|
| Build the dev image (once) | `docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .` |
| Serve with live reload | `docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material` |
| Build (what CI runs) | `GOOGLE_ANALYTICS_KEY=G-XXXXXXXX mkdocs build --strict` |
| Sync check | `tools/sync-check.py --openvidu-io ../openvidu.io` |
| Frontmatter check | `tools/sync-check.py --frontmatter` |

`CI=false` disables the `privacy` plugin (which self-hosts the font) to keep local builds offline
and fast.
