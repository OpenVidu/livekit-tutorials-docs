---
name: mirror-openvidu-io
description: Carry a tutorial change between this site and openvidu.io, keeping the two copies in sync. Use when a tutorial page or shared snippet changes on either side, when openvidu.io releases a new version, or when sync-check.py reports drift.
---

# Mirroring a tutorial change

The same tutorials are published twice: LiveKit-first here, OpenVidu-first on openvidu.io
(`../openvidu.io`). A change to either copy has to be carried to the other.

## File mapping

| Here | openvidu.io |
|---|---|
| `docs/tutorials/application-client/*.md` | `docs/docs/tutorials/application-client/*.md` |
| `docs/tutorials/application-server/*.md` | `docs/docs/tutorials/application-server/*.md` |
| `docs/tutorials/advanced-features/recording-basic.md` | `…/advanced-features/recording-basic-s3.md` |
| `docs/tutorials/advanced-features/recording-advanced.md` | `…/advanced-features/recording-advanced-s3.md` |
| `shared/application-client/*.md`, `shared/application-server/*.md` | `shared/tutorials/…` (`tabs.md` = `application-*-tabs.md` here) |
| `shared/{configure-urls,testing-other-devices,webhook-local-server,run-openvidu-locally}.md` | `shared/tutorials/…` |
| `shared/run-livekit-server*.md` | no counterpart — this site's own step 1 |

## What to change when carrying a hunk

Translate, do not copy verbatim:

- **Frontmatter** — keep each side's own `title`/`description` (LiveKit-first vs OpenVidu-first).
- **Source links** — `blob/master/…` here, `blob/<version>/…` there. Line ranges are the same.
- **Links to openvidu.io** — absolute `https://openvidu.io/latest/docs/…` here (with
  `{:target="_blank"}` and the external-link icon), repo-relative `.md` there.
- **Snippet includes** — `shared/x.md` here, `tutorials/x.md` there.
- **Step 1** — this site includes `run-livekit-server*.md`; openvidu.io runs OpenVidu. Do not
  carry that block either way.
- **Image paths** — `/assets/images/…` here, `/assets/images/platform/tutorials/…` there.
- **"Accessing your app from other devices"** — this site links its own comparison page,
  openvidu.io links its self-hosting docs.

## Always finish with

```bash
tools/sync-check.py --openvidu-io ../openvidu.io
```

It must report every pair in sync. If a difference is genuinely deliberate, add it to the script's
rules **with a comment saying why**, and to the table in `README.md` — never leave it reported.

Then remember both sites publish separately, by hand: see `/publish`.
