---
description: Run every check this repo has — build, sync with openvidu.io, frontmatter, links
---

Run all four, from the repo root, and report each result. Do not stop at the first failure.

1. **Build** — must be zero WARNINGs:
   ```bash
   GOOGLE_ANALYTICS_KEY=G-XXXXXXXX CI=false mkdocs build -d /tmp/lk-site
   ```
2. **Sync with openvidu.io** — the tutorials are published on both sites and must agree:
   ```bash
   tools/sync-check.py --openvidu-io ../openvidu.io
   ```
   If there is no checkout next door, say so rather than skipping silently.
3. **Frontmatter budgets**:
   ```bash
   tools/sync-check.py --frontmatter
   ```
4. **External links** — every off-site URL in the built site should answer 200 with no redirect
   hop. Extract them from `/tmp/lk-site` and probe with `curl -sS -o /dev/null -w '%{http_code}
   r=%{num_redirects}' -L`. GitHub rate-limits anonymous HTML requests, so check
   `github.com/OpenVidu/openvidu-livekit-tutorials` paths through `gh api` instead. Known
   deliberate exceptions: `cloud.livekit.io` (login hop), `kurento.openvidu.io` (OpenVidu's own
   vanity domain) and `openvidu.medium.com` (403 to bots).

Report a one-line verdict per check plus the details of anything that failed.
