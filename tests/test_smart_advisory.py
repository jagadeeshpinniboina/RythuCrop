import sys
import os
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RYTHUCROP_DEV_AUTH"] = "true"

import unittest
from app import app
from app.data.translations import TRANSLATIONS, LANGUAGES


class TestSmartAdvisoryModule(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        index_path = Path(__file__).resolve().parent.parent / "app" / "templates" / "index.html"
        with open(index_path, "r", encoding="utf-8") as f:
            self.index_html = f.read()

        advisory_js_path = Path(__file__).resolve().parent.parent / "app" / "static" / "js" / "advisory.js"
        with open(advisory_js_path, "r", encoding="utf-8") as f:
            self.advisory_js = f.read()

    def test_ui_markup_architecture(self):
        """Verify Call-to-action button, selectors, and container structure."""
        # 1. Prominent CTA Button
        self.assertIn('id="btnFetchAdvisory"', self.index_html)
        self.assertIn('data-i18n="advisory_get_btn"', self.index_html)
        self.assertIn('Get Cultivation Advisory', self.index_html)

        # 2. Crop selector ID
        self.assertIn('id="advisoryCropSelect"', self.index_html)

        # 3. Priority selector with 3 options
        self.assertIn('id="adPriority"', self.index_html)
        self.assertNotIn('data-i18n-option="advisory_focus_all"', self.index_html)
        self.assertIn('data-i18n-option="advisory_focus_care"', self.index_html)
        self.assertIn('data-i18n-option="advisory_focus_fert"', self.index_html)
        self.assertIn('data-i18n-option="advisory_focus_pest"', self.index_html)

        # 4. Result container hidden initially
        self.assertIn('id="advisoryResult"', self.index_html)
        self.assertIn('style="display:none;', self.index_html)
        self.assertIn('id="advisoryContainer"', self.index_html)

        # 5. JS scripts included
        self.assertIn('/static/js/advisory.js', self.index_html)
        self.assertIn('/static/js/advisory_translations.js', self.index_html)

    def test_advisory_js_engine_structure(self):
        """Verify advisory.js defines 3-card layout, priority filtering, and auto-render."""
        self.assertIn("window.renderAdvisory = renderAdvisory", self.advisory_js)
        self.assertIn("advisoryCropSelect", self.advisory_js)
        self.assertIn("btnFetchAdvisory", self.advisory_js)

        # 3 Cards rendering
        self.assertIn("CARD 1: AGRONOMIC GROWTH STAGES", self.advisory_js)
        self.assertIn("CARD 2: TARGETED NUTRIENT & FERTILIZER SCHEDULE", self.advisory_js)
        self.assertIn("CARD 3: PEST & DISEASE IPM SHIELD", self.advisory_js)

        # Priority filtering logic
        self.assertIn('priority === "care"', self.advisory_js)
        self.assertIn('priority === "fertilizer"', self.advisory_js)
        self.assertIn('priority === "pest"', self.advisory_js)

    def test_multilingual_key_presence_for_advisory(self):
        """Verify all advisory translation keys are 100% present and non-empty across all languages."""
        required_keys = [
            "advisory_get_btn",
            "advisory_focus_all",
            "advisory_focus_care",
            "advisory_focus_fert",
            "advisory_focus_pest",
            "card_care_title",
            "card_fert_title",
            "card_pest_title",
            "advisory_card1_title",
            "advisory_card2_title",
            "advisory_card3_title",
            "advisory_active_focus"
        ]

        for lang in LANGUAGES:
            dict_lang = TRANSLATIONS.get(lang, {})
            for key in required_keys:
                self.assertIn(key, dict_lang, f"Key '{key}' missing in language '{lang}'")
                self.assertTrue(dict_lang[key], f"Key '{key}' is empty in language '{lang}'")


if __name__ == "__main__":
    unittest.main()
