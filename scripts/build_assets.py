#!/usr/bin/env python3
"""Build self-contained profile SVGs. --refresh fetches public GitHub data only."""
import argparse
import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "profile-data.json"
ASSETS = ROOT / "assets"
USER = "JunWeiUp"

THEMES = {
    "light": dict(bg="#ffffff", line="#d8e1ed", ink="#18273d", muted="#536880", accent="#1667d9", soft="#edf4ff", green="#087b69"),
    "dark": dict(bg="#0d1117", line="#303c4d", ink="#e6edf3", muted="#a0aec0", accent="#79adff", soft="#142640", green="#72d5bf"),
}


def refresh():
    # This public endpoint deliberately excludes private repositories.
    repos = []
    for page in range(1, 100):
        req = Request(f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100&page={page}", headers={"User-Agent": "JunWeiUp-profile", "Accept": "application/vnd.github+json"})
        with urlopen(req, timeout=30) as response:
            batch = json.load(response)
        if not isinstance(batch, list):
            raise ValueError("Expected a GitHub repository list")
        repos.extend(r for r in batch if not r.get("private", True))
        if len(batch) < 100:
            break
    else:
        raise RuntimeError("Repository pagination limit reached; snapshot was not changed")
    non_forks = [r for r in repos if not r["fork"]]
    data = {
        "as_of": datetime.now(timezone.utc).date().isoformat(),
        "public_repositories": len(repos),
        "non_fork_repositories": len(non_forks),
        "stars_on_public_non_fork_repositories": sum(r["stargazers_count"] for r in non_forks),
    }
    DATA.write_text(json.dumps(data, indent=2) + "\n")


def text(x, y, value, size, fill, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>'


def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title>
<g font-family="Avenir Next, DejaVu Sans, sans-serif">{body}</g>
</svg>\n'''


def panel(t, width, height):
    return f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>'


def header(t):
    body = text(500, 34, "JUNWEIUP", 13, t["muted"], 600, "middle", 'letter-spacing="5"')
    body += text(500, 108, "Hello, I'm Kim.", 62, t["accent"], 700, "middle")
    body += text(500, 150, "I build tools for everyday work.", 23, t["ink"], 500, "middle")
    body += text(500, 190, "macOS   /   MOBILE   /   WEB", 12, t["muted"], 500, "middle", 'letter-spacing="2"')
    body += f'<path d="M780 96 L809 67 M786 67 H809 V90" fill="none" stroke="{t["green"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(1000, 218, "JunWeiUp — Hello, I'm Kim. I build tools for everyday work.", body)


def stats(t, data):
    body = panel(t, 480, 174)
    body += text(24, 33, "Public GitHub", 19, t["ink"], 650)
    cols = [(24, data["public_repositories"], "Public repos"), (178, data["non_fork_repositories"], "Non-fork repos"), (348, data["stars_on_public_non_fork_repositories"], "Stars*")]
    for x, count, label in cols:
        body += text(x, 88, count, 34, t["accent"], 650)
        body += text(x, 112, label, 13, t["muted"])
    body += text(24, 151, f'* Public non-fork repos · Snapshot {data["as_of"]}', 11, t["muted"])
    return svg(480, 174, "Public GitHub repository snapshot", body)


def toolbox(t):
    body = panel(t, 480, 174) + text(24, 33, "Build across platforms", 19, t["ink"], 650)
    for y, platform, stack in [(70, "macOS", "Swift / AppKit"), (105, "Mobile", "Flutter / Dart"), (140, "Web", "React / TypeScript")]:
        body += f'<circle cx="29" cy="{y-5}" r="4" fill="{t["green"]}"/>'
        body += text(45, y, platform, 15, t["muted"], 500)
        body += text(160, y, stack, 16, t["ink"], 550)
    return svg(480, 174, "macOS: Swift and AppKit. Mobile: Flutter and Dart. Web: React and TypeScript.", body)


PROJECTS = {
    "clipy": ("01 / NATIVE PRODUCTIVITY", "Clipy", "Clipboard, screenshots & local sync.", "A native Mac app, connected to Android.", "Swift · AppKit · Flutter"),
    "vault": ("02 / PERSONAL UTILITIES", "Password Vault", "Passwords, TOTP & local vaults.", "A Flutter app with WebDAV backup.", "Releases & installation"),
    "grammar": ("03 / LEARNING ON THE WEB", "grammarPath", "English grammar, one lesson at a time.", "Learning paths & interactive practice.", "React · TypeScript"),
    "explore": ("04 / KEEP EXPLORING", "More on GitHub", "Small tools, experiments & open source.", "Explore the projects behind the profile.", "Browse repositories"),
}


def project(t, data):
    label, name, first, second, stack = data
    body = panel(t, 480, 192)
    body += text(24, 30, label, 10, t["muted"], 600, extra='letter-spacing="1.2"')
    body += text(24, 72, name, 28, t["accent"], 650)
    body += text(24, 106, first, 16, t["ink"])
    body += text(24, 132, second, 15, t["muted"])
    body += f'<line x1="24" x2="456" y1="150" y2="150" stroke="{t["line"]}"/>'
    body += text(24, 174, stack, 12, t["muted"], 500)
    body += f'<path d="M435 174 L446 163 M435 163 H446 V174" fill="none" stroke="{t["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(480, 192, f"{name}: {first} {second}", body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.refresh:
        refresh()
    data = json.loads(DATA.read_text())
    ASSETS.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        files = {"header": header(theme), "stats": stats(theme, data), "toolbox": toolbox(theme)}
        files.update({key: project(theme, value) for key, value in PROJECTS.items()})
        for key, value in files.items():
            (ASSETS / f"{key}-{name}.svg").write_text(value)
    print(f"Built 14 SVG assets. Public data snapshot: {data['as_of']}")


if __name__ == "__main__":
    main()
