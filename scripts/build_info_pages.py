import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import SITE, PRIMARY, SECONDARY, ldjson, breadcrumb, frames_block

# ============================================================== GALLERY
gallery_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Gallery</h1>
      <p class="lede">Artistry, bridal transformations, and salon craft from {e(PRIMARY)} &mdash; serving clients across Raja Bazar, Bailey Road, and Patna.</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Bridal &amp; Occasion Artistry</h2>
      <div class="gallery">
        <figure class="reveal"><img src="/public/bridal.jpg" alt="Signature Royal Bridal Look by Shahnaz Beauty Parlour" width="400" height="500" loading="lazy"><figcaption>Signature Royal Bridal Look</figcaption></figure>
        <figure class="reveal"><img src="/public/images/bridal-portrait.jpg" alt="HD Bridal Artistry with Kundan Jewelry by Puja Gupta" width="400" height="500" loading="lazy"><figcaption>HD Royal Bridal Artistry</figcaption></figure>
        <figure class="reveal"><img src="/public/images/bridal-mehndi.jpg" alt="Intricate Bridal Henna &amp; Mehndi Art" width="400" height="500" loading="lazy"><figcaption>Intricate Bridal Mehndi Art</figcaption></figure>
        <figure class="reveal"><img src="/public/images/bridal-glam.jpg" alt="Occasion Saree &amp; Engagement Artistry" width="400" height="500" loading="lazy"><figcaption>Engagement &amp; Occasion Glam</figcaption></figure>
        <figure class="reveal"><img src="/public/images/bridal-reception.jpg" alt="Reception Artistry &amp; Evening Glam" width="400" height="500" loading="lazy"><figcaption>Reception &amp; Evening Styling</figcaption></figure>
        <figure class="reveal"><img src="/public/hero.jpg" alt="Parul Garg Makeup Academy Certificate - Puja Gupta" width="400" height="500" loading="lazy"><figcaption>Parul Garg Academy Certification</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="section ivory-2">
    <div class="container">
      <h2>Hair &amp; Styling</h2>
      <div class="gallery">
        <figure class="reveal"><img src="/public/images/hair-styling.jpg" alt="Occasion Hair Styling &amp; Glossy Waves" width="400" height="500" loading="lazy"><figcaption>Luxury Hair Styling &amp; Waves</figcaption></figure>
        <figure class="reveal"><img src="/public/images/hair-color.jpg" alt="Balayage &amp; Premium Hair Coloring" width="400" height="500" loading="lazy"><figcaption>Balayage &amp; Hair Color</figcaption></figure>
        <figure class="reveal"><img src="/public/images/hair-wash.jpg" alt="Deep Nourishing Hair Spa &amp; Scalp Treatment" width="400" height="500" loading="lazy"><figcaption>Hair Spa &amp; Treatment</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <h2>Salon &amp; Grooming</h2>
      <div class="gallery">
        <figure class="reveal"><img src="/public/images/mens-styling.jpg" alt="Executive Beard Trim &amp; Men's Styling" width="400" height="500" loading="lazy"><figcaption>Executive Men's Grooming</figcaption></figure>
        <figure class="reveal"><img src="/public/images/mens-haircut.jpg" alt="Precision Scissor Fade &amp; Men's Haircut" width="400" height="500" loading="lazy"><figcaption>Precision Scissor Haircut</figcaption></figure>
        <figure class="reveal"><img src="/public/images/facial-treatment.jpg" alt="Golden Glow Herbal Facial Mask" width="400" height="500" loading="lazy"><figcaption>Golden Glow Facial Therapy</figcaption></figure>
        <figure class="reveal"><img src="/public/images/skin-glow.jpg" alt="Radiant Skin Cleansing &amp; Rejuvenation" width="400" height="500" loading="lazy"><figcaption>Skin Cleansing &amp; Radiance</figcaption></figure>
        <figure class="reveal"><img src="/public/images/salon-ambiance.jpg" alt="Modern Salon Floor &amp; Styling Stations" width="400" height="500" loading="lazy"><figcaption>Modern Salon Ambiance</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="section ink center">
    <div class="container">
      <p>See more real client work, stories &amp; updates on Instagram.</p>
      <a class="btn btn-gold" href="{e(CFG['instagramUrl'])}" data-bind-href="instagram" target="_blank" rel="noopener" data-analytics="instagram_click" data-analytics-label="gallery_page">Follow on Instagram</a>
    </div>
  </section>
'''
write("gallery/index.html", page(
    f"Gallery | {PRIMARY}, Patna",
    f"Real bridal, hair styling, facials, and grooming work from {PRIMARY}, Raja Bazar, Patna.",
    SITE + "/gallery/", "/gallery/", gallery_body,
    extra_head=ldjson(breadcrumb(("Gallery", "/gallery/")))
))

# ============================================================== ABOUT
about_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>About {e(PRIMARY)}</h1>
      <p class="lede">Artistry, elegance and personalized care in Raja Bazar, Sheikhpura, Patna.</p>
    </div>
  </section>

  <section class="section prose">
    <div class="container split">
{frames_block("Certified Artistry", "Modern Salon Ambiance", img_a="/public/hero.jpg", img_b="/public/images/salon-ambiance.jpg")}
      <div class="reveal">
        <p class="pull">A passion for beauty, certified by the best.</p>
        <p>{e(PRIMARY)} is a premier unisex salon at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar. Led by Parul Garg Makeup Academy alumna Puja Gupta, our specialty is bridal makeup and styling, alongside everyday beauty, hair and grooming services for the whole family.</p>
        <p>The salon previously traded as <a href="/shahnai-unisex-salon-patna/">{e(SECONDARY)}</a> &mdash; both names refer to the same salon at the same address; see that page for the full explanation.</p>
      </div>
    </div>

    <div class="container narrow mt-md">
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
