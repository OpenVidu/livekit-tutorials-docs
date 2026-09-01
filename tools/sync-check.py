#!/usr/bin/env python3
"""Compare this site's tutorials with their openvidu.io counterparts.

Both sites document the same tutorial code for different audiences: this one is
LiveKit-first, openvidu.io is OpenVidu-first. Everything else should match. This
script normalizes away the differences that are intentional (listed in
DELIBERATE below) and prints whatever is left, so a drift between the two repos
shows up as a diff instead of going unnoticed.

    tools/sync-check.py [--openvidu-io PATH] [--context N]

Exits 1 if the two sides differ in any way that is not intentional.
"""
from __future__ import annotations

import argparse
import difflib
import pathlib
import posixpath
import re
import sys

# --- What is intentionally different -----------------------------------------
#
# 1. Frontmatter title/description: written for each site's own audience.
# 2. Branch: this site tracks `master`, openvidu.io pins the release tag.
# 3. Links to openvidu.io: absolute and version-less (`/latest/`) here,
#    repo-relative there. UTM parameters exist only here.
# 4. Step 1: this site offers LiveKit local / LiveKit Cloud / OpenVidu, so it
#    uses its own `run-livekit-server*.md` snippets; openvidu.io runs OpenVidu.
# 5. "Accessing your app from other devices": this site keeps the reader on its
#    own comparison page, openvidu.io links its self-hosting docs.
# 6. Recording pages: no Azure variants here, so the Azure case links
#    openvidu.io's Azure tutorials instead.
# 7. The external-link icon marks a link that leaves the site, so it appears on
#    this site's links to openvidu.io and not on openvidu.io's own relative
#    ones. On third-party links it is compared like any other text.

CLIENTS = ["index", "javascript", "react", "angular", "vue", "electron", "ionic", "android", "ios"]
SERVERS = ["index", "node", "go", "ruby", "java", "python", "rust", "php", "dotnet"]

PAIRS: list[tuple[str, str]] = []
for _f in CLIENTS:
    PAIRS.append((f"docs/tutorials/application-client/{_f}.md",
                  f"docs/docs/tutorials/application-client/{_f}.md"))
for _f in SERVERS:
    PAIRS.append((f"docs/tutorials/application-server/{_f}.md",
                  f"docs/docs/tutorials/application-server/{_f}.md"))
PAIRS += [
    ("docs/tutorials/advanced-features/index.md",
     "docs/docs/tutorials/advanced-features/index.md"),
    ("docs/tutorials/advanced-features/recording-basic.md",
     "docs/docs/tutorials/advanced-features/recording-basic-s3.md"),
    ("docs/tutorials/advanced-features/recording-advanced.md",
     "docs/docs/tutorials/advanced-features/recording-advanced-s3.md"),
]
for _f in ["android", "angular", "electron", "ionic", "ios", "javascript", "react", "vue"]:
    PAIRS.append((f"shared/application-client/{_f}.md",
                  f"shared/tutorials/application-client/{_f}.md"))
PAIRS.append(("shared/application-client/application-client-tabs.md",
              "shared/tutorials/application-client/tabs.md"))
for _f in ["dotnet", "go", "java", "node", "php", "python", "ruby", "rust"]:
    PAIRS.append((f"shared/application-server/{_f}.md",
                  f"shared/tutorials/application-server/{_f}.md"))
PAIRS.append(("shared/application-server/application-server-tabs.md",
              "shared/tutorials/application-server/tabs.md"))
for _f in ["configure-urls", "testing-other-devices", "webhook-local-server", "run-openvidu-locally"]:
    PAIRS.append((f"shared/{_f}.md", f"shared/tutorials/{_f}.md"))

# Pages whose step 1 differs by design (see note 4): skip that region.
SKIP_STEP1 = {"docs/tutorials/advanced-features/recording-basic.md",
              "docs/tutorials/advanced-features/recording-advanced.md"}
# Trailing button rows that only exist on openvidu.io (see note 6).
DROP_LINE = re.compile(r"recording-(basic|advanced)-azure")

ICON = re.compile(r" ?:fontawesome-solid-external-link:\{\.external-link-icon\}")
TARGET = re.compile(r"\{:?target=\"?\\?_blank\"?\}")
REF = re.compile(r"/(blob|tree)/(?:master|\d+\.\d+\.\d+|[0-9a-f]{40})/")
CLONE = re.compile(r"(git clone https://github\.com/OpenVidu/[a-z-]+(?:\.git)?) -b \d+\.\d+\.\d+")
SNIP = re.compile(r'--8<-- "([^"]+)"')
IMG_ANY = re.compile(r"!\[[^\]]*\]\([^)]+\)|<img\s")
IMG_NAMES = re.compile(r"([\w.-]+\.(?:png|jpg|jpeg|webp|gif|svg))")
WIDTH = re.compile(r"width:\s*(\d+%)")
CONTAINER = '<div class="tutorials-container" markdown>'
WRAPPER = re.compile(r'<div class="grid[^"]*"( markdown)?>|</div>|<p[^>]*>|</p>')
HEADING = re.compile(r"^(#{2,4}) (\d+\. .*)$")
STEP1 = re.compile(r"^### 1\. Run (?:OpenVidu|LiveKit) Server(?: and Egress)?$")
STEP2 = re.compile(r"^### 2\. ")
OVURL = re.compile(r"https://openvidu\.io/latest/docs/([^)\s\"'`]*?)/?(?:\?[^)#\s]*)?(#[^)\s\"'`]*)?(?=[)\s\"'`]|$)")
MDLINK = re.compile(r"\]\((?!https?:|wss:|mailto:|#)([^)\s]+?)\)")
OVDOC_LINK = re.compile(r"\[([^\]]*)\]\((OVDOC:[^)]*)\)")
ACCESS = re.compile(
    r"\[Accessing your (?:app from other devices in your network|local deployment from other "
    r"devices on your network)\]\([^)]*\)")
SERVER_STEP_LINK = re.compile(r"\[(?:LiveKit|OpenVidu) Server\]\(#1-run-(?:livekit|openvidu)-server\)")
AZURE_TAIL = re.compile(r" on openvidu\.io instead\.$")


def canon_snip(path: str) -> str:
    p = re.sub(r"^(tutorials|shared)/", "", path)
    p = re.sub(r"application-(client|server)/(application-\1-)?tabs\.md", r"application-\1/TABS", p)
    if p in ("run-openvidu-server.md", "run-livekit-server.md", "run-livekit-server-and-egress.md"):
        p = "SERVER-STEP"
    return p


def logical(target: str, page_dir: str | None, side: str) -> str:
    """Map a doc link to a token that is the same on both sides."""
    anchor = ""
    if "#" in target:
        target, anchor = target.split("#", 1)
        anchor = "#" + anchor
    if target.endswith(".md"):
        target = target[:-3]
    if target.startswith("/"):
        path = target.lstrip("/")
    else:
        # A snippet's relative links resolve at the include site, which for every
        # tutorial snippet is a page in tutorials/<area>/.
        path = posixpath.normpath(posixpath.join(page_dir or "tutorials/AREA", target))
    if side == "ov" and path.startswith("docs/"):
        path = path[len("docs/"):]
    path = re.sub(r"recording-(basic|advanced)-s3", r"recording-\1", path)
    return "OVDOC:" + path + anchor


def normalize(text: str, side: str, page_dir: str | None, skip_step1: bool) -> list[str]:
    if text.startswith("---\n"):
        text = text.split("\n---\n", 1)[1]
    text = TARGET.sub("", text)
    text = REF.sub(r"/\1/REF/", text)
    text = CLONE.sub(r"\1", text)
    text = re.sub(r"recording-(basic|advanced)-s3", r"recording-\1", text)
    text = re.sub(r"^# (Basic|Advanced) Recording Tutorial S3$", r"# \1 Recording Tutorial",
                  text, flags=re.M)
    text = re.sub(r"\*\*Recording (Basic|Advanced) S3\*\*", r"**Recording \1**", text)
    text = SNIP.sub(lambda m: f'--8<-- "SNIP/{canon_snip(m.group(1))}"', text)
    text = MDLINK.sub(lambda m: "](" + logical(m.group(1), page_dir, side) + ")", text)
    text = OVURL.sub(lambda m: "OVDOC:" + m.group(1).rstrip("/") + (m.group(2) or ""), text)
    # This site links openvidu.io from the outside, so those links carry the
    # external-link icon and openvidu.io's own relative ones do not. Everywhere
    # else the icon is compared.
    text = OVDOC_LINK.sub(lambda m: "[" + ICON.sub("", m.group(1)) + "](" + m.group(2) + ")", text)
    text = ACCESS.sub("[ACCESS-FROM-OTHER-DEVICES]", text)
    text = SERVER_STEP_LINK.sub("[SERVER-STEP]", text)

    out: list[str] = []
    in_step1 = False
    for line in text.split("\n"):
        stripped = HEADING.sub(r"### \2", line.strip())
        if skip_step1:
            if STEP1.match(stripped):
                in_step1 = True
                out.append("### 1. Run SERVER")
                continue
            if in_step1:
                if STEP2.match(stripped):
                    in_step1 = False
                else:
                    continue
        if DROP_LINE.search(line) and "instead" not in line:
            continue
        if stripped.startswith("///"):
            continue
        if WRAPPER.fullmatch(stripped):
            continue
        if IMG_ANY.search(line):
            names = ",".join(sorted(set(IMG_NAMES.findall(line))))
            width = WIDTH.search(line)
            indent = re.match(r"\s*", line).group(0)
            out.append(f"{indent}IMG({names}" + (f",w={width.group(1)}" if width else "") + ")")
            continue
        line = HEADING.sub(r"### \2", line)
        line = STEP1.sub("### 1. Run SERVER", line)
        line = AZURE_TAIL.sub(" instead.", line)
        line = re.sub(r"^(\s*)-\s+", r"\1- ", line)
        line = re.sub(r"^(\s*)(\d+)\.\s+", r"\1\2. ", line)
        out.append(line.rstrip())

    collapsed: list[str] = []
    for line in out:
        if not line and collapsed and not collapsed[-1]:
            continue
        collapsed.append(line)
    while collapsed and not collapsed[-1]:
        collapsed.pop()
    # A button row left empty by DROP_LINE (openvidu.io's Azure recording
    # tutorials) is one of those intentional extras, not a layout difference.
    result: list[str] = []
    for i, line in enumerate(collapsed):
        if line == CONTAINER:
            rest = [l for l in collapsed[i + 1:] if l]
            if not rest or rest[0] == CONTAINER:
                continue
        result.append(line)
    while result and not result[-1]:
        result.pop()
    return result


TITLE_MAX = 45          # Material appends " - LiveKit Tutorials" (20 chars)
DESC_RANGE = (100, 160)


def check_frontmatter(root: pathlib.Path) -> int:
    """Every page needs a unique title and description, within the SERP budgets."""
    problems, seen = [], {}
    pages = sorted((root / "docs").rglob("*.md"))
    for page in pages:
        m = re.match(r"^---\n(.*?)\n---\n", page.read_text(), re.S)
        fm = m.group(1) if m else ""
        rel = page.relative_to(root)
        for key, limits in (("title", (1, TITLE_MAX)), ("description", DESC_RANGE)):
            found = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', fm, re.M)
            if not found:
                problems.append(f"{rel}: no {key}")
                continue
            value = found.group(1)
            low, high = limits
            if not low <= len(value) <= high:
                problems.append(f"{rel}: {key} is {len(value)} chars, wanted {low}-{high}")
            if value in seen.setdefault(key, {}):
                problems.append(f"{rel}: {key} duplicates {seen[key][value]}")
            else:
                seen[key][value] = rel
    for problem in problems:
        print("  " + problem)
    print(f"{len(pages)} pages checked, {len(problems)} problem(s).")
    return 1 if problems else 0


def main() -> int:
    here = pathlib.Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--openvidu-io", type=pathlib.Path, default=here.parent / "openvidu.io",
                    help="path to a checkout of the openvidu.io repo (default: ../openvidu.io)")
    ap.add_argument("--context", type=int, default=0, help="lines of diff context")
    ap.add_argument("--frontmatter", action="store_true",
                    help="instead of the sync diff, check every page's title and description")
    args = ap.parse_args()

    if args.frontmatter:
        return check_frontmatter(here)

    if not args.openvidu_io.is_dir():
        print(f"openvidu.io checkout not found at {args.openvidu_io}", file=sys.stderr)
        return 2

    divergent = 0
    for lk_rel, ov_rel in PAIRS:
        lk_file, ov_file = here / lk_rel, args.openvidu_io / ov_rel
        for f in (lk_file, ov_file):
            if not f.is_file():
                print(f"missing: {f}", file=sys.stderr)
                return 2
        skip = lk_rel in SKIP_STEP1
        lk_dir = None if lk_rel.startswith("shared/") else posixpath.dirname(lk_rel)[len("docs/"):]
        ov_dir = None if ov_rel.startswith("shared/") else posixpath.dirname(ov_rel)[len("docs/"):]
        a = normalize(lk_file.read_text(), "lk", lk_dir, skip)
        b = normalize(ov_file.read_text(), "ov", ov_dir, skip)
        diff = list(difflib.unified_diff(a, b, f"livekit-tutorials {lk_rel}",
                                         f"openvidu.io {ov_rel}", n=args.context, lineterm=""))
        if diff:
            divergent += sum(1 for l in diff if l[:1] in "+-" and l[:3] not in ("+++", "---"))
            print("\n".join(diff) + "\n")

    if divergent:
        print(f"{divergent} unexplained line(s) across {len(PAIRS)} tutorial file pairs.")
        print("Either sync the two repos, or record the difference in DELIBERATE.")
        return 1
    print(f"In sync: {len(PAIRS)} tutorial file pairs, no unexplained differences.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
