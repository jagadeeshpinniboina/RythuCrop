import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.data.translations import TRANSLATIONS, LANGUAGES, LOCALIZED_CROP_NAMES


def test_multilingual_parity():
    print("=" * 80)
    print("VERIFYING 9-LANGUAGE TRANSLATION PARITY (100% KEY COVERAGE)")
    print("=" * 80)

    en_keys = set(TRANSLATIONS["en"].keys())
    print(f"Total English UI Keys: {len(en_keys)}")

    all_passed = True
    for lang in LANGUAGES:
        if lang == "en":
            continue

        lang_keys = set(TRANSLATIONS[lang].keys())
        missing = en_keys - lang_keys
        extra = lang_keys - en_keys

        if missing:
            print(f"[FAIL] {lang.upper()} is missing {len(missing)} keys: {missing}")
            all_passed = False
        else:
            print(f"[PASS] {lang.upper()}: 100% key parity ({len(lang_keys)}/{len(en_keys)} keys present)")

    print("\nVERIFYING CROP NAME COVERAGE ACROSS ALL 9 LANGUAGES:")
    for crop_id, names in LOCALIZED_CROP_NAMES.items():
        missing_langs = [l for l in LANGUAGES if l not in names or not names[l]]
        if missing_langs:
            print(f"[FAIL] Crop '{crop_id}' missing in languages: {missing_langs}")
            all_passed = False
        else:
            print(f"[PASS] Crop '{crop_id}': translated in all 9 languages")

    print("=" * 80)
    if all_passed:
        print("ALL MULTILINGUAL PARITY CHECKS PASSED SUCCESSFULLY!")
    else:
        print("SOME MULTILINGUAL CHECKS FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    test_multilingual_parity()
