import json, os, html, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CFG = json.load(open(os.path.join(ROOT, "config", "business.json")))

# Baked-in defaults so every phone/WhatsApp link works even before JS hydration
# (or if JS fails to load). data-bind-href on the same element upgrades it live
# from the Sheet when the value there differs from this deploy-time default.
TEL_DEFAULT = "tel:" + CFG["phone"]
WA_DEFAULT = "https://wa.me/" + re.sub(r"\D", "", CFG["whatsapp"])

NAV = [
    ("/bridal-makeup-patna/", "Bridal"),
    ("/unisex-salon-patna/", "Salon"),
    ("/services/", "Services"),
    ("/gallery/", "Gallery"),
    ("/about/", "About"),
    ("/contact/", "Contact"),
    ("/faq/", "FAQ"),
]

def addr_line():
    a = CFG["address"]
    return f'{a["line1"]}, {a["locality"]}, {a["city"]}, {a["state"]} {a["postalCode"]}'

def e(s): return html.escape(str(s), quote=True)

def head_common(title, description, canonical, extra_head="", robots=""):
    robots_tag = f'\n<meta name="robots" content="{e(robots)}">' if robots else ""
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">{robots_tag}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:site_name" content="{e(CFG['primaryBrand'])}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="icon" href="/public/icons/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/src/css/styles.css">
<script src="/src/js/boot.js"></script>
{extra_head}'''

def header(current):
    items = "\n".join(
        f'        <li><a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>'
        for h, l in NAV
    )
    cta_cur = ' aria-current="page"' if current == "/book/" else ""
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header" data-header>
  <div class="container bar">
    <a class="brand" href="/">
      <span class="brand__name" data-bind-text="brand">{e(CFG['primaryBrand'])}</span>
      <span class="brand__tag" data-bind-text="descriptor">{e(CFG['descriptor'])}</span>
    </a>
    <nav class="nav" aria-label="Primary">
      <ul id="primary-nav">
{items}
      </ul>
      <a class="btn btn-gold" href="/book/"{cta_cur} data-analytics="booking_start" data-analytics-label="header">Send Booking Request</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" data-menu-toggle>Menu</button>
    </nav>
  </div>
</header>
'''

def sticky_bar():
    return '''<nav class="sticky-bar" aria-label="Quick actions">
  <a href="tel:" data-bind-href="phone" data-analytics="phone_click" data-analytics-label="sticky_bar">Call</a>
  <a href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="sticky_bar">WhatsApp</a>
  <a class="go" href="/book/" data-analytics="booking_start" data-analytics-label="sticky_bar">Book Now</a>
</nav>
'''

def consent_banner():
    return '''<div class="consent" data-consent hidden role="dialog" aria-label="Cookie consent">
  <p>We use optional analytics (Google Analytics, Microsoft Clarity) to understand how the site is used. No booking details are ever sent to them.</p>
  <div class="row">
    <button type="button" class="btn btn-gold" data-consent-accept>Accept</button>
    <button type="button" class="btn btn-dark" data-consent-decline>Decline</button>
  </div>
</div>
'''

def footer():
    nav_extra = "".join(f'        <li><a href="{h}">{l}</a></li>\n' for h, l in NAV if h not in ("/contact/",))
    return f'''<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <h2 data-bind-text="brand">{e(CFG['primaryBrand'])}</h2>
      <p data-bind-text="descriptor">{e(CFG['descriptor'])}</p>
      <p data-bind-text="address">{e(addr_line())}</p>
    </div>
    <div>
      <h2>Explore</h2>
      <ul>
{nav_extra}        <li><a href="/book/">Send Booking Request</a></li>
        <li><a href="/shahnai-unisex-salon-patna/">Shahnai Unisex Salon</a></li>
      </ul>
    </div>
    <div>
      <h2>Connect</h2>
      <ul>
        <li><a href="tel:" data-bind-href="phone" data-bind-text="phone" data-analytics="phone_click" data-analytics-label="footer">{e(CFG['phone'])}</a></li>
        <li><a href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="footer">WhatsApp</a></li>
        <li><a href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="footer">Instagram</a></li>
        <li><a href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="footer">Get Directions</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <span>&copy; <span data-year></span> {e(CFG['primaryBrand'])}. All rights reserved.</span>
    <span><a href="/privacy-policy/">Privacy Policy</a> &middot; <a href="/terms/">Terms</a></span>
  </div>
</footer>
'''

SCRIPTS_COMMON = '''<script src="/src/js/analytics.js"></script>
<script src="/src/js/catalog.js"></script>
<script src="/src/js/main.js"></script>
'''

def page(title, description, canonical, current, body, extra_head="", extra_scripts="", robots="", body_class=""):
    cls = f' class="{body_class}"' if body_class else ""
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
{head_common(title, description, canonical, extra_head, robots)}
</head>
<body{cls}>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
{sticky_bar()}
{consent_banner()}
{SCRIPTS_COMMON}{extra_scripts}</body>
</html>
'''

def write(relpath, content):
    # Central fix-up: no page should ever ship a dead tel:/wa.me link waiting on JS.
    content = content.replace('href="tel:"', f'href="{TEL_DEFAULT}"')
    content = content.replace('href="https://wa.me/"', f'href="{WA_DEFAULT}"')
    full = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", relpath, len(content), "bytes")
