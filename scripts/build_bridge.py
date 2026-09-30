import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from layout import CFG, page, write, addr_line, e
from shared_blocks import SITE, PRIMARY, SECONDARY, ldjson, breadcrumb, faqpage, frames_block, faq_block

bridge_faqs = [
    (f"Is {SECONDARY} the same place as {PRIMARY}?",
     f"Yes. According to the current operator, {SECONDARY} is an earlier, informal name that regulars still use for the same salon at this Raja Bazar, Sheikhpura address, which now operates under the name {PRIMARY}."),
    ("Why does the salon have two names?",
     f"The business has traded under {SECONDARY} in the past. {PRIMARY} is the name currently in use for the salon at this location. Both names refer to one salon, not two separate businesses."),
    ("Where is the salon located?",
     f"Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014 \u2014 the same address for both names."),
    ("Does this salon offer bridal makeup?",
     "Yes \u2014 bridal, engagement and reception makeup, pre-bridal services, and bridal hairstyling and draping as add-ons. See the bridal makeup page for details."),
    ("How do I book an appointment here?",
     'Use the booking request form with your preferred date and service. The salon will contact you on WhatsApp or by phone to confirm.'),
]

body = f'''  <section class="hero section-sm">
    <div class="container narrow">
      <span class="wordmark reveal">A Note on Our Name</span>
      <h1 class="reveal">{e(SECONDARY)} in Patna</h1>
      <p class="lede reveal">If you know this salon as <strong>{e(SECONDARY)}</strong>, you&rsquo;re in the right place. The salon at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar now operates as <strong>{e(PRIMARY)}</strong> &mdash; same salon, same address, same team.</p>
      <div class="actions reveal">
        <a class="btn btn-gold" href="/book/" data-analytics="booking_start" data-analytics-label="bridge_page">Send Booking Request</a>
        <a class="btn btn-line" href="https://wa.me/" data-bind-href="whatsapp" data-wa-text="Hi, I know this salon as Shahnai Unisex Salon - I'd like to ask about an appointment." target="_blank" rel="noopener" data-analytics="whatsapp_click" data-analytics-label="bridge_page">Ask on WhatsApp</a>
      </div>
    </div>
  </section>

  <section class="section prose">
    <div class="container narrow">
      <h2>The relationship between the two names</h2>
      <p>{e(SECONDARY)} was the name many regulars and long-time clients know this salon by. The salon at this Raja Bazar, Sheikhpura location now operates and is promoted under the name <strong>{e(PRIMARY)}</strong>, as confirmed by the current operator. If you searched for {e(SECONDARY)} and landed here, this is the same salon &mdash; not a different business, and not a franchise or branch of any other company by either name.</p>
      <p class="muted small">This page states the relationship as described by the salon&rsquo;s current operator. It is kept here specifically so that {e(SECONDARY)} does not become two conflicting listings online.</p>

      <h2>What the salon offers</h2>
      <p>Unisex services &mdash; hairstyling, facials and men&rsquo;s grooming &mdash; alongside a bridal makeup specialty: bridal, engagement and reception makeup, pre-bridal services, and add-ons like bridal hairstyling and draping. The current, always-up-to-date list is on the <a href="/services/">services page</a>.</p>
    </div>
  </section>

  <section class="section ink">
    <div class="container split">
{frames_block("Salon", "Bridal work")}
      <div class="reveal">
        <p class="pull">One salon. One address. Two names, over time.</p>
        <p class="muted">Real photography of the salon and its work goes here once supplied &mdash; nothing on this page is stock imagery presented as the salon&rsquo;s own.</p>
        <div class="actions">
          <a class="btn btn-line" href="/bridal-makeup-patna/">Bridal Makeup</a>
          <a class="btn btn-line" href="/unisex-salon-patna/">Unisex Salon Services</a>
        </div>
      </div>
    </div>
  </section>

{faq_block(bridge_faqs, anchor="bridge-faq")}
  <section class="section ink">
    <div class="container">
      <div class="head"><hr class="rule"><h2>Visit Us</h2><p class="muted" data-bind-text="address">{e(addr_line())}</p></div>
      <div class="actions">
        <a class="btn btn-gold" href="{e(CFG['mapsUrl'])}" data-bind-href="maps" target="_blank" rel="noopener" data-analytics="directions_click" data-analytics-label="bridge_page">Get Directions</a>
        <a class="btn btn-line" href="/contact/">Contact Details</a>
      </div>
    </div>
  </section>
'''

write("shahnai-unisex-salon-patna/index.html", page(
    f"{SECONDARY} Patna | {PRIMARY}, Raja Bazar",
    f"Looking for {SECONDARY} in Patna? This is {PRIMARY} at Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar \u2014 same salon, current name.",
    SITE + "/shahnai-unisex-salon-patna/", "/shahnai-unisex-salon-patna/", body,
    extra_head=ldjson(breadcrumb((SECONDARY + " in Patna", "/shahnai-unisex-salon-patna/"))) + ldjson(faqpage(bridge_faqs))
))
print("brand-bridge page done")
