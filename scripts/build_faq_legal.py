import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import SITE, PRIMARY, SECONDARY, ldjson, breadcrumb, faqpage

# ============================================================== FAQ (full AEO set, section 37)
faqs = [
    (f"What is {PRIMARY}?",
     f"{PRIMARY} is a unisex salon and bridal makeup studio at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna."),
    (f"Where is {PRIMARY} in Patna?",
     f"Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014."),
    (f"Is {PRIMARY} a unisex salon?",
     "Yes. Alongside its bridal makeup specialty, the salon serves men, women and families with hairstyling, facials and grooming."),
    (f"Is {PRIMARY} the same place as {SECONDARY}?",
     f"Yes, according to the current operator. {SECONDARY} is an earlier name for the same salon at this Raja Bazar address, now operating as {PRIMARY}. See the <a href=\"/shahnai-unisex-salon-patna/\">full explanation</a>."),
    (f"Does {PRIMARY} offer bridal makeup?",
     'Yes \u2014 bridal, engagement and reception makeup, plus pre-bridal services. See the <a href="/bridal-makeup-patna/">bridal makeup page</a> and the <a href="/services/">services page</a> for current availability.'),
    ("Does the salon offer engagement makeup?",
     'Engagement makeup is offered where shown as active on the <a href="/services/">services page</a>, which reflects the salon\u2019s current offering.'),
    ("Does the salon offer bridal hairstyling?",
     "Bridal hairstyling is available as an add-on to a bridal booking, subject to current availability."),
    ("How do I book an appointment?",
     'Use the <a href="/book/">booking request form</a> \u2014 choose your service and preferred date. It takes under a minute.'),
    ("Is my appointment confirmed once I submit the form?",
     "No \u2014 submitting the form sends a request. The salon will contact you on WhatsApp or by phone to confirm the exact time before it\u2019s final."),
    ("How can I contact the salon?",
     'By phone, WhatsApp, or Instagram \u2014 see the <a href="/contact/">contact page</a> for current details.'),
    ("Do you serve customers from across Patna?",
     "Yes, the salon welcomes clients from across Patna and nearby areas. All services are provided at the Raja Bazar location."),
    ("How much do services cost?",
     'Prices are shown on the <a href="/services/">services page</a> where available. Where a price isn\u2019t listed, it shows as \u201cPrice on enquiry\u201d \u2014 ask us directly and we\u2019ll confirm it.'),
    ("Can I reschedule or cancel a request?",
     "Yes \u2014 call or WhatsApp the salon directly and mention your booking ID, name and date; there is no self-service rescheduling portal."),
    ("Does the salon accept online payment?",
     "Not at this time. Payment is handled directly with the salon."),
]

faq_items_html = "\n".join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
faq_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Frequently Asked Questions</h1>
    </div>
  </section>

  <section class="section faq">
    <div class="container narrow">
{faq_items_html}
    </div>
  </section>

  <section class="section ink center">
    <div class="container">
      <p>Still have a question?</p>
      <a class="btn btn-gold" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I have a question." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="faq_page">Ask on WhatsApp</a>
    </div>
  </section>
'''
write("faq/index.html", page(
    f"FAQ | {PRIMARY}, Patna",
    f"Answers about booking, services, pricing and location at {PRIMARY}, Raja Bazar, Patna.",
    SITE + "/faq/", "/faq/", faq_body,
    extra_head=ldjson(breadcrumb(("FAQ", "/faq/"))) + ldjson(faqpage(faqs))
))

# ============================================================== PRIVACY
privacy_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Privacy Policy</h1>
      <p class="muted">Last updated: <span data-year></span></p>
    </div>
  </section>
  <section class="section prose">
    <div class="container narrow">
      <p>This page explains, in plain language, what information {e(PRIMARY)} collects through this website and how it is used. It is a plain-language starting point, not a substitute for advice from a qualified professional on the law that applies to your business.</p>

      <h2>What we collect</h2>
      <p>When you submit a booking request, we collect your name, mobile number, chosen service and add-ons, preferred date and time, and any note you add. We do not ask for your email address, home address, age, gender or payment details on this site.</p>

      <h2>How it&rsquo;s used</h2>
      <p>This information is written to a private Google Sheet used only by the salon owner, so we can contact you on WhatsApp or by phone to confirm your appointment. If automatic WhatsApp notifications are enabled, your booking details are also sent, once, to our WhatsApp messaging provider for that purpose only.</p>

      <h2>Analytics and cookies</h2>
      <p>We use Google Analytics (GA4) and Microsoft Clarity to understand how the site is used, but only after you accept the cookie banner shown on your first visit &mdash; nothing loads before that. These tools never receive your name, mobile number or note text.</p>

      <h2>Storage and access</h2>
      <p>Booking requests are stored in a Google Sheet accessible only to the salon owner. We do not sell or share your information with third parties for marketing purposes.</p>

      <h2>Your choices</h2>
      <p>To ask what information we hold about you, or to request it be removed, contact us on WhatsApp or by phone using the details on the <a href="/contact/">contact page</a>.</p>
    </div>
  </section>
'''
write("privacy-policy/index.html", page(
    f"Privacy Policy | {PRIMARY}",
    f"How {PRIMARY} collects and uses information submitted through this website.",
    SITE + "/privacy-policy/", "/privacy-policy/", privacy_body
))

# ============================================================== TERMS
terms_body = f'''  <section class="section-sm ink">
    <div class="container narrow">
      <hr class="rule">
      <h1>Terms of Use</h1>
      <p class="muted">Last updated: <span data-year></span></p>
    </div>
  </section>
  <section class="section prose">
    <div class="container narrow">
      <p>These terms are a plain-language starting point for using this website, not a substitute for advice from a qualified professional on the law that applies to your business.</p>

      <h2>Booking requests</h2>
      <p>Submitting the booking form sends a request only. No appointment is confirmed until {e(PRIMARY)} contacts you directly to confirm the date, time and details.</p>

      <h2>Pricing</h2>
      <p>Prices shown on this site are set by the salon and may change. Where a price is not listed, it will be confirmed with you directly before your appointment.</p>

      <h2>Payments</h2>
      <p>This website does not process online payments. Payment is handled directly with the salon.</p>

      <h2>Cancellations and rescheduling</h2>
      <p>To cancel or reschedule a request, contact the salon by phone or WhatsApp using the details on the <a href="/contact/">contact page</a>.</p>

      <h2>Names and brand</h2>
      <p>{e(PRIMARY)} and {e(SECONDARY)} refer to the same salon at the same address; see the <a href="/shahnai-unisex-salon-patna/">explanation page</a> for details.</p>

      <h2>Content and images</h2>
      <p>Photography and content on this site belong to {e(PRIMARY)} and may not be reused without permission.</p>

      <h2>Contact</h2>
      <p>Questions about these terms can be sent to the salon by phone or WhatsApp.</p>
    </div>
  </section>
'''
write("terms/index.html", page(
    f"Terms of Use | {PRIMARY}",
    f"Terms of use for the {PRIMARY} website and booking request form.",
    SITE + "/terms/", "/terms/", terms_body
))

# ============================================================== 404
err_body = '''  <section class="err-page">
    <span class="wordmark reveal">Error 404</span>
    <h1>We couldn&rsquo;t find that page.</h1>
    <p class="lede">The page you&rsquo;re looking for may have moved. Try one of these instead.</p>
    <div class="actions center">
      <a class="btn btn-gold" href="/">Homepage</a>
      <a class="btn btn-dark" href="/services/">Services</a>
      <a class="btn btn-dark" href="/book/">Book Now</a>
    </div>
  </section>
'''
write("404.html", page(
    f"Page Not Found | {PRIMARY}",
    f"This page could not be found. Return to the {PRIMARY} homepage.",
    SITE + "/404.html", "", err_body, robots="noindex"
))

print("faq/privacy/terms/404 done")
