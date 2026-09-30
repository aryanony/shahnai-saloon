# Shahnaz Beauty Parlour — Website + Booking Pipeline

**Before anything else, read `docs/fact-validation-table.md`.** Research
turned up a same-city naming conflict with an existing "Shahnaz Husain"
franchise salon in Patna. It doesn't block this delivery, but it should be
resolved before the "Shahnaz" name goes on a domain, a Google Business
Profile, or signage. `docs/domain-research.md` gives a concrete fallback
(lead with "Shahnai Unisex Salon" instead) that needs no rebuild — see
"Changing the brand name later" below.

```
Customer fills form  →  Vercel Function (validates)  →  Apps Script  →  Google Sheet row
                                                              ↓
                                                     WhatsApp notification
                                                     (CLICK_TO_CHAT or AUTO_NOTIFY via Meta/Twilio)
```

No React, no build step for the pages themselves (they're pre-generated
HTML — see below), no database beyond the Google Sheet, no admin panel.
See `docs/strategy-dossier.md` for the full strategy, SEO, analytics,
testing and launch plan, and `docs/migration-matrix.md` for exactly what
changed from the previous `shahnai-website.zip` codebase and why.

## Project layout

```
config/business.json     Single source of truth: brand names, address, phones, URLs
config/catalog.fallback.json  Starter services/add-ons used if the Sheet is unreachable
scripts/                 Python page generator — regenerate every page from config/business.json
  layout.py                header/footer/nav/consent-banner/sticky-bar + write() (bakes tel:/wa.me defaults)
  shared_blocks.py         reusable sections (hero arch, steps, FAQ, schema helpers)
  build_*.py                one script per page group
  build_seo_files.py        generates sitemap.xml and self-checks every route exists
src/css/styles.css       Hand-authored design system — zero inline styles anywhere (see CSP note below)
src/js/                  boot.js, main.js, catalog.js, booking.js, analytics.js, home.js, services.js, message.js
api/                      Vercel Functions: catalog.js, booking.js, health.js
api/_lib/                 Server-only helpers: appsScript.js, catalog.js, validate.js, whatsapp.js
apps-script/Code.gs       The only code that touches the Sheet directly
tests/                    Node's built-in test runner — pure-logic unit tests (validate.js, message.js)
docs/                     fact-validation-table.md, domain-research.md, migration-matrix.md,
                           whatsapp-template.txt, strategy-dossier.md
sheet/                    A copy of the Sheet template used to build this repo, for reference
```

## One-time setup

### 1. Google Sheet
Open `sheet/shahnaz_beauty_parlour_simple_booking_google_sheet_template.xlsx`
in Google Sheets (or upload it) — it already matches the schema this code
expects (`Settings`, `Services`, `Additional Services`, `Bookings`). Fill in
real prices where known; leave blank for "Price on enquiry".

### 2. Apps Script
1. In the Sheet: **Extensions → Apps Script**.
2. Paste in `apps-script/Code.gs`.
3. Open `setup()`, run it once (creates and logs `BOOKING_SHARED_SECRET` in
   Script Properties — copy the logged value).
4. **Deploy → New deployment → Web app**. Execute as **Me**, access **Anyone**.
5. Copy the `/exec` URL.
6. After any future code change: **Deploy → Manage deployments → Edit → New version.**

### 3. Vercel
1. Import this repo (framework preset: **Other** / static).
2. Set environment variables from `.env.example`:
   `APPS_SCRIPT_URL`, `BOOKING_SHARED_SECRET`, and only if using
   `WHATSAPP_MODE = AUTO_NOTIFY`: `WHATSAPP_PROVIDER` plus either the
   Meta or Twilio variable group.
3. Deploy.

### 4. WhatsApp (optional — CLICK_TO_CHAT needs none of this)
See `docs/whatsapp-template.txt` for the exact template text to submit for
approval with either provider before switching `Settings!WHATSAPP_MODE` to
`AUTO_NOTIFY`.

### 5. Analytics (optional)
Fill in `GTM_CONTAINER_ID` and `CLARITY_PROJECT_ID` in `src/js/analytics.js`.
Both loaders stay inert until a visitor accepts the on-page consent banner —
nothing is tracked before that, by design.

### 6. Search Console
Verify the domain, submit `https://<your-domain>/sitemap.xml`, then watch
**Pages** and **Core Web Vitals** over the following weeks.

## Regenerating the pages

Every page is pre-built static HTML, generated from `config/business.json`
so brand/address/phone changes only need editing one file and re-running:

```
npm run build:pages
```

This also regenerates `sitemap.xml` and fails loudly if any route it lists
doesn't actually exist on disk — see `scripts/build_seo_files.py`.

## Changing the brand name later

Because every page reads from `config/business.json` at generation time
(not hand-edited per file), swapping which name leads is a data change:

1. Edit `config/business.json` — swap `primaryBrand` and `secondaryBrand`
   (and `descriptor`/`siteUrl` if needed).
2. Edit `Settings!PRIMARY_BRAND` / `SECONDARY_BRAND` in the live Sheet to match.
3. Run `npm run build:pages`.
4. Redeploy.

No page's HTML needs manual editing for a brand-name change. See
`docs/domain-research.md` → "Path B" for why this might be worth doing.

## Running the tests

```
npm test
```

Covers the pure validation logic (`api/_lib/validate.js`) and the WhatsApp
message formatter (`src/js/message.js`) — the two places a subtle bug would
most directly cost a real booking or send a malformed owner notification.
`api/booking.js` itself is integration-tested manually per the launch
runbook (`docs/strategy-dossier.md` → "Launch Runbook", step 5): submit one
real booking end-to-end before going live.

## Local development

Static pages need no build step to preview (`npx serve .`). For the API
routes, use `vercel dev` with the same environment variables set locally
(e.g. in `.env.local` — never commit it).

## Adding real photography

Every `.ph-box` placeholder in `index.html`, `bridal-makeup-patna/`,
`unisex-salon-patna/`, `shahnai-unisex-salon-patna/` and `gallery/` is
meant to be replaced with a real `<img>` (WebP/AVIF, explicit
`width`/`height`, `loading="lazy"` except the single likely LCP image, and
descriptive `alt` text). No stock or placeholder image is ever presented as
real client work — see brief §25/§39 and `docs/fact-validation-table.md`.

## Security notes

- No Google or WhatsApp credentials ever reach the browser — only the
  Vercel functions in `api/` hold them, as environment variables.
- `BOOKING_SHARED_SECRET` stops strangers from posting fake bookings
  straight to the public Apps Script URL.
- `vercel.json` sets a Content-Security-Policy **with no `unsafe-inline`**
  for scripts or styles — every page here has zero inline `<script>` blocks
  and zero `style="..."` attributes (verified by an automated check during
  the build; see `docs/strategy-dossier.md` → QA). JSON-LD blocks are
  exempt by design (browsers don't execute `application/ld+json` as code).
- `apps-script/Code.gs` guards against spreadsheet formula injection: any
  customer-entered `name` or `note` starting with `=`, `+`, `-` or `@` is
  prefixed with `'` before being written, so it can never execute as a
  formula when the owner opens the sheet.
