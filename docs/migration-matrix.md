# Rebrand Migration Matrix

This reflects an actual comparison between the uploaded `shahnai-website.zip`
and this delivery, not a generic list. "Keep?" tells you whether the *old*
element survives in some form; almost everything below is a controlled
change with a reason, not a blind find-and-replace.

| File / area | Old | New | Keep? | Why |
|---|---|---|---|---|
| Brand name, everywhere | "Shahnai Beauty Saloon" (14 files) | "Shahnaz Beauty Parlour" as primary; "Shahnai Unisex Salon" retained as `secondaryBrand` | **Partial** | Per brief §2/§3: rebrand the public identity, but keep Shahnai findable — see the new `/shahnai-unisex-salon-patna/` bridge page. **Read `docs/fact-validation-table.md` before finalizing "Shahnaz" as the public name** — a same-city naming conflict was found |
| `config/business.json` | *(did not exist — brand strings were hard-coded per file)* | New single source of truth for name/address/phones/URLs, baked into every page at generation time | **New** | Brief §10 asks for exactly this "one central config/data object"; it also fixes a real staleness risk in the old build (16 files each hard-coded the brand name independently) |
| `apps-script/Code.gs` → `nextBookingId_` | Prefix `SB-` | Prefix `SBP-` | **Changed** | Matches the brief's own sample IDs (`SBP-260001`) |
| `apps-script/Code.gs` → Settings keys | `BUSINESS_NAME`, `PRIMARY_PHONE`, `WHATSAPP_NUMBER` | `PRIMARY_BRAND`, `SECONDARY_BRAND`, `PHONE`, `ALT_PHONE`, `WHATSAPP` | **Changed** | Matches brief §18's Settings schema and the actual uploaded `.xlsx` template's tab |
| `apps-script/Code.gs` → Bookings columns | `submitted_at, status, name, mobile, service, additional_services, preferred_date, preferred_time, customer_note, source, page` (11 cols) | `created_at, booking_id, name, mobile, service, additional_services, preferred_date, preferred_time, note, status` (10 cols, reordered) | **Changed** | Matches brief §17 exactly and the real uploaded Sheet's header row (read directly, not assumed) |
| `apps-script/Code.gs` → row writing | Fixed column order, no formula-injection guard | Header-mapped writes (order-independent) + `guard_()` prefixes any user text starting with `=+-@` with `'` | **Improved** | A booking `note` or `name` starting with `=` could otherwise execute as a spreadsheet formula when the owner opens the Bookings tab — a real, previously-unhandled risk |
| `apps-script/Code.gs` → dedupe | `CacheService` only | `CacheService` (idempotent — returns the *same* booking on retry) + per-mobile rate limit (`MOBILE_MAX_PER_WINDOW`) | **Improved** | Old version rejected a retried duplicate as an error; a flaky connection could then show the customer a false failure after the row already saved. New version returns the same success instead |
| `api/booking.js` → `WHATSAPP_MODE` values | `CLICK_TO_CHAT` / `AUTO_API` | `CLICK_TO_CHAT` / `AUTO_NOTIFY` | **Changed** | Matches brief §20/§54 exactly, and the real uploaded Sheet's data-validation list (`Settings!B12`) |
| `api/_lib/whatsapp.js` | Twilio only | Twilio **or** Meta WhatsApp Cloud API, selected by `WHATSAPP_PROVIDER` | **Extended** | Brief §20 says "WhatsApp Business API/provider" generically; Meta's own Cloud API is now offered as a first-party alternative to a third-party reseller |
| `api/booking.js` → fill-time / bot check | Compared `Date.now()` on the server to a client-sent wall-clock timestamp | Compares to a client-sent **elapsed** duration (`performance.now()` delta) | **Fixed** | The old check silently broke for any visitor with an incorrect phone/PC clock — a real false-positive bug, not just a style change |
| `api/booking.js` → dedupe token retry | A retried token was rejected with an error | A retried token returns the original `{ok:true, bookingId}` | **Fixed** | Same idempotency issue as the Apps Script row above, fixed on both layers |
| `vercel.json` → CSP | `script-src 'self' 'unsafe-inline' ...`, `style-src ... 'unsafe-inline'` | `script-src 'self' ...` / `style-src 'self' https://fonts.googleapis.com` — **no `unsafe-inline`** | **Tightened** | The new build has zero inline `<script>` blocks and zero `style="..."` attributes (verified by an automated check — see `docs/strategy-dossier.md` → QA), so the weaker policy is no longer needed |
| Consent / analytics | GTM+Clarity loaded unconditionally on page load | Loaded only after the visitor accepts the on-page consent banner | **New** | Not explicitly requested, but brief §42 says "consent-aware" Clarity use; this makes GA4 consent-aware too, for consistency |
| Reviews section (`index.html`) | One visible placeholder review styled like a real quote | Explicit "verified reviews will appear here... no review text is invented" message, no placeholder styled as a real quote | **Changed** | Brief §38/§50 forbids anything that reads as a fabricated review, even a labeled placeholder |
| Gallery/bridal placeholders | `frame-card` divs with inline `style="position:static..."` | `.ph-box` placeholder class, zero inline styles | **Changed** | Required by the tightened CSP above |
| `/shahnai-unisex-salon-patna/` | *(did not exist)* | New brand-bridge page | **New** | Required by brief §6 |
| `/services/index.html` | Flat service list | Grouped by `category` via menu sections | **Improved** | Easier to scan once bridal/unisex/grooming are all on one page |
| `package.json` name/description | `shahnai-beauty-saloon-website` | `shahnaz-beauty-parlour-website`, adds `test` and `build:pages` scripts | **Changed** | Reflects the new brand and the new Python page generator / Node test suite |
| `.env.example` | Twilio vars only | Adds `WHATSAPP_PROVIDER` switch + Meta Cloud API vars alongside Twilio | **Extended** | Supports the new dual-provider `whatsapp.js` |
| `robots.txt` / `sitemap.xml` | Old site URL, 11 routes | New site URL, 12 routes (adds the brand-bridge page) | **Changed** | New page added, URL updated |
| `README.md` / `OWNER-GUIDE.md` / `STRATEGY.md` | Shahnai-specific | Rewritten for the new brand, schema and dual-brand strategy (`docs/strategy-dossier.md`) | **Rewritten** | Content, not just find-and-replace, since the Sheet schema and booking ID format both changed |
| Old Sheet ID `1d8kX...Bqnpw` (previous project) | Referenced in the old `STRATEGY.md` | Not referenced anywhere in this delivery | **Dropped** | This project ships against the newly uploaded `.xlsx` template, which becomes its own Sheet once opened in Google Sheets — the old Sheet ID belonged to the prior engagement |

## What was intentionally NOT changed

- The zero-npm-dependency approach for `api/` functions (still plain
  `fetch`, no SDKs) — kept because it worked and adds no attack surface.
- The overall architecture: static HTML/CSS/JS + Vercel Functions + Apps
  Script + Google Sheet, no database, no accounts, no admin panel. The old
  `STRATEGY.md` established this and it remains correct for a salon this
  size.
- The "one booking = one row" model and booking-ID-based idempotency
  concept — only the implementation bugs around it were fixed, not the
  design.
