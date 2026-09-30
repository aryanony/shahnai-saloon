import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import SITE, PRIMARY, SECONDARY, ldjson, breadcrumb, faqpage, frames_block, FINAL_CTA, faq_block

# ============================================================== BRIDAL
bridal_faqs = [
    ("What bridal makeup services are available?", "Bridal, engagement and reception makeup, and pre-bridal services, with bridal hairstyling and saree or dupatta draping available as add-ons. Current availability and prices are always on the services page."),
    ("Does the salon offer a bridal makeup trial?", "A bridal makeup trial can be requested as an add-on when submitting a booking request; the salon will confirm availability directly."),
    ("How do I book bridal makeup?", 'Submit a booking request on the website with your preferred date. The salon will contact you on WhatsApp or by phone to confirm the appointment.'),
]

bridal_body = f'''  <section class="hero section-sm">
    <div class="container narrow">
      <span class="wordmark reveal">Bridal Specialty</span>
      <h1 class="reveal">Bridal Makeup in Patna</h1>
      <p class="lede reveal">{e(PRIMARY)} in Sheikhpura, Raja Bazar, Patna offers bridal, engagement and reception makeup, pre-bridal services, bridal hairstyling and draping &mdash; planned around your face, outfit and wedding-day timeline.</p>
      <div class="actions reveal">
        <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="bridal_page">Request Bridal Appointment</a>
        <a class="btn btn-line" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about bridal makeup." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="bridal_page">Talk on WhatsApp</a>
      </div>
    </div>
  </section>

  <section class="section prose">
    <div class="container narrow">
      <h2>What&rsquo;s included in a bridal booking</h2>
      <p>A bridal request can include the core makeup application along with add-ons: bridal hairstyling, saree or dupatta draping, a bridal makeup trial, and family or guest makeup for those attending with you. Exact inclusions and pricing are confirmed with the salon once you submit a request, since every bridal look is planned individually.</p>
      <h2>Bridal looks offered</h2>
      <ul>
        <li><strong>Bridal Makeup</strong> &mdash; for the wedding day itself.</li>
        <li><strong>Engagement Makeup</strong> &mdash; for the engagement or ring ceremony.</li>
        <li><strong>Reception Makeup</strong> &mdash; a distinct look for the reception function.</li>
        <li><strong>Pre-Bridal Services</strong> &mdash; skin and beauty preparation ahead of the wedding.</li>
      </ul>
      <p>Only services the salon currently offers are listed here and on the <a href="/services/">services page</a>, which is kept in sync with the salon&rsquo;s own records &mdash; nothing here is invented.</p>
    </div>
  </section>

  <section class="section ink">
    <div class="container split">
{frames_block("Bridal look", "Trial look")}
      <div class="reveal">
        <p class="pull">Real bridal work, not stock photography.</p>
        <p class="muted">This section is set up for the salon to add real, optimized photographs of actual bridal work. No placeholder or stock imagery is presented to visitors as real client work.</p>
        <a class="btn btn-line" href="/gallery/">See Full Gallery</a>
      </div>
    </div>
  </section>

{faq_block(bridal_faqs, anchor="bridal-faq")}
  <section class="section ink">
    <div class="container">
      <div class="head"><hr class="rule"><h2>Location</h2><p class="muted" data-bind-text="address">{e(addr_line())}</p></div>
      <div class="actions">
        <a class="btn btn-gold" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="bridal_page">Get Directions</a>
        <a class="btn btn-line" href="/book/">Request Bridal Appointment</a>
      </div>
    </div>
  </section>
'''
write("bridal-makeup-patna/index.html", page(
    f"Bridal Makeup in Patna | {PRIMARY}, Raja Bazar",
    f"Bridal makeup in Patna at {PRIMARY}, Raja Bazar \u2014 bridal, engagement and reception makeup, pre-bridal care, hairstyling and draping. Request an appointment.",
    SITE + "/bridal-makeup-patna/", "/bridal-makeup-patna/", bridal_body,
    extra_head=ldjson(breadcrumb(("Bridal Makeup in Patna", "/bridal-makeup-patna/"))) + ldjson(faqpage(bridal_faqs))
))

# ============================================================== UNISEX SALON
unisex_faqs = [
    ("Is " + PRIMARY + " a unisex salon?", "Yes. Alongside its bridal specialty, the salon serves men, women and families with hairstyling, facials and grooming."),
    ("Where is the salon located?", "Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014."),
]
unisex_body = f'''  <section class="hero section-sm">
    <div class="container narrow">
      <span class="wordmark reveal">Unisex Salon</span>
      <h1 class="reveal">Unisex Salon in Patna</h1>
      <p class="lede reveal">Alongside its bridal specialty, {e(PRIMARY)} serves men, women and families from one location in Sheikhpura, Raja Bazar &mdash; hairstyling, facials and grooming for every member of the household.</p>
      <div class="actions reveal">
        <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="unisex_page">Send Booking Request</a>
        <a class="btn btn-line" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about salon services." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="unisex_page">Talk on WhatsApp</a>
      </div>
    </div>
  </section>

  <section class="section prose">
    <div class="container narrow">
      <h2>Services for everyone</h2>
      <ul>
        <li><strong>Hair Styling</strong> &mdash; for everyday and occasion looks.</li>
        <li><strong>Facial / Skin Care</strong> &mdash; beauty and skin care treatments.</li>
        <li><strong>Men&rsquo;s Grooming</strong> &mdash; grooming services for men.</li>
        <li><strong>Party Makeup</strong> &mdash; for functions and celebrations.</li>
      </ul>
      <p>The current list of active services and prices is always on the <a href="/services/">services page</a>, sourced directly from the salon&rsquo;s own records.</p>
      <h2>One salon, one address</h2>
      <p>{e(PRIMARY)} operates from a single location at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014 &mdash; the same salon behind its bridal makeup work, previously known to some regulars as <a href="/shahnai-unisex-salon-patna/">Shahnai Unisex Salon</a>.</p>
    </div>
  </section>

{faq_block(unisex_faqs, anchor="unisex-faq")}
  <section class="section ink">
    <div class="container">
      <div class="head"><hr class="rule"><h2>Location</h2><p class="muted" data-bind-text="address">{e(addr_line())}</p></div>
      <div class="actions">
        <a class="btn btn-gold" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="unisex_page">Get Directions</a>
        <a class="btn btn-line" href="/book/">Send Booking Request</a>
      </div>
    </div>
  </section>
'''
write("unisex-salon-patna/index.html", page(
    f"Unisex Salon in Patna | {PRIMARY}, Raja Bazar",
    f"Unisex salon in Sheikhpura, Raja Bazar, Patna \u2014 hairstyling, facials and men's grooming at {PRIMARY}.",
    SITE + "/unisex-salon-patna/", "/unisex-salon-patna/", unisex_body,
    extra_head=ldjson(breadcrumb(("Unisex Salon in Patna", "/unisex-salon-patna/"))) + ldjson(faqpage(unisex_faqs))
))

print("bridal/unisex done")
