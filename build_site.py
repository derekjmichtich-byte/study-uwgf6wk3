#!/usr/bin/env python3
"""Render index.html and <kid>/index.html from site.json."""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
KIDS = [("owen", "Owen", "#ff6b35", "🚀"), ("eli", "Eli", "#2a9d8f", "🦖"), ("kathryn", "Kathryn", "#9b5de5", "🦄")]
SUBJ = {"math": "#f4a261", "spelling": "#4cc9f0"}
CSS = """*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#fffaf0;color:#222}
main{max-width:720px;margin:0 auto;padding:20px 16px 48px}h1{font-size:2.2rem;text-align:center;margin:12px 0 24px}
.kids{display:grid;gap:18px}.kid{display:block;padding:34px 20px;border-radius:24px;color:#fff;text-decoration:none;font-size:2.4rem;font-weight:800;text-align:center;box-shadow:0 6px 0 rgba(0,0,0,.2)}
.kid:active{transform:translateY(4px);box-shadow:0 2px 0 rgba(0,0,0,.2)}
.card{background:#fff;border-radius:20px;padding:18px;margin:0 0 18px;box-shadow:0 3px 10px rgba(0,0,0,.08);border-left:10px solid var(--c)}
.tag{display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-weight:700;font-size:.9rem}
.card h2{margin:10px 0 4px;font-size:1.5rem}.date{color:#666;margin:0 0 14px}
.btn{display:block;text-align:center;padding:18px;border-radius:16px;background:var(--c);color:#fff;font-size:1.4rem;font-weight:800;text-decoration:none;min-height:56px}
.pdf{display:inline-block;margin-top:12px;padding:10px 4px;font-size:1.1rem;color:#333}
.home{display:inline-block;padding:12px 6px;font-size:1.1rem;color:#333;text-decoration:none}"""
def page(title, body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body><main>{body}</main></body></html>\n"""
def fmt(d):
    return datetime.date.fromisoformat(d).strftime("%a, %b %-d, %Y")
def main():
    data = json.load(open(os.path.join(ROOT, "site.json")))
    btns = "".join(f'<a class="kid" style="background:{c}" href="{k}/">{e} {n}</a>' for k, n, c, e in KIDS)
    open(os.path.join(ROOT, "index.html"), "w").write(page("Practice", f'<h1>Who\'s practicing? 📚</h1><div class="kids">{btns}</div>'))
    for k, n, c, e in KIDS:
        items = sorted(data.get(k, []), key=lambda x: x["date"], reverse=True)
        cards = ""
        for it in items:
            sc = SUBJ.get(it["subject"].lower(), "#888")
            pr = f'<a class="btn" href="{html.escape(it["html"])}">▶ Practice</a>' if it.get("html") else ""
            pdf = f'<a class="pdf" href="{html.escape(it["pdf"])}">🖨️ Printable (PDF)</a>' if it.get("pdf") else ""
            cards += (f'<div class="card" style="--c:{c}"><span class="tag" style="background:{sc}">{html.escape(it["subject"])}</span>'
                      f'<h2>{html.escape(it["title"])}</h2><p class="date">{fmt(it["date"])}</p>{pr}{pdf}</div>')
        if not items: cards = "<p>Nothing here yet!</p>"
        os.makedirs(os.path.join(ROOT, k), exist_ok=True)
        open(os.path.join(ROOT, k, "index.html"), "w").write(page(f"{n}'s practice", f'<a class="home" href="../">← Home</a><h1>{e} {n}\'s practice</h1>{cards}'))
    print("built")
main()
