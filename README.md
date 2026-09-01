# livekit-tutorials-docs

Visit at [https://livekit-tutorials.openvidu.io/](https://livekit-tutorials.openvidu.io/).

Create custom Docker image with necessary extra plugings:

```bash
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .
```

Serve:

```bash
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

Build:

```bash
docker run --rm -it -v ${PWD}:/docs squidfunk/mkdocs-material build
```

## Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_

The same tutorials are published on both sites for different audiences: this one is LiveKit-first
(it captures LiveKit-brand search traffic), [openvidu.io](https://github.com/OpenVidu/openvidu.io)
is OpenVidu-first. **Any change to a tutorial must be made on both sides.**

Check it with:

```bash
tools/sync-check.py [--openvidu-io ../openvidu.io]   # the two copies still agree
tools/sync-check.py --frontmatter                    # titles <=45, descriptions 100-160, both unique
```

It compares every tutorial page and snippet against its openvidu.io counterpart, normalizing away
the differences that are intentional, and exits non-zero if anything else differs. The intentional
differences, all listed at the top of the script:

| | This site | openvidu.io |
|---|---|---|
| Frontmatter `title`/`description` | LiveKit-first wording | OpenVidu-first wording |
| Tutorial source links | track `master` | pinned to the release tag |
| Links to openvidu.io | absolute, version-less (`/latest/`), UTM-tagged on conversion links | repo-relative `.md` |
| Step 1 | `run-livekit-server*.md`: LiveKit local, LiveKit Cloud or OpenVidu | runs OpenVidu |
| "Accessing your app from other devices" | this site's own comparison page | openvidu.io self-hosting docs |
| Recording tutorials | S3 only; the Azure case links openvidu.io's Azure tutorials | S3 and Azure variants |
| Image paths | `/assets/images/…` | `/assets/images/platform/tutorials/…` |
| The external-link icon | on links to openvidu.io too — from here they leave the site | only on third-party links |

When a real difference is meant to stay, add it to the script's rules with a comment saying why —
never leave it reported.

## Publishing

Merging to `main` does not change the live site.

- In this repository, push to `main` and run GitHub Action [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml) selecting the `main` branch.
- In repository [openvidu.io](https://github.com/OpenVidu/openvidu.io), push to `main` and run the GitHub Action to [overwrite the latest version](https://github.com/OpenVidu/openvidu.io#overwriting-the-latest-version), so the tutorials at [openvidu.io/latest/docs/tutorials](https://openvidu.io/latest/docs/tutorials/application-client/) match.
