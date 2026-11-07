#!/usr/bin/env python3
"""Render index.html and <kid>/index.html from site.json."""
import json, os, html, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
KIDS = [("owen", "Owen", "#ff6b35", "🚀"), ("eli", "Eli", "#2a9d8f", "🦖"), ("kathryn", "Kathryn", "#9b5de5", "🦄"), ("aydan", "Aydan", "#1e407c", "")]
MATURE = {"aydan"}  # college-level: plain styling, no stars/reward/reporting scripts
SUBJ = {"math": "#f4a261", "spelling": "#4cc9f0", "chemistry": "#1e407c"}
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
def stars_widget(k, n):
    """Star total + next prize for kids listed in prizes.json (total read from this device's localStorage '<kid>-stars')."""
    try: pr = json.load(open(os.path.join(ROOT, "prizes.json"))).get(k) or []
    except FileNotFoundError: pr = []
    if not pr: return ""
    # surprise prizes: the schedule (prize names / thresholds) is NOT shown or embedded here
    return (f'<div class="card" id="stars" style="--c:#ffd23f;text-align:center"><div style="font-size:2rem;font-weight:800">⭐ <span id="starTotal">0</span> stars</div>'
            f'<div id="starNext" style="font-size:1.2rem"></div><div style="color:#888;font-size:.85rem;margin-top:6px">Stars are saved on this device.</div></div>'
            f'<script>(function(){{var d={{}};try{{d=JSON.parse(localStorage.getItem("{k}-stars")||"null")||{{}};}}catch(e){{}}'
            f'var t=d.total||0,days=d.days||[],n=0,x=new Date(),f=function(x){{return x.getFullYear()+"-"+("0"+(x.getMonth()+1)).slice(-2)+"-"+("0"+x.getDate()).slice(-2);}};'
            f'if(days.indexOf(f(x))<0)x.setDate(x.getDate()-1);while(days.indexOf(f(x))>=0){{n++;x.setDate(x.getDate()-1);}}'
            f'document.getElementById("starTotal").textContent=t;'
            f'document.getElementById("starNext").textContent=(n>1?"🔥 "+n+" days in a row! ":"")+"Keep practicing. Surprises happen when you keep trying! 🎁";}})();</script>')
def learn_js(n):
    """report.js (Learn: #key= saving + parent-granted reward pop-up) with the live reporting config, like the practice pages."""
    import sys, contextlib, io
    sys.path.insert(0, "/workspace/practice/src")
    try:
        import build_common
        with contextlib.redirect_stdout(io.StringIO()):
            js = build_common.report_js("/workspace/practice/reporting/config.json")
    except Exception as e:
        print("  (no reward script on index pages:", e, ")"); return ""
    return f'<script>{js}</script><script>try{{Learn.init({{kid:{json.dumps(n)},page:"index",index:true}},__report.cfg,__report.testEnv);}}catch(e){{}}</script>'
MCSS = """*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif;background:#f6f7f9;color:#1d2433;line-height:1.5}
header{background:#1e407c;color:#fff;padding:16px 18px}header a{color:#cfe0ff;text-decoration:none}header h1{font-family:Georgia,serif;font-weight:600;margin:4px 0 0;font-size:1.6rem}
main{max-width:760px;margin:0 auto;padding:18px 14px 48px}.it{background:#fff;border:1px solid #d9dee7;border-radius:10px;padding:16px 18px;margin:0 0 14px}
.it h2{font-family:Georgia,serif;font-weight:600;font-size:1.2rem;margin:4px 0}.sub{font-size:.8rem;font-weight:700;letter-spacing:.4px;text-transform:uppercase;color:#1e407c}
.date{color:#5b6475;margin:0 0 10px;font-size:.95rem}.b{display:inline-block;padding:10px 16px;border-radius:7px;background:#1e407c;color:#fff;text-decoration:none;font-weight:600;margin:0 8px 6px 0;min-height:44px}
.b.s{background:#fff;color:#1e407c;border:1px solid #1e407c}.note{color:#5b6475;font-size:.88rem}"""
def mature_index(k, n, c, items):
    items = sorted(items, key=lambda x: x["date"], reverse=True)
    body = ""
    for it in items:
        o = f'<a class="b" href="{html.escape(it["html"])}">Open</a>' if it.get("html") else ""
        p = f'<a class="b s" href="{html.escape(it["pdf"])}">Printable PDF</a>' if it.get("pdf") else ""
        body += f'<div class="it"><div class="sub">{html.escape(it["subject"])}</div><h2>{html.escape(it["title"])}</h2><p class="date">{fmt(it["date"])}</p>{o}{p}</div>'
    if not items: body = "<p>Nothing here yet.</p>"
    body += '<p class="note">Progress is saved in this browser only.</p>'
    ping = ""
    if k == "aydan":
        try:
            import sys
            sys.path.insert(0, "/workspace/practice/src")
            import build_common
            ping = "<script>" + build_common.open_ping_js("/workspace/practice/reporting/config.json", {
                "kid": "Aydan", "topic": "aydan-hub", "title": "Aydan's study hub",
                "subject": "Chemistry", "page": "Aydan's study hub"}) + "</script>"
        except Exception as e:
            print("  (no open-ping on aydan hub:", e, ")")
    os.makedirs(os.path.join(ROOT, k), exist_ok=True)
    open(os.path.join(ROOT, k, "index.html"), "w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{html.escape(n)} — study hub</title>
<style>{MCSS}</style></head><body><header><a href="../">← Home</a><h1>{html.escape(n)}’s study hub</h1></header><main>{body}</main>{ping}</body></html>\n""")
def fmt(d):
    return datetime.date.fromisoformat(d).strftime("%a, %b %-d, %Y")
def main():
    data = json.load(open(os.path.join(ROOT, "site.json")))
    btns = "".join(f'<a class="kid" style="background:{c}" href="{k}/">{(e + " ") if e else ""}{n}</a>' for k, n, c, e in KIDS)
    open(os.path.join(ROOT, "index.html"), "w").write(page("Practice", f'<h1>Who\'s practicing? 📚</h1><div class="kids">{btns}</div>'))
    for k, n, c, e in KIDS:
        if k in MATURE:
            mature_index(k, n, c, data.get(k, [])); continue
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
        open(os.path.join(ROOT, k, "index.html"), "w").write(page(f"{n}'s practice", f'<a class="home" href="../">← Home</a><h1>{e} {n}\'s practice</h1>{stars_widget(k, n)}{cards}{learn_js(n)}'))
    print("built")
main()
