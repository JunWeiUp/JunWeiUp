#!/usr/bin/env python3
"""Check project icons and generated bilingual profile cards."""
import base64
import unittest
import xml.etree.ElementTree as ET

from build_assets import ASSETS, COPY, PROJECT_ICONS, THEMES, project

SVG = "{http://www.w3.org/2000/svg}"


class ProjectCardTests(unittest.TestCase):
    def test_all_cards_embed_their_local_icon(self):
        for locale, copy in COPY.items():
            for theme_name, theme in THEMES.items():
                for key, data in copy["projects"].items():
                    with self.subTest(locale=locale, theme=theme_name, project=key):
                        root = ET.fromstring(project(theme, key, data))
                        images = root.findall(f".//{SVG}image")
                        self.assertEqual(len(images), 1)
                        image = images[0]
                        self.assertEqual(
                            {attr: image.get(attr) for attr in ("x", "y", "width", "height")},
                            dict(x="400", y="40", width="56", height="56"),
                        )
                        self.assertEqual(image.get("clip-path"), f"url(#{key}-icon-mask)")
                        mask = root.find(f'.//{SVG}clipPath[@id="{key}-icon-mask"]/{SVG}rect')
                        self.assertIsNotNone(mask)
                        self.assertEqual(mask.get("rx"), "10")
                        prefix, encoded = image.get("href", "").split(",", 1)
                        self.assertEqual(prefix, "data:image/png;base64")
                        embedded = base64.b64decode(encoded, validate=True)
                        self.assertTrue(embedded.startswith(b"\x89PNG\r\n\x1a\n"))
                        self.assertTrue(embedded == (ASSETS / PROJECT_ICONS[key]).read_bytes())

    def test_generated_cards_match_source(self):
        for locale, copy in COPY.items():
            suffix = "" if locale == "en" else f"-{locale}"
            for theme_name, theme in THEMES.items():
                for key, data in copy["projects"].items():
                    with self.subTest(locale=locale, theme=theme_name, project=key):
                        path = ASSETS / f"{key}{suffix}-{theme_name}.svg"
                        self.assertTrue(
                            path.read_text() == project(theme, key, data),
                            f"Rebuild {path.name} with scripts/build_assets.py",
                        )


if __name__ == "__main__":
    unittest.main()
