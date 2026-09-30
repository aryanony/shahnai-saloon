import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import (
    SITE, PRIMARY, SECONDARY, DESC, ldjson, breadcrumb, faqpage, LOCAL_BUSINESS,
    hero_arch, frames_block, TRUST_STRIP, PROCESS_STEPS, faq_block, FINAL_CTA
)

# ============================================================== HOMEPAGE
WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "name": PRIMARY,
    "alternateName": [SECONDARY, "Shahnaz Salon Patna", "Shahnai Salon Raja Bazar"],
    "url": SITE + "/",
    "image": f"{SITE}/public/shahnaz-og.png",
    "description": "Best Unisex Salon and Bridal Makeup Studio in Raja Bazar, Sheikhpura, Patna. Certified Parul Garg Academy Artistry.",
    "inLanguage": "en-IN"
}

home_faqs = [
    (f"Where is {PRIMARY} located in Patna?", f"{PRIMARY} is located at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014 on Bailey Road."),
    (f"Who is the lead bridal makeup artist at {PRIMARY}?", f"Puja Gupta is the lead bridal artist, professionally certified by Parul Garg Makeup Academy, specializing in HD bridal, engagement, reception, and party looks."),
    (f"Is {PRIMARY} a unisex salon?", f"Yes. Alongside its bridal makeup studio, {PRIMARY} offers full salon services for women and men, including hairstyling, skin care, facials, and grooming."),
    (f"Is {PRIMARY} the same salon as {SECONDARY}?", f"Yes. Regulars know this address as {SECONDARY}. The salon at Vishal Market, Raja Bazar operates as {PRIMARY}."),
    ("How do I book an appointment or bridal package?", f"You can request an appointment online via our booking form or directly message on WhatsApp at {CFG['phone']}. Our team confirms details directly with you.")
]

home_body = f'''  <section class="hero">
    <div class="container hero__grid">
      <div>
        <span class="wordmark reveal">{e(PRIMARY)}</span>
        <h1 class="reveal">Unisex Salon &amp; Bridal Makeup Studio in Raja Bazar, Patna</h1>
        <p class="lede reveal">{e(DESC)} at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar &mdash; bridal makeup, hairstyling, beauty and grooming, with a booking request confirmed personally by the salon.</p>
        <div class="actions reveal">
          <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="hero">Send Booking Request</a>
          <a class="btn btn-line" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="hero">Talk on WhatsApp</a>
        </div>
        <p class="hero__where reveal">Also known to regulars as <a href="/shahnai-unisex-salon-patna/">Shahnai Unisex Salon</a> &middot; <span data-bind-text="address">{e(addr_line())}</span></p>
      </div>
      <div class="hero__art">
{hero_arch(["Bridal", "Portfolio"])}
      </div>
    </div>
  </section>

{TRUST_STRIP}
  <section class="section" aria-labelledby="bridal-h">
    <div class="container split">
{frames_block("Signature Bridal", "HD Royal Glam", img_a="/public/bridal.jpg", img_b="/public/images/bridal-portrait.jpg")}
      <div class="reveal">
        <p class="pull">A bridal specialty, built on real experience.</p>
        <p>{e(PRIMARY)} is a unisex salon with a strong focus on bridal makeup and styling &mdash; from the first trial to the wedding morning, planned around your face, your outfit and your day.</p>
        <a class="btn btn-dark" href="/bridal-makeup-patna/">Explore Bridal Makeup</a>
      </div>
    </div>
  </section>

  <section class="section ink" aria-labelledby="services-h">
    <div class="container">
      <div class="center head reveal">
        <hr class="rule">
        <h2 id="services-h">Services</h2>
        <p class="muted">Read live from the salon&rsquo;s own records &mdash; always current.</p>
      </div>
      <div id="home-services" class="reveal"><p class="state-note">Loading current services&hellip;</p></div>
      <div class="center mt-md">
        <a class="btn btn-line" href="/services/">View Full Menu &amp; Prices</a>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="why-h">
    <div class="container">
      <div class="head reveal"><hr class="rule"><h2 id="why-h">Why clients choose {e(PRIMARY)}</h2></div>
      <div class="grid-3 reveal">
        <div class="col"><h3>Bridal-first expertise</h3><p>Bridal and pre-bridal work is the core of the salon, not an add-on &mdash; trials, timing and long-wear finishing are planned properly.</p></div>
        <div class="col"><h3>One salon, every occasion</h3><p>Unisex services for the whole family &mdash; engagement, reception and party looks, hairstyling, facials and grooming, from one Raja Bazar address.</p></div>
        <div class="col"><h3>Clear, simple booking</h3><p>Send a request in under a minute. The salon confirms the details with you directly on WhatsApp or by phone.</p></div>
      </div>
    </div>
  </section>

  <section class="section bridge" aria-labelledby="bridge-h">
    <div class="container center">
      <h2 id="bridge-h">Looking for Shahnai Unisex Salon?</h2>
      <p class="lede">{e(PRIMARY)} is the current operating brand at this Raja Bazar, Sheikhpura location, where the salon was previously known to many regulars as Shahnai Unisex Salon.</p>
      <div class="actions">
        <a class="btn btn-line" href="/shahnai-unisex-salon-patna/">Read the Full Story</a>
      </div>
    </div>
  </section>

  <section class="section ink" aria-labelledby="gallery-h">
    <div class="container">
      <div class="center head reveal"><hr class="rule"><h2 id="gallery-h">Real work from the salon</h2></div>
      <div class="gallery reveal">
        <figure><img src="/public/bridal.jpg" alt="Real Bridal Transformation by Shahnaz Beauty Parlour" width="400" height="500" loading="lazy"><figcaption>Signature Bridal Transformation</figcaption></figure>
        <figure><img src="/public/images/bridal-portrait.jpg" alt="Royal HD Bridal Artistry by Puja Gupta" width="400" height="500" loading="lazy"><figcaption>Royal HD Bridal Artistry</figcaption></figure>
        <figure><img src="/public/images/hair-styling.jpg" alt="Luxury Hair Styling &amp; Occasion Waves" width="400" height="500" loading="lazy"><figcaption>Luxury Hair Styling &amp; Waves</figcaption></figure>
        <figure><img src="/public/images/mens-styling.jpg" alt="Executive Men's Grooming &amp; Styling" width="400" height="500" loading="lazy"><figcaption>Executive Men's Grooming</figcaption></figure>
        <figure><img src="/public/images/facial-treatment.jpg" alt="Golden Glow Skin Therapy &amp; Facial" width="400" height="500" loading="lazy"><figcaption>Golden Glow Skin Therapy</figcaption></figure>
        <figure><img src="/public/hero.jpg" alt="Puja Gupta Certified by Parul Garg Makeup Academy" width="400" height="500" loading="lazy"><figcaption>Parul Garg Certified Artistry</figcaption></figure>
      </div>
      <div class="center mt-md"><a class="btn btn-line" href="/gallery/" data-analytics="gallery_open" data-analytics-label="home">See Full Gallery</a></div>
    </div>
  </section>

{PROCESS_STEPS}
  <section class="section ink center" aria-labelledby="reviews-h">
    <div class="container">
      <div class="head"><hr class="rule"><h2 id="reviews-h">What clients say</h2><p class="muted">Real reviews only.</p></div>
      <p class="muted">Verified reviews will appear here once shared by the salon. No review text is invented for this page.</p>
      <a class="btn btn-line" href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="reviews">See Real Work on Instagram</a>
    </div>
  </section>

  <section class="section" aria-labelledby="about-h">
    <div class="container narrow">
      <hr class="rule">
      <h2 id="about-h">About {e(PRIMARY)}</h2>
      <p>{e(PRIMARY)} is a unisex salon in Sheikhpura, Raja Bazar, Patna, with a specialty in bridal makeup and styling &mdash; serving brides, families and everyday grooming clients from one location at Vishal Market, near Pillar No. 76.</p>
      <a class="btn btn-dark" href="/about/">Read More</a>
    </div>
  </section>

  <section class="section ink" aria-labelledby="loc-h">
    <div class="container">
      <div class="head"><hr class="rule"><h2 id="loc-h">Find us in Raja Bazar</h2><p class="muted" data-bind-text="address">{e(addr_line())}</p></div>
      <div class="actions">
        <a class="btn btn-gold" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="location_section">Get Directions</a>
        <a class="btn btn-line" href="tel:" data-bind-href="phone" data-analytics="phone_click" data-analytics-label="location_section">Call Us</a>
      </div>
    </div>
  </section>

{faq_block(home_faqs)}
{FINAL_CTA}'''

write("index.html", page(
    f"{PRIMARY} | Best Unisex Salon &amp; Bridal Makeup in Patna",
    f"{PRIMARY} at Pillar No. 76, Raja Bazar, Sheikhpura, Patna \u2014 certified bridal makeup by Parul Garg Academy alumna Puja Gupta, hair styling, facials and unisex grooming.",
    SITE + "/", "/", home_body,
    extra_head=ldjson(LOCAL_BUSINESS) + ldjson(WEBSITE_SCHEMA) + ldjson(faqpage(home_faqs)),
    extra_scripts='<script src="/src/js/home.js"></script>\n'
))

# ============================================================== BOOK
book_body = '''  <section class="section-sm ink">
    <div class="container narrow center">
      <hr class="rule">
      <h1>Send a Booking Request</h1>
      <p class="lede">Choose your service and preferred date. Takes less than a minute &mdash; we&rsquo;ll contact you to confirm.</p>
    </div>
  </section>

  <section class="section section-tight">
    <div class="container book-grid">
      <div class="reveal">
        <p class="pull">This is a request, not a live calendar.</p>
        <p>Submitting the form sends your details to the salon. It does not mean the appointment is confirmed &mdash; the salon will reach out on WhatsApp or by phone to agree the exact time before it&rsquo;s final.</p>
        <p class="muted small">Prefer to skip the form? Call or WhatsApp us directly using the buttons in the footer.</p>
      </div>

      <div>
        <div class="panel" id="panel-form">
          <form id="booking-form" novalidate>
            <div class="field">
              <label for="name">Name</label>
              <input type="text" id="name" name="name" autocomplete="name" required maxlength="60">
              <p class="err" role="alert">Please enter your name.</p>
            </div>
            <div class="field">
              <label for="mobile">Mobile number</label>
              <input type="tel" id="mobile" name="mobile" autocomplete="tel" inputmode="tel" placeholder="98xxxxxxxx" required>
              <p class="err" role="alert">Please enter a valid 10-digit mobile number.</p>
            </div>
            <div class="field">
              <label for="service">Service</label>
              <select id="service" name="serviceId" required>
                <option value="" disabled selected>Loading services&hellip;</option>
              </select>
              <p class="err" role="alert">Please choose a service.</p>
            </div>
            <div class="field">
              <label for="preferredDate">Preferred date</label>
              <input type="date" id="preferredDate" name="preferredDate" required>
              <p class="err" role="alert">Please choose today or a later date.</p>
            </div>
            <div class="field">
              <label for="preferredTime">Preferred time <span class="opt">(optional)</span></label>
              <input type="time" id="preferredTime" name="preferredTime">
            </div>
            <fieldset class="field">
              <legend>Additional services <span class="opt">(optional)</span></legend>
              <div class="checks" id="addon-list"></div>
            </fieldset>
            <div class="field">
              <label for="note">Anything we should know? <span class="opt">(optional)</span></label>
              <textarea id="note" name="note" maxlength="300" rows="3"></textarea>
              <p class="hint">Up to 300 characters.</p>
              <p class="err" role="alert">Please keep your note under 300 characters.</p>
            </div>
            <div class="trap" aria-hidden="true">
              <label for="company">Company</label>
              <input type="text" id="company" name="company" tabindex="-1" autocomplete="off">
            </div>
            <button class="btn btn-gold btn-block" type="submit" id="submit-btn">
              <span class="spin" aria-hidden="true"></span>
              <span class="label">Send Booking Request</span>
            </button>
            <p class="foot-note muted">Takes less than a minute. We&rsquo;ll contact you to confirm.</p>
          </form>
        </div>

        <div class="panel state" id="panel-success">
          <div class="center">
            <span class="tick" aria-hidden="true">&#10003;</span>
            <p class="mark">Request received</p>
            <p id="success-message">Your booking request has been received. We&rsquo;ll contact you to confirm.</p>
            <span class="bid">Booking ID<br><span id="booking-id"></span></span>
            <div class="actions">
              <a class="btn btn-dark" href="tel:" data-bind-href="phone" data-analytics="phone_click" data-analytics-label="booking_success">Call</a>
              <a class="btn btn-gold" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, following up on my booking request." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="booking_success">WhatsApp</a>
              <a class="btn btn-line" href="/services/">Explore Services</a>
            </div>
          </div>
        </div>

        <div class="panel state" id="panel-error">
          <div class="center">
            <p class="mark">We couldn&rsquo;t send that</p>
            <p>Something went wrong on our end and your request didn&rsquo;t go through. Please call or message us directly and we&rsquo;ll take your details right away.</p>
            <div class="actions">
              <a class="btn btn-dark" href="tel:" data-bind-href="phone" data-analytics="phone_click" data-analytics-label="booking_error">Call</a>
              <a class="btn btn-gold" id="wa-fallback" href="https://wa.me/" data-bind-href="whatsapp" target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="booking_error">WhatsApp Us</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
'''
write("book/index.html", page(
    f"Send a Booking Request | {PRIMARY}, Patna",
    f"Request an appointment at {PRIMARY} in Raja Bazar, Patna. Choose your service and preferred date \u2014 we'll contact you to confirm.",
    SITE + "/book/", "/book/", book_body,
    extra_scripts='<script src="/src/js/booking.js"></script>\n'
))

# ============================================================== SERVICES
services_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Services &amp; Prices</h1>
      <p class="lede">Read live from the salon&rsquo;s own records, so this always reflects what&rsquo;s currently offered. Where a price shows as &ldquo;Price on enquiry&rdquo;, ask us on WhatsApp or by phone and we&rsquo;ll confirm it for your booking.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div id="services-menu"><p class="state-note">Loading current services&hellip;</p></div>
    </div>
  </section>

  <section class="section ink">
    <div class="container">
      <div class="center head"><hr class="rule"><h2>Additional services</h2><p class="muted">Add any of these to your booking request.</p></div>
      <div id="addons-menu"><p class="state-note">Loading add-ons&hellip;</p></div>
    </div>
  </section>

  <section class="section center">
    <div class="container"><a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="services_page">Send Booking Request</a></div>
  </section>
'''
write("services/index.html", page(
    f"Services & Prices | {PRIMARY}, Patna",
    f"Current services and prices at {PRIMARY}, Raja Bazar, Patna \u2014 bridal, beauty, hair and grooming, updated live from the salon.",
    SITE + "/services/", "/services/", services_body,
    extra_head=ldjson(breadcrumb(("Services", "/services/"))),
    extra_scripts='<script src="/src/js/services.js"></script>\n'
))

print("home/book/services done")
