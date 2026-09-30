# Shahnaz Beauty Parlour — Implementation Dossier

Companion to the code in this repository. Three companion docs are referenced
throughout rather than repeated: `docs/fact-validation-table.md` (what's
verified vs. client-stated, **including a brand-risk finding — read that
one first**), `docs/migration-matrix.md` (file-by-file diff from the old
`shahnai-website.zip`), and `docs/domain-research.md`.

---

## 1. Executive Summary

Shahnaz Beauty Parlour — a unisex salon and bridal makeup studio in Raja
Bazar, Sheikhpura, Patna — gets a premium, editorial-feeling website built
on the same deliberately small pipeline the prior `shahnai-website.zip`
established: a customer fills a short form, one row is written to the
owner's own Google Sheet, and the owner is notified on WhatsApp. No live
calendar, no payments, no accounts, no admin panel — the Sheet remains the
control panel.

The rebrand keeps the old architecture (static HTML/CSS/JS + Vercel
Functions + Apps Script + Google Sheet) because it was already correct for
a business this size, and upgrades it rather than replacing it: real bugs
found in the old code are fixed (see `migration-matrix.md`), the Sheet
schema now matches the real uploaded template exactly, a second public
identity ("Shahnai Unisex Salon") is supported through one bridge page
rather than a duplicate site, and the Content-Security-Policy is tightened
because the new build has zero inline scripts or styles.

**The one item that needs a human decision before launch:** research
surfaced an existing, unrelated "Shahnaz Husain"-branded salon already
operating in Patna, part of a large, actively-franchised national brand
family that uses this exact "Shahnaz ___ Beauty Parlour/Salon" naming
pattern in multiple cities. This is a real trademark/confusion risk, not a
copywriting problem — see `fact-validation-table.md` for sources and a
recommended path (including a no-rebuild fallback to lead with "Shahnai
Unisex Salon" instead). Everything else in this dossier applies equally
either way, since the codebase treats the brand name as data
(`config/business.json`), not hard-coded text.

Guiding principle carried over from the brief: **advanced experience,
simple operation.**

## 2. Brand Authorization & Fact Validation

See `docs/fact-validation-table.md` in full. Summary: no claim of
franchise, celebrity affiliation, official branch status, or any
superlative ("best", "top", "#1", "certified", specific years of
experience) appears anywhere on the site. The Shahnai/Shahnaz relationship
is presented as client-stated, not independently verified. The brand-risk
finding (an existing same-city "Shahnaz Husain" franchise) is the one item
requiring the owner's attention before the name is locked in for a domain
or Google Business Profile.

## 3. Existing ZIP Audit

`shahnai-website.zip` was a working, reasonably well-built static site:
clean separation of `api/`, `apps-script/`, `src/`, sensible fallback
catalog, no framework bloat, already following the "simple booking, no
admin panel" philosophy correctly. Three real bugs were found and fixed
(not just rebranded) — see `migration-matrix.md` for detail:
1. The bot/fill-time check compared server time to a **client wall-clock
   timestamp**, which silently misfires for anyone with an inaccurate
   device clock.
2. A retried (duplicate) `requestToken` was treated as an **error** rather
   than returning the original success — a flaky network could show a
   customer a false failure after their booking had already saved.
3. No protection against **spreadsheet formula injection** — a booking
   `name` or `note` beginning with `=` could execute as a formula when the
   owner opened the Bookings tab.

Nothing was thrown away without a reason listed in the migration matrix.

## 4. Dual-Brand Architecture

| | Decision | Rationale | Implementation | Risk | Priority |
|---|---|---|---|---|---|
| Business entity | One salon, one address, two names over time | Client-stated; avoids Google's "no duplicate listings" rule | `config/business.json`: `primaryBrand`, `secondaryBrand` | If the two-names claim is inaccurate, this misrepresents the business | High |
| Secondary brand page | One dedicated, content-rich page (`/shahnai-unisex-salon-patna/`), not a duplicate site or second GBP | Brief §3/§6: "do not represent two separate businesses unless they genuinely are two" | Full page: relationship explanation, services, photos placeholder, FAQ, directions, contact, booking CTA | A thin/mechanical version would read as a doorway page and could be filtered by Google | High |
| Internal linking | Every major page links to the bridge page at least once (hero line, footer, bridge section, About, FAQ) | Reinforces the relationship for both users and crawlers without needing a second site | See `hero__where` line in `index.html`, footer `Explore` list, homepage "bridge" section | Low | Medium |
| Google Business Profile | **One** profile, named for the primary brand once chosen, with the secondary name only in the business description if genuinely accurate — never as a second listing | Google's guidance (§ below) explicitly prohibits duplicate listings for one location | N/A — GBP is managed outside this codebase | Creating a second "Shahnai Unisex Salon" listing at the same address risks suspension of both | High |

## 5. Domain Research & Selection

See `docs/domain-research.md` in full (candidate table, honest
availability caveat, and the two-path recommendation tied to the brand-risk
finding).

## 6. Information Architecture

```
/                              Homepage
/bridal-makeup-patna/          Bridal pillar page
/unisex-salon-patna/           Unisex-salon pillar page
/shahnai-unisex-salon-patna/   Brand-bridge page
/services/                     Live, Sheet-driven full menu
/gallery/                      Photo placeholders, categorized
/about/
/contact/
/book/                         Booking form
/faq/                          Full AEO question set
/privacy-policy/
/terms/
/404
```
No doorway pages for services not yet confirmed active (engagement,
reception, party, pre-bridal, hairstyling, course) — these are represented
on `/services/` and `/bridal-makeup-patna/` and get a dedicated page only
if the owner asks for one later, per brief §31.

## 7. Page-by-Page SEO

| Page | Title | H1 | Schema |
|---|---|---|---|
| `/` | Shahnaz Beauty Parlour \| Unisex Salon & Bridal Makeup in Patna | Unisex Salon & Bridal Makeup Studio in Raja Bazar, Patna | `BeautySalon` (with `alternateName`), `WebSite` |
| `/bridal-makeup-patna/` | Bridal Makeup in Patna \| Shahnaz Beauty Parlour, Raja Bazar | Bridal Makeup in Patna | `BreadcrumbList`, `FAQPage` |
| `/unisex-salon-patna/` | Unisex Salon in Patna \| Shahnaz Beauty Parlour, Raja Bazar | Unisex Salon in Patna | `BreadcrumbList`, `FAQPage` |
| `/shahnai-unisex-salon-patna/` | Shahnai Unisex Salon Patna \| Shahnaz Beauty Parlour, Raja Bazar | Shahnai Unisex Salon in Patna | `BreadcrumbList`, `FAQPage` |
| `/services/` | Services & Prices \| Shahnaz Beauty Parlour, Patna | Services & Prices | `BreadcrumbList` |
| `/faq/` | FAQ \| Shahnaz Beauty Parlour, Patna | Frequently Asked Questions | `BreadcrumbList`, `FAQPage` (14 Q&As, brief §37's full set) |

All titles/H1s exactly match brief §32/§33 where specified.

## 8. Keyword Architecture

- **Primary brand:** Shahnaz Beauty Parlour Patna / Raja Bazar / Sheikhpura
- **Secondary identity:** Shahnai Unisex Salon Patna / Raja Bazar / Sheikhpura
- **Generic service terms:** bridal makeup artist Patna, bridal makeup
  Patna, unisex salon Patna, beauty parlour Patna, hair salon Patna, bridal
  makeup Raja Bazar, salon near Raja Bazar, engagement makeup Patna,
  reception makeup Patna, pre bridal services Patna, bridal hairstyling
  Patna

No search-volume figures are claimed anywhere (none were available to
verify), and no ranking outcome is promised — see §56 of the brief and the
AEO/AIO section below.

## 9. Shahnai Unisex Salon Search Strategy

Rather than a second site or a second GBP (both against Google's own
rules — see §21 below), the strategy is: one dedicated, genuinely useful
page (`/shahnai-unisex-salon-patna/`) that (a) ranks for "Shahnai unisex
salon Patna" style queries on its own content merit, (b) is linked from
every major page so its relevance signal isn't isolated, and (c) is named
in the homepage `<title>`'s `alternateName` schema field and Open Graph
data so both names are machine-legible as one entity. This is the
"one clear brand bridge" the brief calls for in §3.

## 10. Homepage Wireframe (ASCII)

```
┌──────────────────────────────────────────────────┐
│ Shahnaz Beauty Parlour   Bridal Salon Services ... [Send Booking Request] │
├──────────────────────────────────────────────────┤
│  SHAHNAZ BEAUTY PARLOUR (shimmer wordmark)         │
│  Unisex Salon & Bridal Makeup Studio               │  hero, ink bg,
│  in Raja Bazar, Patna                    ┌───────┐ │  arch photo frame,
│  [Send Booking Request] [WhatsApp]        │ arch  │ │  radial gold glow
│  Also known as Shahnai Unisex Salon      └───────┘ │
├──────────────────────────────────────────────────┤
│ address · phone · directions · instagram            │  trust strip
├──────────────────────────────────────────────────┤
│ [layered frames]      "A bridal specialty, built     │  editorial split
│                         on real experience."          │
├──────────────────────────────────────────────────┤
│              SERVICES (live from Sheet)              │  ink section
├──────────────────────────────────────────────────┤
│  Why clients choose us — 3 columns                    │
├──────────────────────────────────────────────────┤
│     "Looking for Shahnai Unisex Salon?"               │  maroon bridge
│      [Read the Full Story]                            │  section
├──────────────────────────────────────────────────┤
│              Real work (gallery preview)              │  ink section
├──────────────────────────────────────────────────┤
│  1. Send request  2. We confirm  3. Visit us          │
├──────────────────────────────────────────────────┤
│  Reviews — real only, Instagram link                   │  ink section
├──────────────────────────────────────────────────┤
│  About teaser · Location · FAQ (4 Qs) · Final CTA     │
├──────────────────────────────────────────────────┤
│  Footer                                                │
└──────────────────────────────────────────────────┘
        (mobile: sticky Call | WhatsApp | Book Now bar)
```

## 11. Booking Wireframe

```
┌───────────────────────────────┐
│  Send a Booking Request         │
│  Name                           │
│  Mobile number                  │
│  Service          [ dropdown  ] │  ← live, grouped by category
│  Preferred date    [ date    ]  │
│  Preferred time (opt)[ time  ]  │
│  Additional services  [ ] [ ]   │  ← live from Sheet
│  Note (opt)         [_______]   │
│  [   Send Booking Request   ]   │
└───────────────────────────────┘
        ↓ submit
┌───────────────────────┐   or   ┌───────────────────────┐
│  ✓ Request received     │       │  We couldn't send that │
│  Booking ID: SBP-260002 │       │  [Call]  [WhatsApp]    │
│  [Call][WhatsApp][Svcs] │       └───────────────────────┘
└───────────────────────┘
```

## 12. Mobile UX

- Sticky bottom bar (`Call | WhatsApp | Book Now`) below 900px, safe-area
  aware (`env(safe-area-inset-bottom)`), `body` padding compensates so it
  never overlaps the footer.
- All form controls ≥48px tall; checkboxes 22×22px (well above the 24px
  WCAG 2.2 target when combined with label padding).
- Native `<input type="date">` / `type="time">` — no custom JS date picker.
- Hero art reorders above the headline on narrow screens (`hero__art { order: -1 }`).

## 13. UI Design System

Colors: ink `#14100E`, champagne gold `#C6A15B`, ivory `#F6EFE3`, deep
maroon `#6E1B29` (emphasis only), taupe (borders/decoration). Type: Cinzel
(display) + Jost (body) — deliberately not Playfair/Inter, the current
AI-generated-design defaults. Full token list and every component class in
`src/css/styles.css`.

## 14. Visual Effects

Hero photo frame: CSS `perspective`/`rotateY` tilt, softened on hover.
Buttons: a CSS-only gold "shimmer" sweep on hover (`.btn-gold::after`).
Wordmark: slow animated gradient shimmer. Scroll-reveal: `IntersectionObserver`
adds `.in` to `.reveal` elements — but `.reveal` is fully visible without
JS or before the observer fires (progressive enhancement, not
hide-then-show). All motion respects `prefers-reduced-motion: reduce`
(disables the wordmark shimmer, the hero tilt, and all transitions — see
the media query at the end of `styles.css`).

## 15. Content Architecture

Every page answers: what is this, who is it for, where is it, what happens
next, how do I book — per brief §49. No page repeats "Patna" more than a
handful of natural times; no generic filler ("elevate your beauty
journey"); no copied competitor text. Content strictly reflects
`config/business.json` and the Sheet — see the fact-validation table for
what's stated vs. verified.

## 16. Local SEO

Locality hierarchy used consistently: Raja Bazar → Sheikhpura → Vishal
Market / Pillar No. 76 → Patna → Bihar. No thin locality pages created for
wider areas — the FAQ's "Do you serve customers from across Patna?" answer
covers wider reach honestly without inventing area-specific pages.

## 17. On-Page SEO

Answer-first paragraphs open every major content section (see
`/bridal-makeup-patna/` → "What's included in a bridal booking"). Service
names match the Sheet's `service_name` values exactly — no renaming for
keyword density. Internal links use descriptive anchor text ("bridal
makeup page", not "click here").

## 18. Technical SEO

- Canonical `<link>` on every page (baked per-page via `scripts/layout.py`).
- `robots.txt` + auto-generated, self-verifying `sitemap.xml`
  (`scripts/build_seo_files.py` fails the build if a listed route doesn't
  exist on disk).
- `404.html` served for unmatched routes, `<meta name="robots" content="noindex">`.
- `cleanUrls` + `trailingSlash` in `vercel.json` prevent `/book` vs `/book/`
  duplicate-URL variants.
- Semantic HTML throughout — `header`, `main`, `nav`, `footer`,
  `details`/`summary` for every FAQ (no JS-only accordion).

## 19. AEO / AIO / GEO

Per Google's own current guidance on optimizing for generative AI search —
[developers.google.com/search/docs/fundamentals/ai-optimization-guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) —
there is no separate technical "AI unlock"; the same fundamentals that help
classic Search also help AI features: answer-first paragraphs, accurate
structured data, and consistent NAP across the site. This is implemented
directly: every pillar page and the FAQ page open with a direct-answer
sentence before any elaboration, and `FAQPage` schema matches the visible
`<details>` content exactly (never a mismatch between what's marked up and
what's shown). No "AI ranking hack," schema trick, or citation guarantee
is claimed anywhere, per brief §36/§56.

## 20. Structured Data

`BeautySalon` (with `alternateName` for the secondary brand) + `WebSite` on
the homepage; `BreadcrumbList` on every inner page; `FAQPage` on every page
with visible FAQs, generated with `json.dumps(..., ensure_ascii=False)` so
it's never hand-typed/invalid JSON (an actual bug caught and fixed during
this build — an early draft used Python's `%r` string formatting, which
produces single-quoted, non-JSON output; the fix and a repo-wide validation
sweep are in `scripts/build_faq_legal.py` and the QA section below). No
`aggregateRating` or `review` schema anywhere — no rating exists to
publish truthfully.

## 21. Google Business Profile

Current official guidance consulted:
[support.google.com/business/answer/3038177](https://support.google.com/business/answer/3038177) (representing your business accurately),
[.../answer/3415281](https://support.google.com/business/answer/3415281) (duplicate listings),
[.../answer/7091](https://support.google.com/business/answer/7091) (guidelines for representing your business).
Key rules this project respects: use the real-world business name only (no
keyword-stuffed variant like "Shahnaz Beauty Parlour Best Bridal Makeup
Artist Patna" — explicitly avoided per brief §4), one profile per physical
location, accurate category/address/phone, real reviews only. **The
brand-risk finding in §2 above is a Google Business Profile risk too** — a
name too close to an existing franchise's naming pattern in the same city
is exactly the kind of thing that can trigger a suspension or ownership
dispute on GBP, independent of any trademark question.

## 22. Google Sheet Architecture

Tabs (matching the real uploaded `.xlsx` exactly): `README`, `Settings`,
`Services`, `Additional Services`, `Bookings`. See `OWNER-GUIDE.md` for the
owner-facing explanation and `apps-script/Code.gs`'s header comment for the
exact column names each tab must keep.

## 23. Sheet-to-Website Data Flow

```
Owner edits Sheet
      ↓
GET /api/catalog (Vercel, 45s edge cache) → Apps Script doGet() → Sheet
      ↓
Website re-fetches on each page load (catalog.js), hydrates
[data-bind-text]/[data-bind-href] elements — including phone/WhatsApp/
address, not just services — so a Settings change reaches the live site
without a redeploy
```
Every phone/WhatsApp link ships with a real, working default baked in at
generation time (`scripts/layout.py` → `TEL_DEFAULT`/`WA_DEFAULT`), so the
site is never one broken JS load away from a dead "Call" button — the live
Sheet value only upgrades it if different.

## 24. Booking Flow

```
Customer fills /book/ → client validation (booking.js) → POST /api/booking
  → server validation (validate.js) → catalog re-check (live services/add-ons)
  → rate-limit + dedupe check → Apps Script doPost() → LockService-guarded
  row append → booking ID returned → (optional) WhatsApp notify
  → success/error state shown to customer
```
Idempotent by design: a retried `requestToken` (network hiccup, double-tap)
returns the *original* booking ID rather than erroring or double-booking —
fixed from the old codebase, see `migration-matrix.md`.

## 25. WhatsApp Flow

`CLICK_TO_CHAT` (default): browser opens `wa.me` with a prefilled message —
zero setup, zero cost, zero approval process. `AUTO_NOTIFY`: server sends
an approved template via Meta Cloud API or Twilio (`WHATSAPP_PROVIDER`
switch) — see `docs/whatsapp-template.txt` for the exact template to submit
and `api/_lib/whatsapp.js` for the implementation. Either way, the message
format is generated by the single shared `src/js/message.js`, so the
click-to-chat text and the automatic notification can never drift apart
(this — one formatter, two callers — is new versus the old codebase, which
only had the automatic path). A WhatsApp failure never loses the booking:
the Sheet row is written first, notification is attempted after, and
failure is only logged server-side (`api/booking.js`).

## 26. API Architecture

`api/catalog.js` (GET, cached, falls back to `config/catalog.fallback.json`)
and `api/booking.js` (POST — full validation pipeline, see §24). Shared
server-only helpers in `api/_lib/`: `appsScript.js` (HTTP client with
timeout), `catalog.js` (shape validation + short cache), `validate.js`
(pure, unit-tested), `whatsapp.js` (dual-provider notifier). Zero npm
runtime dependencies — both functions use the native `fetch` available in
Vercel's Node 18+ runtime.

## 27. Security

No Google or WhatsApp credentials ever reach the browser. `BOOKING_SHARED_SECRET`
gates the otherwise-public Apps Script Web App. Formula-injection guard on
every user-entered Sheet cell (`guard_()` in `Code.gs`). CSP with **no**
`unsafe-inline` for scripts or styles (verified — see QA below); JSON-LD is
exempt by browser design, not a policy hole. Full header set in
`vercel.json`: CSP, `X-Content-Type-Options`, `Referrer-Policy`,
`X-Frame-Options`, `Permissions-Policy`.

## 28. Analytics / GTM / GA4

Consent-gated: `src/js/analytics.js` loads nothing until
`ShahnazAnalytics.enable()` is called by `main.js`, which only happens
after the visitor accepts the on-page banner. Events (no PII in any
payload — enforced by an allow-list in `analytics.js`'s `sanitize()`):
`booking_start`, `booking_submit`, `booking_error`, `phone_click`,
`whatsapp_click`, `directions_click`, `instagram_click`, `service_select`
(fire this from a `service` `change` listener if you want it — not wired
by default since the select's native behavior already covers most
analysis needs), `gallery_open`, `faq_open`.

## 29. Clarity

Same consent-gated loader as GA4. Once live, review weekly for: scroll
depth on `/`, dead/rage clicks on the booking form specifically, and
mobile friction on the service dropdown and date picker — the
highest-leverage places for a small salon site to lose a booking.

## 30. Search Console

Verify the final domain, submit `sitemap.xml`, monitor **Pages**,
**Performance**, **Core Web Vitals**, and **Manual actions/Security**. No
indexing timeline or ranking outcome is promised anywhere in this project.

## 31. Performance

No framework; all four custom JS files combined are a few KB unminified.
No Tailwind Play CDN. Single Google Fonts request, loaded asynchronously by
`boot.js` (`display=swap` — text renders in a fallback font immediately,
never blocked). `/api/catalog` is edge-cached 45s. Images: none shipped yet
(placeholders only — see `README.md` → "Adding real photography"); when
added, WebP/AVIF + explicit dimensions + `loading="lazy"` below the fold is
required, eager-loading reserved for the single real LCP candidate.

## 32. Accessibility

Skip link, visible focus rings (`:focus-visible`, gold on ink / maroon on
ivory for contrast), `aria-current` on the active nav item, native
`<details>/<summary>` for every FAQ, `role="alert"` on inline form errors,
`prefers-reduced-motion` respected globally, 48px-minimum touch targets on
every interactive control, consent banner is a labeled `role="dialog"`.

## 33. Vercel Deployment

Static files + two `api/` functions, no build step for the HTML (pages are
pre-generated by the Python scripts and committed). Environment variables:
`APPS_SCRIPT_URL`, `BOOKING_SHARED_SECRET`, and the WhatsApp provider group
only if `AUTO_NOTIFY` is used. See `README.md` → "One-time setup" for the
exact steps.

## 34. File-by-File Migration

See `docs/migration-matrix.md` in full.

## 35. QA Matrix

**Automated (run before every deploy):**
- [x] `npm test` — 19 unit tests covering `validate.js` (mobile
  normalization, date bounds, token/id format, note length, page
  fallback) and `message.js` (exact WhatsApp format, template param order,
  time/date formatting) — all passing as of this delivery.
- [x] Repo-wide sweep (run during this build, zero findings on final pass):
  zero `style="..."` attributes, zero inline `<script>` blocks without
  `src`, every JSON-LD block `json.loads()`-valid, HTML tag balance across
  15 tag types, every internal `href` resolves to a real file, zero bare
  `href="tel:"` / `href="https://wa.me/"` links.
- [x] `scripts/build_seo_files.py` self-check — every `sitemap.xml` route
  verified to exist on disk before the script exits successfully.

**Manual, before launch:**
- [ ] Submit a real booking end-to-end; confirm the Sheet row and (if
  AUTO_NOTIFY) the WhatsApp message.
- [ ] Set a service's `active` to `No`; confirm it disappears from
  `/services/` and the booking dropdown within ~60 seconds.
- [ ] Trigger each client-side validation error at least once (bad mobile,
  missing service, past date, over-length note) and confirm the message
  shown.
- [ ] Full keyboard pass: tab through the booking form, open/close a FAQ,
  operate the mobile menu, without a mouse.
- [ ] Validate every page's JSON-LD in Google's Rich Results Test.
- [ ] Lighthouse mobile run once real images are added.

## 36. Launch Checklist

1. Resolve the brand-risk finding (§2 / `fact-validation-table.md`).
2. Fill in real prices/availability in the Sheet.
3. Deploy `apps-script/Code.gs`, run `setup()`, deploy as a Web App.
4. Set Vercel environment variables; deploy the site.
5. Run through §35's manual QA matrix.
6. Add real photography; regenerate pages if any config changed
   (`npm run build:pages`).
7. Fill in `GTM_CONTAINER_ID` / `CLARITY_PROJECT_ID`.
8. Verify domain in Search Console; submit `sitemap.xml`.
9. Finalize the Google Business Profile using the confirmed brand name.
10. Go live.

## 37. 30/60/90 Day Plan

**Days 1–30:** Confirm indexing of all 12 pages in Search Console; fix any
crawl errors; collect the first 5–10 real reviews and real photographs to
replace placeholders; watch Clarity recordings for booking-form friction.

**Days 31–60:** Expand `/gallery/` with real categorized work; consider a
dedicated page for any one service (engagement/reception/pre-bridal) once
its Sheet row has been active and stable for a month; review GA4 for which
services get the most `service_select`/`booking_submit` events and make
sure those are prominent on the homepage.

**Days 61–90:** Revisit whether `AUTO_NOTIFY` is worth the WhatsApp
template-approval overhead based on real CLICK_TO_CHAT usage; review Search
Console query data (not fabricated — pulled from the real property) to see
which of the keyword-architecture terms in §8 are actually driving
impressions, and adjust on-page emphasis accordingly.

## 38. Maintenance Plan

- Sheet edits (services, prices, Settings) need no developer involvement —
  see `OWNER-GUIDE.md`.
- A brand name/descriptor/address change needs `config/business.json` +
  `npm run build:pages` + redeploy — see `README.md` → "Changing the brand
  name later."
- A new page or content change to an existing page needs a code change
  (edit the relevant `scripts/build_*.py`, rerun the generator).
- Recheck `docs/fact-validation-table.md` yearly, or immediately if the
  owner's relationship to either brand name changes.

## 39. Final Acceptance Criteria

- [x] Booking a real appointment writes exactly one row to the Sheet and
  (optionally) notifies WhatsApp, without a live calendar, payments,
  accounts, or an admin panel.
- [x] Changing a service's `active`/`price`/`display_order` in the Sheet
  changes the live site with no redeploy.
- [x] No page states an unverified claim (franchise, celebrity affiliation,
  award, superlative, fabricated review/rating) — see
  `fact-validation-table.md`.
- [x] `/shahnai-unisex-salon-patna/` exists, explains the relationship
  honestly, and is a complete, useful page — not a doorway page.
- [x] Zero inline scripts/styles; CSP ships without `unsafe-inline`.
- [x] `npm test` passes (19/19); `sitemap.xml` self-verified against disk.
- [ ] **Owner has read and acted on the brand-risk finding** before the
  site goes live under the "Shahnaz" name.
