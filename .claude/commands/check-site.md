---
description: Run every check this repo has — build, sync with openvidu.io, frontmatter, links
---

Run all four, from the repo root, and report each result. Do not stop at the first failure.

1. **Build** — `--strict` turns any WARNING into a failure:
   ```bash
   GOOGLE_ANALYTICS_KEY=G-XXXXXXXX CI=false mkdocs build --strict -d /tmp/lk-site
   ```
   Without a local mkdocs, run it through Docker instead:
   `docker run --rm -e CI=false -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX -v ${PWD}:/docs squidfunk/mkdocs-material build --strict`
   (output lands in `site/`, which is gitignored).
2. **Sync with openvidu.io** — the tutorials are published on both sites and must agree:
   ```bash
   tools/sync-check.py --openvidu-io ../openvidu.io
   ```
   If there is no checkout next door, say so rather than skipping silently.
3. **Frontmatter budgets**:
   ```bash
   tools/sync-check.py --frontmatter
   ```
4. **External links** — the full sweep is the weekly `check-external-links.yaml` workflow
   (lychee over the built HTML, reporting through the `broken-links` issue); dispatch it with
   `gh workflow run check-external-links.yaml` when a full pass is wanted now. For the pages a
   change touched, spot-check their off-site URLs with `curl -sS -o /dev/null -w '%{http_code}
   r=%{num_redirects}' -L` (200, no redirect hop). GitHub rate-limits anonymous HTML requests,
   so check `github.com/OpenVidu/openvidu-livekit-tutorials` paths through `gh api` instead.
   Known deliberate exceptions: `cloud.livekit.io` (login hop), `kurento.openvidu.io` (OpenVidu's
   own vanity domain) and `openvidu.medium.com` (403 to bots).

Report a one-line verdict per check plus the details of anything that failed.
