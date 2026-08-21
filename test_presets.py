"""Tests for daily-intelligence presets module."""

import unittest
import presets


class PresetsTests(unittest.TestCase):
    def test_all_feeds_are_valid_https_urls(self) -> None:
        for jx, group in presets.JURISDICTION_FEEDS.items():
            for group_name, urls in group.items():
                self.assertTrue(urls, f"Empty feed list for {jx} -> {group_name}")
                for u in urls:
                    self.assertTrue(u.startswith("https://") or u.startswith("http://"), f"Invalid URL {u} in {jx}")

        for topic, pack in presets.TOPIC_PACKS.items():
            for u in pack.get("feeds", []):
                self.assertTrue(u.startswith("https://") or u.startswith("http://"), f"Invalid URL {u} in {topic}")

    def test_assemble_australia_profile(self) -> None:
        profile = {
            "who": "Australian tax accountant",
            "jurisdictions": ["AU"],
            "topics": ["Payroll", "AI in accounting practice"],
            "watch_for": "Payday Super",
        }
        context, sections, queries, feeds, fallbacks = presets.assemble(profile)
        self.assertIn("Australia profession & tax", feeds)
        self.assertIn("Payroll", sections)
        self.assertIn("AI in accounting practice", sections)
        self.assertIn("Worth knowing", sections)
        self.assertTrue(any("Payday Super" in q for q in queries))
        self.assertIn("AU", context)

    def test_assemble_multi_jurisdiction(self) -> None:
        profile = {
            "who": "Cross-border specialist",
            "jurisdictions": ["US", "CA", "DE", "SG"],
            "topics": ["VAT & e-invoicing"],
        }
        context, sections, queries, feeds, fallbacks = presets.assemble(profile)
        self.assertIn("Canada profession & tax", feeds)
        self.assertIn("Germany profession & tax", feeds)
        self.assertIn("Singapore profession & tax", feeds)
        self.assertIn("US profession & tax", feeds)


if __name__ == "__main__":
    unittest.main()
