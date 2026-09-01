---
description: Publish this site (and remind about openvidu.io's own publish)
---

Merging to `main` does not change the live site. To publish:

1. Confirm `main` is clean and `/check-site` passes.
2. Run the [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml)
   workflow on `main` (`gh workflow run publish-web.yaml --ref main`), then watch it:
   `gh run watch $(gh run list --workflow=publish-web.yaml --limit 1 --json databaseId -q '.[0].databaseId')`.
   It runs `mkdocs gh-deploy --force`; GitHub Pages then rebuilds `gh-pages` a little later
   (`gh api repos/OpenVidu/livekit-tutorials-docs/pages/builds/latest -q .status` → `built`).
3. **If the change touched the tutorials, openvidu.io needs publishing too**, or the two copies
   go out of step: push the mirrored change there and run its Publish Web action with command
   `latest`.
4. Verify live: the changed pages, `robots.txt` and `llms.txt` (200), the footer year, and that
   `/overrides/main.html` still 404s.

Ask before starting: publishing is the user's call, and this workflow is the only thing that
changes what visitors see.
