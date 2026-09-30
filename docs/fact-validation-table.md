# Fact Validation Table

**Read this first: a same-city naming conflict was found during research — see the
flagged row below and the "Critical brand-risk finding" section beneath the table.
This affects the recommended brand decision, not just a minor detail.**

Every row below is a claim that appears (or could appear) on the website.
"Verified?" reflects what evidence has actually been supplied in this
project, not what is presumed true. Nothing marked "No" should be published
as an unqualified fact until it is verified — see the "Safe to publish?"
column for exactly how each one is currently handled.

| # | Claim | Evidence needed | Verified? | Safe to publish? |
|---|---|---|---|---|
| 1 | Business trades as "Shahnaz Beauty Parlour" | Signage, GST/shop registration, or owner confirmation in writing | **No** — client-stated only | Yes, as the operating name (this is how a business simply describes itself); not published as a claim that requires third-party proof — **but see the brand-risk finding below before finalizing this name** |
| 2 | "Shahnaz Beauty Parlour" and "Shahnai Unisex Salon" are the same salon at the same address, not two businesses | Owner's own statement (received); ideally also matching signage/GBP history | Client-stated, **not independently verified** | Yes, but phrased throughout as "according to the current operator" / "the salon previously traded as" — never stated as independently confirmed fact. See `/shahnai-unisex-salon-patna/` |
| 3 | The salon is an authorized Shahnaz Husain franchise, official branch, or has any affiliation with the Shahnaz Husain company/brand | A signed franchise agreement or written authorization from Shahnaz Husain Group | **No evidence supplied — and see finding below** | **No.** Nothing on this site claims or implies this. If the owner does hold such an agreement, request the document before adding any franchise/authorization language |
| 4 | Address: Vishal Market, near Pillar No. 76, Sheikhpura, Raja Bazar, Patna, Bihar 800014 | Owner confirmation / matches Google Maps listing | Client-provided | Yes — published as given; owner should double check it matches the Google Business Profile address exactly before launch |
| 5 | Phone +91 76458 12695 (primary), +91 75468 63963 (secondary/WhatsApp) | Owner confirmation | Client-provided (corrected mid-project — see migration matrix) | Yes, as provided |
| 6 | Instagram `@pujaguptamakeup` is the salon's official account | Confirm the account still exists and is actively managed by the owner | **Not reverified this session** | Yes, carried over as given, but the owner should reconfirm this is still the correct, active handle before launch |
| 7 | Services offered (bridal, engagement, reception, party, pre-bridal, hair, facial, grooming, course) | Owner confirmation per service | Client-provided starter list | Yes, with `active`/`price_type` left as "Enquiry"/blank where no price was given — never a fabricated number |
| 8 | Any price | Owner-entered figure in the Sheet | Not supplied | Site shows "Price on enquiry" until the owner fills in a real number |
| 9 | Reviews / testimonials | Real, unedited reviews from the owner | None supplied | Site links to Instagram/Google for real reviews; no review text is invented anywhere (see homepage reviews section) |
| 10 | Superlatives ("best", "top", "#1", "award-winning", "certified", "most trusted", "L'Oréal", "HD", "airbrush", specific "years of experience") | Independent, checkable proof for each specific claim | Not supplied | **None used anywhere on the site.** If the owner wants to add any of these later, each one needs its own evidence before publishing (see brief §56) |

## Critical brand-risk finding (please read before launch)

A web search for this project turned up **an existing, unrelated business
already trading in Patna as "Shahnaz Husain & Loreal Professional Beauty
Clinic"**, at Panchmukhi Hanuman Mandir Chauraha, East Boring Canal Road,
Kidwaipuri, Patna 800001 — a different address from this salon's Raja Bazar
location. ([source](https://www.weddingwire.in/makeup-salon/shahnaz-husain-%26-loreal-professional-beauty-clinic--e185319))

This is very likely a licensed franchise of **The Shahnaz Husain Group** —
the Padma Shri-awarded, internationally known beauty brand founded by
Shahnaz Husain, which operates over 400 franchise salons, spas and training
academies worldwide under names that all lead with "Shahnaz"
([Wikipedia](https://en.wikipedia.org/wiki/Shahnaz_Husain);
[company profile](https://theceomagazine.com/executive-interviews/healthcare-pharmaceutical/shahnaz-husain)).
The same search turned up this exact naming pattern — "Shahnaz [something]
Beauty Parlour/Salon" — franchised in multiple other cities (Jaipur,
Lucknow, Gorakhpur, Howrah), confirming this is an actively used,
recognizable brand family, not a coincidence of a common personal name.

**Why this matters for this project specifically:**
- The brief's own instruction — never publish "authorized franchise,"
  "official branch," or "celebrity affiliation" without evidence — is
  handled correctly on this site (no such claim appears anywhere). But the
  *name itself*, "Shahnaz Beauty Parlour," is close enough to this existing
  naming family that customers, Google, or the Shahnaz Husain Group itself
  could reasonably read it as connected to that franchise network, even
  with no such claim stated in the copy.
- There is a **same-city, same-industry, similarly-named existing
  business**. That is a materially different (and larger) risk than the
  "different Bihar business using shahnazbeautyparlour.in" the brief
  already flagged — this one is in Patna itself.
- This is a trademark/passing-off and customer-confusion question, which is
  a legal judgment call, not an SEO or copywriting one. It should not be
  decided by an AI assistant or resolved by careful wording alone.

**Recommendation:** before registering a domain, creating a Google Business
Profile, or ordering signage under "Shahnaz Beauty Parlour," the owner
should have a local advocate/trademark professional do a quick clearance
check, and separately confirm directly whether they have any formal
relationship with the Shahnaz Husain Group. If the answer is no relationship
exists, the lowest-risk path is a name that does not lead with "Shahnaz" —
for instance keeping **Shahnai Unisex Salon** as the primary public brand
(it does not collide with the pattern above), or another distinct name of
the owner's choosing. The site and Sheet in this delivery are built around
a central `config/business.json` and `Settings` tab specifically so that
swapping the primary brand name later is a data change, not a rebuild — see
`README.md` → "Changing the brand name later."

## What this means for launch

Before going live, the owner (or whoever manages the Google Business Profile)
should:
1. **Resolve the brand-risk finding above** — this comes first, before any
   domain purchase or signage order.
2. Confirm item 2 is accurate as understood — the wording on
   `/shahnai-unisex-salon-patna/` should match how the owner actually wants
   the relationship explained.
3. Reconfirm items 4–6 (address, phones, Instagram) against the current
   Google Business Profile so every channel matches exactly (Google's own
   guidance treats mismatched NAP details across the web as a ranking and
   trust problem — see `docs/strategy-dossier.md` → "Google Business Profile").
4. If a genuine Shahnaz Husain franchise agreement exists, share it before
   any franchise/authorization language is added anywhere.

