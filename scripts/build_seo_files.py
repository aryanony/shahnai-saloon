import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG

SITE = CFG["siteUrl"].rstrip("/")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ROUTES = [
    ("/", "1.0"),
    ("/bridal-makeup-patna/", "0.9"),
    ("/unisex-salon-patna/", "0.8"),
    ("/shahnai-unisex-salon-patna/", "0.8"),
    ("/services/", "0.8"),
    ("/book/", "0.9"),
    ("/gallery/", "0.6"),
    ("/about/", "0.6"),
    ("/contact/", "0.6"),
    ("/faq/", "0.5"),
    ("/privacy-policy/", "0.2"),
    ("/terms/", "0.2"),
]

urls = "\n".join(f"  <url><loc>{SITE}{path}</loc><priority>{p}</priority></url>" for path, p in ROUTES)
xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(xml)
print("wrote sitemap.xml with", len(ROUTES), "routes")

# Sanity check: every route in the sitemap must have a real index.html on disk.
missing = [p for p, _ in ROUTES if p != "/" and not os.path.isfile(os.path.join(ROOT, p.strip("/"), "index.html"))]
if not os.path.isfile(os.path.join(ROOT, "index.html")):
    missing.append("/")
if missing:
    raise SystemExit("sitemap references pages that do not exist: " + ", ".join(missing))
print("all sitemap routes verified on disk")
