# Domain Research

**Availability is NOT verified here.** I have no registrar/WHOIS access from
this environment, so "Appears in use?" below only reflects what a web search
turned up (a live site, directory listing, etc. using that name) — the
absence of a hit does NOT mean a domain is free to register. Check every
shortlisted domain at a registrar (e.g. Namecheap, GoDaddy, IN Registry for
.in) before deciding, and do a trademark screen for any candidate before
buying it — see the brand-risk finding in `fact-validation-table.md` first,
since it affects which name family is worth registering at all.

## Candidates

| Domain | Brand clarity | Length | Local relevance | Secondary-brand (Shahnai) support | Registrar-verified? | Notes |
|---|---|---|---|---|---|---|
| shahnazbeautypatna.com | High | Medium | High (Patna in-name) | None | **Not verified** | Clean, descriptive; still carries the brand-risk noted above |
| shahnazsalonpatna.com | High | Medium | High | None | **Not verified** | "Salon" reads slightly more unisex than "Beauty" |
| shahnazpatna.com | Medium | Short | High | None | **Not verified** | Short, but less descriptive of the service; higher chance of feeling generic |
| shahnazbeautypatna.in | High | Medium | High | None | **Not verified** | `.in` reads as more local/Indian; often easier to register than `.com` for a Patna-first business |
| shahnazpatna.in | Medium | Short | High | None | **Not verified** | Same trade-off as the `.com` version above |
| shahnazsalonpatna.in | High | Medium | High | None | **Not verified** | Good fallback if `.com` is taken |
| shahnazunisexsalonpatna.com | Medium | Long | High | Partial (keeps "unisex") | **Not verified** | Long — harder to say/type/print on signage |
| shahnaiunisexsalonpatna.com | High for the secondary brand | Long | High | **Full** | **Not verified** | Best option if the secondary brand ends up primary (see risk note) |
| shahnaiunisexsalon.in | High for the secondary brand | Medium | Medium | **Full** | **Not verified** | Good secondary-domain candidate for a 301 into the main site's `/shahnai-unisex-salon-patna/` page |
| shahnaiunisexsalon.com | High for the secondary brand | Medium | Medium | **Full** | **Not verified** | Same role as above, `.com` variant |
| shahnaibeautypatna.com | Medium | Medium | High | Partial | **Not verified** | Blended option if the brand direction changes |
| shahnaiparlourpatna.in | Medium | Medium | High | Partial | **Not verified** | Alternate blended option |

**Known exclusion:** `shahnazbeautyparlour.in` is already in use by an
unrelated Bihar business per the brief — excluded from this shortlist.

## Recommendation

Given the brand-risk finding, there are two honest paths, not one:

**Path A — proceed with "Shahnaz Beauty Parlour" as planned.**
Primary: `shahnazbeautypatna.com` (or the `.in` if `.com` is taken).
Secondary redirect (optional): `shahnaiunisexsalonpatna.com` → 301 to
`primary-domain.com/shahnai-unisex-salon-patna/`. Only take this path after
the trademark clearance check recommended in `fact-validation-table.md`.

**Path B — lead with "Shahnai Unisex Salon" instead** (lower brand-risk,
since it doesn't sit in the "Shahnaz ___" franchise-naming family at all).
Primary: `shahnaiunisexsalonpatna.com` or `shahnaiunisexsalon.in`. The
codebase supports this with a one-line change: swap `primaryBrand` and
`secondaryBrand` in `config/business.json`, update `Settings!PRIMARY_BRAND`
/ `SECONDARY_BRAND` in the Sheet to match, and regenerate the pages
(`npm run build:pages`) — see README.md.

Either way: **one primary domain**, with at most one secondary domain that
redirects into a single site — never two parallel, near-duplicate sites (this
also matches Google's own guidance against duplicate business listings; see
`docs/strategy-dossier.md` → "Google Business Profile").
