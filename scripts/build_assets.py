#!/usr/bin/env python3
"""Build bilingual profile SVGs from project capabilities and local copy."""
import argparse
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

THEMES = {
    "light": dict(bg="#ffffff", line="#d8e1ed", ink="#18273d", muted="#536880", accent="#1667d9", soft="#edf4ff", green="#087b69"),
    "dark": dict(bg="#0d1117", line="#303c4d", ink="#e6edf3", muted="#a0aec0", accent="#79adff", soft="#142640", green="#72d5bf"),
}

COPY = {
    "en": {
        "greeting": "Hello, I'm Kim.",
        "tagline": "I build tools for everyday work.",
        "platforms": "macOS   /   MOBILE   /   WEB",
        "capabilities_title": "What I build",
        "capabilities": (
            ("Native tools", "Clipboard · screenshots · OCR"),
            ("Connected apps", "Local sync · Mac + Android"),
            ("Web apps", "Interfaces · everyday utilities"),
        ),
        "capabilities_alt": "What I build: native productivity tools, apps with local sync across devices, and practical web applications.",
        "toolbox_title": "Build across platforms",
        "mobile": "Mobile",
        "toolbox_alt": "macOS: Swift and AppKit. Mobile: Flutter and Dart. Web: React and TypeScript.",
        "projects": {
            "clipy": ("01 / NATIVE PRODUCTIVITY", "Clipy", "Clipboard, screenshots & local sync.", "A native Mac app, connected to Android.", "Swift · AppKit · Flutter"),
            "vault": ("02 / PERSONAL UTILITIES", "Password Vault", "Passwords, TOTP & local vaults.", "A Flutter app with WebDAV backup.", "Releases & installation"),
        },
    },
    "zh-CN": {
        "greeting": "你好，我是 Kim。",
        "tagline": "为日常工作，打造顺手的工具。",
        "platforms": "macOS   /   移动端   /   WEB",
        "capabilities_title": "我能做什么",
        "capabilities": (
            ("原生效率工具", "剪贴板 · 截图 · 文字识别"),
            ("跨设备协作", "局域网同步 · 移动端体验"),
            ("Web 应用", "交互界面 · 实用工具"),
        ),
        "capabilities_alt": "我能做什么：原生效率工具、支持局域网同步的跨设备应用，以及实用的 Web 应用。",
        "toolbox_title": "跨平台开发",
        "mobile": "移动端",
        "toolbox_alt": "macOS：Swift 与 AppKit。移动端：Flutter 与 Dart。Web：React 与 TypeScript。",
        "projects": {
            "clipy": ("01 / 原生效率工具", "Clipy", "剪贴板、截图与局域网同步。", "原生 Mac 应用，连接 Android 设备。", "Swift · AppKit · Flutter"),
            "vault": ("02 / 日常实用工具", "Password Vault", "密码、TOTP 双重认证与本地保管库。", "基于 Flutter，支持 WebDAV 备份。", "发布与安装"),
        },
    },
}


def text(x, y, value, size, fill, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>'


def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title>
<g font-family="Avenir Next, DejaVu Sans, PingFang SC, Noto Sans CJK SC, Microsoft YaHei, sans-serif">{body}</g>
</svg>\n'''


def panel(t, width, height):
    return f'<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>'


def header(t, copy):
    body = text(500, 34, "JUNWEIUP", 13, t["muted"], 600, "middle", 'letter-spacing="5"')
    body += text(500, 108, copy["greeting"], 62, t["accent"], 700, "middle")
    body += text(500, 150, copy["tagline"], 23, t["ink"], 500, "middle")
    body += text(500, 190, copy["platforms"], 12, t["muted"], 500, "middle", 'letter-spacing="2"')
    body += f'<path d="M780 96 L809 67 M786 67 H809 V90" fill="none" stroke="{t["green"]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    return svg(1000, 218, f'JunWeiUp — {copy["greeting"]} {copy["tagline"]}', body)


def capabilities(t, copy):
    body = panel(t, 480, 174) + text(24, 33, copy["capabilities_title"], 19, t["ink"], 650)
    for y, (label, detail) in zip((70, 105, 140), copy["capabilities"]):
        body += f'<path d="M25 {y-5} L29 {y-1} L36 {y-9}" fill="none" stroke="{t["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        body += text(45, y, label, 15, t["ink"], 550)
        body += text(188, y, detail, 13, t["muted"])
    return svg(480, 174, copy["capabilities_alt"], body)


def toolbox(t, copy):
    body = panel(t, 480, 174) + text(24, 33, copy["toolbox_title"], 19, t["ink"], 650)
    for y, platform, stack in [(70, "macOS", "Swift / AppKit"), (105, copy["mobile"], "Flutter / Dart"), (140, "Web", "React / TypeScript")]:
        body += f'<circle cx="29" cy="{y-5}" r="4" fill="{t["green"]}"/>'
        body += text(45, y, platform, 15, t["muted"], 500)
        body += text(160, y, stack, 16, t["ink"], 550)
    return svg(480, 174, copy["toolbox_alt"], body)


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
    parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    count = 0
    for locale, copy in COPY.items():
        suffix = "" if locale == "en" else f"-{locale}"
        for name, theme in THEMES.items():
            files = {"header": header(theme, copy), "capabilities": capabilities(theme, copy), "toolbox": toolbox(theme, copy)}
            files.update({key: project(theme, value) for key, value in copy["projects"].items()})
            for key, value in files.items():
                (ASSETS / f"{key}{suffix}-{name}.svg").write_text(value)
                count += 1
    print(f"Built {count} SVG assets across {len(COPY)} languages.")


if __name__ == "__main__":
    main()
