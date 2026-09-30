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
    "@id": SITE + "/#salon",
    "name": PRIMARY,
    "alternateName": SECONDARY,
    "description": DESC + " in Raja Bazar, Sheikhpura, Patna. Specializing in HD & Airbrush Bridal Makeup by Parul Garg Certified Artist Puja Gupta, alongside unisex hair styling, facials, and grooming.",
    "url": SITE + "/",
    "telephone": CFG["phone"],
    "priceRange": "\u20B9\u20B9",
    "currenciesAccepted": "INR",
    "paymentAccepted": "Cash, UPI, Google Pay, PhonePe, Paytm, Card",
    "image": f"{SITE}/public/shahnaz-og.png",
    "logo": f"{SITE}/public/icon.png",
    "hasMap": CFG["mapsUrl"],
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 25.6093,
        "longitude": 85.0886
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "09:30",
            "closes": "20:30"
        }
    ],
    "areaServed": [
        {"@type": "City", "name": "Patna"},
        {"@type": "Place", "name": "Raja Bazar, Patna"},
        {"@type": "Place", "name": "Sheikhpura, Patna"},
        {"@type": "Place", "name": "Bailey Road, Patna"},
        {"@type": "Place", "name": "Ashiana Nagar, Patna"},
        {"@type": "Place", "name": "Boring Road, Patna"},
        {"@type": "Place", "name": "Kankarbagh, Patna"},
        {"@type": "Place", "name": "Jagdeo Path, Patna"},
        {"@type": "Place", "name": "Shastri Nagar, Patna"},
        {"@type": "Place", "name": "Danapur, Patna"}
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": CFG["address"]["line1"],
        "addressLocality": CFG["address"]["city"],
        "addressRegion": CFG["address"]["state"],
        "postalCode": CFG["address"]["postalCode"],
        "addressCountry": CFG["address"]["country"],
    },
    "founder": {
        "@type": "Person",
        "name": "Puja Gupta",
        "jobTitle": "Lead Bridal Makeup Artist & Salon Founder",
        "alumniOf": {
            "@type": "EducationalOrganization",
            "name": "Parul Garg Makeup Academy"
        }
    },
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Shahnaz Beauty & Bridal Services Menu",
        "itemListElement": [
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Bridal Makeup in Patna",
                    "description": "HD and Airbrush Bridal Makeup by Parul Garg Certified Artist Puja Gupta"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Engagement & Reception Makeup",
                    "description": "Custom occasion makeup and pre-bridal care"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Unisex Hair Styling & Treatments",
                    "description": "Cuts, hair styling, spa, and beauty treatments"
                }
            },
            {
                "@type": "Offer",
                "itemOffered": {
                    "@type": "Service",
                    "name": "Facials & Skin Rejuvenation",
                    "description": "Skin cleansing, glowing facials and skin care"
                }
            }
        ]
    },
    "sameAs": [u for u in [CFG["instagramUrl"], CFG["mapsUrl"]] if u],
}

# ----------------------------------------------------------------- shared bits
def hero_arch(caption_lines=None, img_src="/public/hero.jpg", img_alt="Certified Makeup and Hairstyling Artist Puja Gupta with Parul Garg"):
    return f'''      <div class="arch-wrap reveal">
        <div class="arch arch--photo">
          <img src="{img_src}" alt="{e(img_alt)}" width="600" height="600" loading="eager" fetchpriority="high">
          <div class="arch__overlay"></div>
          <div class="arch__badge">
            <span class="arch__badge-kicker">Certified Professional</span>
            <span class="arch__badge-title">Parul Garg Makeup Academy</span>
          </div>
        </div>
      </div>'''

def frames_block(tag_a="Bridal Look", tag_b="Reception & Artistry", img_a="/public/bridal.jpg", img_b="/public/parul-garg.jpg"):
    img_b_tag = f'<img src="{img_b}" alt="{e(tag_b)}" width="480" height="640" loading="lazy">' if img_b else ''
    return f'''    <div class="frames reveal">
      <div class="frame frame--b">
        {img_b_tag}
        <span class="frame__tag">{tag_b}</span>
      </div>
      <div class="frame frame--a">
        <img src="{img_a}" alt="{e(tag_a)} - Real Bridal Transformation" width="480" height="640" loading="lazy">
        <span class="frame__tag frame__tag--gold">{tag_a}</span>
      </div>
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
