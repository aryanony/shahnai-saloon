import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import SITE, PRIMARY, SECONDARY, ldjson, breadcrumb

# ============================================================== GALLERY
def ph_figs(n, label):
    return "\n".join(
        f'''      <figure class="reveal"><div class="ph-box" role="img" aria-label="Placeholder for real salon photography"></div><figcaption class="muted small">{label}</figcaption></figure>'''
        for _ in range(n)
    )

gallery_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Gallery</h1>
      <p class="lede">Real work from the salon floor. This page is set up for the owner to add real, lazy-loaded photography &mdash; no stock or placeholder images are presented as real client work.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Bridal</h2>
      <div class="gallery">
{ph_figs(3, "Add real bridal photography")}
      </div>
    </div>
  </section>

  <section class="section ivory-2">
    <div class="container">
      <h2>Hair &amp; Styling</h2>
      <div class="gallery">
{ph_figs(3, "Add real hair/styling photography")}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Salon &amp; Grooming</h2>
      <div class="gallery">
{ph_figs(3, "Add real salon/grooming photography")}
      </div>
    </div>
  </section>

  <section class="section ink center">
    <div class="container">
      <p>See more real work on Instagram.</p>
      <a class="btn btn-gold" href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="gallery_page">Instagram</a>
    </div>
  </section>
'''
write("gallery/index.html", page(
    f"Gallery | {PRIMARY}, Patna",
    f"Real bridal and salon work from {PRIMARY}, Raja Bazar, Patna.",
    SITE + "/gallery/", "/gallery/", gallery_body,
    extra_head=ldjson(breadcrumb(("Gallery", "/gallery/")))
))

# ============================================================== ABOUT
about_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>About {e(PRIMARY)}</h1>
    </div>
  </section>

  <section class="section prose">
    <div class="container narrow">
      <p>{e(PRIMARY)} is a unisex salon at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar. The salon&rsquo;s primary focus is bridal makeup and styling, alongside everyday beauty, hair and grooming services for the whole family.</p>
      <p>The salon previously traded as <a href="/shahnai-unisex-salon-patna/">{e(SECONDARY)}</a> &mdash; both names refer to the same salon at the same address; see that page for the full explanation.</p>
      <h2>What we focus on</h2>
      <ul>
        <li>Bridal, engagement and reception makeup, with pre-bridal services</li>
        <li>Bridal hairstyling and saree / dupatta draping</li>
        <li>Hair styling, facials and skin care</li>
        <li>Men&rsquo;s grooming</li>
      </ul>
      <p>Service availability and pricing are managed directly by the salon and reflected live on the <a href="/services/">services page</a> &mdash; nothing on this site is invented or assumed.</p>
      <h2>Visit us</h2>
      <p data-bind-text="address">{e(addr_line())}</p>
      <div class="actions">
        <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="about_page">Send Booking Request</a>
        <a class="btn btn-dark" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="about_page">Get Directions</a>
      </div>
    </div>
  </section>
'''
write("about/index.html", page(
    f"About | {PRIMARY}, Patna",
    f"About {PRIMARY} \u2014 a unisex salon with a bridal makeup specialty in Sheikhpura, Raja Bazar, Patna.",
    SITE + "/about/", "/about/", about_body,
    extra_head=ldjson(breadcrumb(("About", "/about/")))
))

# ============================================================== CONTACT
contact_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Contact</h1>
      <p class="lede">Reach {e(PRIMARY)} directly, or send a booking request and we&rsquo;ll get back to you.</p>
    </div>
  </section>

  <section class="section">
    <div class="container grid-3">
      <div class="col">
        <h3>Call</h3>
        <p>
          <a href="tel:" data-bind-href="phone" data-bind-text="phone" data-analytics="phone_click" data-analytics-label="contact_page">{e(CFG['phone'])}</a><br>
          <a href="tel:{e(CFG['alternatePhone'])}" data-analytics="phone_click" data-analytics-label="contact_page_alt">{e(CFG['alternatePhone'])}</a>
        </p>
      </div>
      <div class="col">
        <h3>WhatsApp</h3>
        <p><a href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="contact_page">Message on WhatsApp</a></p>
      </div>
      <div class="col">
        <h3>Instagram</h3>
        <p><a href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="contact_page">Visit our Instagram</a></p>
      </div>
    </div>
  </section>

  <section class="section ivory-2">
    <div class="container">
      <h3>Address</h3>
      <p data-bind-text="address">{e(addr_line())}</p>
      <a class="btn btn-dark" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="contact_page">Get Directions</a>
    </div>
  </section>

  <section class="section ink center">
    <div class="container">
      <h2>Prefer to request a booking instead?</h2>
      <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="contact_page">Send Booking Request</a>
    </div>
  </section>
'''
write("contact/index.html", page(
    f"Contact | {PRIMARY}, Patna",
    f"Call, WhatsApp or visit {PRIMARY} in Raja Bazar, Patna.",
    SITE + "/contact/", "/contact/", contact_body,
    extra_head=ldjson(breadcrumb(("Contact", "/contact/")))
))

print("gallery/about/contact done")
