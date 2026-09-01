---
description: Start the local MkDocs dev server with live reload (Docker)
---

Serve the site locally with live reload. Run from the repo root, in the background:

```bash
docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

- If the image is missing, build it first (a few minutes):
  `docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .`
- If host port 8000 is taken, map another one (`-p 9100:8000`) — do not stop whatever holds it.
- Report the URL and watch the startup log: the build must reach "Serving on" with **zero
  WARNINGs**. `INFO` lines about `#run-openvidu-locally` / `#deploy-openvidu` anchors are
  `pymdownx.tabbed` false positives — expected.

Expected local behaviour, not to be "fixed": canonicals and JSON-LD show the localhost URL, and
the `privacy` plugin is off unless `CI` is set, so the font loads from Google rather than from
`assets/external/`.

- `--dirty` is on (fast, rebuilds only the edited page): after editing a shared snippet, a hook
  or an override, touch the including page (or restart) to see the change everywhere. For a
  full-fidelity serve, override the CMD to drop it:
  `docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material serve --dev-addr=0.0.0.0:8000 --livereload`

Stop it with `docker stop mkdocs`.
