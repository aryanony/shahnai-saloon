import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e

SITE = CFG["siteUrl"].rstrip("/")
PRIMARY = CFG["primaryBrand"]
SECONDARY = CFG["secondaryBrand"]
DESC = CFG["descriptor"]

def ldjson(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>\n"

def breadcrumb(*parts):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (name, path) in enumerate(parts, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": SITE + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def faqpage(qas):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qas
        ],
    }

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "BeautySalon",
    "name": PRIMARY,
    "alternateName": SECONDARY,
    "description": DESC + " in Raja Bazar, Sheikhpura, Patna.",
    "url": SITE + "/",
    "telephone": CFG["phone"],
    "priceRange": "\u20B9\u20B9",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": CFG["address"]["line1"],
        "addressLocality": CFG["address"]["city"],
        "addressRegion": CFG["address"]["state"],
        "postalCode": CFG["address"]["postalCode"],
        "addressCountry": CFG["address"]["country"],
    },
    "sameAs": [u for u in [CFG["instagramUrl"]] if u],
}

# ----------------------------------------------------------------- shared bits
def hero_arch(caption_lines):
    spans = "".join(f"<span>{c}</span>" for c in caption_lines)
    return f'''      <div class="arch-wrap reveal">
        <div class="arch">
          <div class="arch__words">{spans}</div>
        </div>
      </div>'''

def frames_block(tag_a, tag_b):
    return f'''    <div class="frames reveal" aria-hidden="true">
      <div class="frame frame--b"><span class="menu__price small">{tag_b}</span></div>
      <div class="frame frame--a"><span class="menu__price small">{tag_a}</span></div>
    </div>'''

def gallery_placeholder_grid(n, label="Real photography — add here"):
    figs = "\n".join(
        f'''      <figure class="reveal">
        <div class="ph-box" role="img" aria-label="Placeholder for real salon photography"></div>
        <figcaption class="muted small">{label}</figcaption>
      </figure>'''
        for _ in range(n)
    )
    return f'    <div class="gallery">\n{figs}\n    </div>'

TRUST_STRIP = f'''  <div class="trust">
    <div class="container trust__row">
      <span data-bind-text="address">{e(addr_line())}</span>
      <a href="tel:" data-bind-href="phone" data-bind-text="phone" data-analytics="phone_click" data-analytics-label="trust_strip">{e(CFG['phone'])}</a>
      <a href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="trust_strip">Get Directions</a>
      <a href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="trust_strip">Instagram</a>
    </div>
  </div>
'''

PROCESS_STEPS = '''  <section class="section" aria-labelledby="process-h">
    <div class="container">
      <div class="center head reveal">
        <hr class="rule">
        <h2 id="process-h">How a booking request works</h2>
      </div>
      <ol class="steps reveal">
        <li><h3>Send a request</h3><p>Choose a service and preferred date on the booking form. It takes under a minute.</p></li>
        <li><h3>We confirm with you</h3><p>The salon contacts you on WhatsApp or by phone to confirm the exact time.</p></li>
        <li><h3>Visit the salon</h3><p data-bind-text="address">''' + e(addr_line()) + '''</p></li>
      </ol>
    </div>
  </section>
'''

def faq_block(qas, anchor="faq"):
    items = "\n".join(
        f'''    <details><summary>{q}</summary><p>{a}</p></details>'''
        for q, a in qas
    )
    return f'  <section class="section faq" id="{anchor}" aria-labelledby="faq-h">\n    <div class="container narrow">\n      <div class="reveal head-sm"><hr class="rule"><h2 id="faq-h">Frequently asked questions</h2></div>\n{items}\n    </div>\n  </section>\n'

FINAL_CTA = '''  <section class="section ink center" aria-labelledby="cta-h">
    <div class="container">
      <h2 id="cta-h">Ready to plan your visit?</h2>
      <p class="lede">Send a booking request and we will confirm the details with you directly.</p>
      <div class="actions">
        <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="final_cta">Send Booking Request</a>
        <a class="btn btn-line" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="final_cta">Talk on WhatsApp</a>
      </div>
    </div>
  </section>
'''
