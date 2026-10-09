#!/usr/bin/env python3
"""Copy a practice HTML + PDF into the site (scrubbed) and register it in site.json."""
import argparse, json, os, re, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
_TF = os.path.join(ROOT, ".private_terms")  # local-only, gitignored list of strings that must never be published
FORBIDDEN = [l.strip().lower() for l in open(_TF) if l.strip()] if os.path.exists(_TF) else []
ROBOTS = '<meta name="robots" content="noindex,nofollow">'

def kebab(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def scrub_html(src, dst):
    t = open(src, encoding="utf-8").read()
    t = re.sub(r'("to"\s*:\s*)"[^"]*"', r'\1""', t)
    t = re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', '', t)
    if 'name="robots"' not in t:
        t = re.sub(r'(<head[^>]*>)', r'\1\n' + ROBOTS, t, count=1, flags=re.I)
    bad = [f for f in FORBIDDEN if f in t.lower()]
    if bad:
        sys.exit(f"REFUSED {src}: contains {bad}")
    open(dst, "w", encoding="utf-8").write(t)

def check_pdf(src):
    txt = subprocess.run(["pdftotext", src, "-"], capture_output=True, text=True).stdout
    txt += subprocess.run(["pdfinfo", src], capture_output=True, text=True).stdout
    bad = [f for f in FORBIDDEN if f in txt.lower()]
    if bad:
        sys.exit(f"REFUSED {src}: contains {bad} (excluded, not edited)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kid", required=True, choices=["owen", "eli", "kathryn"])
    ap.add_argument("--title", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--html"); ap.add_argument("--pdf")
    ap.add_argument("--slug", help="kebab-case base filename (default: from title)")
    a = ap.parse_args()
    slug = kebab(a.slug or a.title)
    d = os.path.join(ROOT, a.kid); os.makedirs(d, exist_ok=True)
    item = {"title": a.title, "subject": a.subject, "date": a.date, "html": None, "pdf": None}
    if a.pdf:
        check_pdf(a.pdf)
    if a.html:
        scrub_html(a.html, os.path.join(d, slug + ".html")); item["html"] = slug + ".html"
    if a.pdf:
        shutil.copyfile(a.pdf, os.path.join(d, slug + ".pdf")); item["pdf"] = slug + ".pdf"
    p = os.path.join(ROOT, "site.json")
    data = json.load(open(p)) if os.path.exists(p) else {"owen": [], "eli": [], "kathryn": []}
    lst = data.setdefault(a.kid, [])
    lst[:] = [x for x in lst if not (x["html"] == item["html"] and x["pdf"] == item["pdf"])]
    lst.append(item)
    json.dump(data, open(p, "w"), indent=2); open(p, "a").write("\n")
    print(f"added {a.kid}/{slug}")
main()
