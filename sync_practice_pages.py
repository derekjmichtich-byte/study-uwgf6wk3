#!/usr/bin/env python3
"""Re-copy the rebuilt practice pages into the site under their EXISTING slugs (same scrubbing as add_item.py:
emails removed, noindex added, private-string check). site.json entries (title/date/pdf) are left untouched.
  ./sync_practice_pages.py            # copy all mapped pages
  ./sync_practice_pages.py --check    # only report which site pages differ"""
import os, sys, filecmp, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from add_item import scrub_html, ROOT
PAGES = [  # (source html, site path)
    ("/workspace/practice/Eli_SimpleSolutions_Test5_Practice.html", "eli/test-5-lessons-17-20.html"),
    ("/workspace/practice/Eli_Spelling_ShortO_LongO.html",          "eli/spelling-short-o-long-o.html"),
    ("/workspace/practice/Eli_Spelling_U_Yoo_Oo.html",              "eli/spelling-u-yoo-oo.html"),
    ("/workspace/practice/Eli_Spelling_Vowel_Sounds_oo.html",       "eli/spelling-vowel-sounds-oo.html"),
    ("/workspace/practice/Eli_Multiplication_Facts.html",           "eli/multiplication-facts.html"),
    ("/workspace/practice/Kathryn_Spelling_Practice.html",          "kathryn/silent-e-words.html"),
    ("/workspace/practice/Kathryn_WordList4_Spelling.html",         "kathryn/word-list-4.html"),
    ("/workspace/practice/Kathryn_WordList5_Spelling.html",         "kathryn/spelling-word-list-5.html"),
    ("/workspace/practice/Kathryn_Math_Quiz2_3.html",              "kathryn/math-quiz-2-3.html"),
    ("/workspace/practice/Eli_Math_Quiz5_Review.html",             "eli/math-quiz-5.html"),
    ("/workspace/practice/Eli_Number_Bonds_2x1.html",              "eli/number-bonds-2-digit-x-1-digit.html"),
    ("/workspace/owen-lesson27/Owen_Lesson27_Practice.html",        "owen/lesson-27.html"),
    ("/workspace/eli-eng28/Eli_English_Lessons28_31_Practice.html", "eli/english-test-review-lessons-28-31.html"),
    # weekly extra practice (built by practice/src/build.py from extra_practice.html + xp_<week>_<kid>.json)
    ("/workspace/practice/Owen_Extra_Practice_2026-10-17.html",     "owen/extra-practice-2026-10-17.html"),
    ("/workspace/practice/Eli_Extra_Practice_2026-10-17.html",      "eli/extra-practice-2026-10-17.html"),
    ("/workspace/practice/Kathryn_Extra_Practice_2026-10-17.html",  "kathryn/extra-practice-2026-10-17.html"),
    ("/workspace/practice/Owen_Extra_Practice_2026-10-24.html",     "owen/extra-practice-2026-10-24.html"),
    ("/workspace/practice/Eli_Extra_Practice_2026-10-24.html",      "eli/extra-practice-2026-10-24.html"),
    ("/workspace/practice/Kathryn_Extra_Practice_2026-10-24.html",  "kathryn/extra-practice-2026-10-24.html"),
    ("/workspace/practice/wip/owen/lesson-27-quest.html",          "owen/lesson-27-quest.html"),
]
check = "--check" in sys.argv
for src, rel in PAGES:
    dst = os.path.join(ROOT, rel)
    assert os.path.exists(dst), f"{rel} is not in the site yet (use add_item.py for new pages)"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
    scrub_html(src, tmp)
    same = filecmp.cmp(tmp, dst, shallow=False)
    if check: print(("same    " if same else "DIFFERS ") + rel); os.unlink(tmp); continue
    os.replace(tmp, dst); os.chmod(dst, 0o644)
    print(("unchanged " if same else "updated   ") + rel)
