import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG

SITE = CFG["siteUrl"].rstrip("/")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

ROUTES = [
    ("/", "1.0", "daily", [
        f"{SITE}/public/shahnaz-og.png",
        f"{SITE}/public/hero.jpg",
        f"{SITE}/public/bridal.jpg",
        f"{SITE}/public/images/bridal-portrait.jpg",
        f"{SITE}/public/images/hair-styling.jpg",
        f"{SITE}/public/images/mens-styling.jpg"
    ]),
    ("/bridal-makeup-patna/", "0.95", "daily", [
        f"{SITE}/public/bridal.jpg",
        f"{SITE}/public/images/bridal-portrait.jpg",
        f"{SITE}/public/images/bridal-mehndi.jpg",
        f"{SITE}/public/images/bridal-glam.jpg",
        f"{SITE}/public/hero.jpg"
    ]),
    ("/services/", "0.9", "daily", []),
    ("/book/", "0.9", "weekly", []),
    ("/unisex-salon-patna/", "0.85", "weekly", [
        f"{SITE}/public/images/mens-styling.jpg",
        f"{SITE}/public/images/hair-styling.jpg",
        f"{SITE}/public/images/hair-color.jpg",
        f"{SITE}/public/images/facial-treatment.jpg",
        f"{SITE}/public/images/salon-ambiance.jpg"
    ]),
    ("/shahnai-unisex-salon-patna/", "0.85", "weekly", []),
    ("/gallery/", "0.75", "weekly", [
        f"{SITE}/public/bridal.jpg",
        f"{SITE}/public/images/bridal-portrait.jpg",
        f"{SITE}/public/images/bridal-mehndi.jpg",
        f"{SITE}/public/images/bridal-glam.jpg",
        f"{SITE}/public/images/bridal-reception.jpg",
        f"{SITE}/public/images/hair-styling.jpg",
        f"{SITE}/public/images/hair-color.jpg",
        f"{SITE}/public/images/hair-wash.jpg",
        f"{SITE}/public/images/mens-styling.jpg",
        f"{SITE}/public/images/mens-haircut.jpg",
        f"{SITE}/public/images/facial-treatment.jpg",
        f"{SITE}/public/images/skin-glow.jpg",
        f"{SITE}/public/images/salon-ambiance.jpg",
        f"{SITE}/public/hero.jpg"
    ]),
    ("/about/", "0.7", "monthly", [
        f"{SITE}/public/hero.jpg",
        f"{SITE}/public/images/salon-ambiance.jpg"
    ]),
    ("/contact/", "0.7", "monthly", []),
    ("/faq/", "0.6", "monthly", []),
    ("/privacy-policy/", "0.3", "yearly", []),
    ("/terms/", "0.3", "yearly", []),
]

url_nodes = []
for path, prio, freq, imgs in ROUTES:
    img_xml = "".join(f"\n    <image:image><image:loc>{img}</image:loc></image:image>" for img in imgs)
    url_nodes.append(
        f"  <url>\n    <loc>{SITE}{path}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>{img_xml}\n  </url>"
    )

urls_body = "\n".join(url_nodes)
sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
{urls_body}
</urlset>
'''

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)
print("wrote sitemap.xml with", len(ROUTES), "routes")

# ----------------- Write robots.txt with advanced AI and search crawler directives
robots_txt = f'''# robots.txt for Shahnaz Beauty Parlour (https://shahnazsalon.vercel.app)
# Optimized for Google, Bing, Apple, and AI search engines (Perplexity, ChatGPT, Gemini, Claude)

User-agent: *
Allow: /
Disallow: /api/
Disallow: /apps-script/

# AI Search and Answer Engines (AEO & AIO)
User-agent: Googlebot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Bingbot
Allow: /

User-agent: Applebot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

Sitemap: {SITE}/sitemap.xml
Host: {SITE}
'''

with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots_txt)
print("wrote robots.txt with search and AI crawler directives")

# Sanity check: every route in the sitemap must have a real index.html on disk.
missing = [p for p, _, _, _ in ROUTES if p != "/" and not os.path.isfile(os.path.join(ROOT, p.strip("/"), "index.html"))]
if not os.path.isfile(os.path.join(ROOT, "index.html")):
    missing.append("/")
if missing:
    raise SystemExit("sitemap references pages that do not exist: " + ", ".join(missing))
print("all sitemap routes verified on disk")
