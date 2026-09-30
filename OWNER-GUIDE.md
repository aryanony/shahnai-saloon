# Running Your Website — Owner Guide

You do not need to edit any website code. Everything below is done inside
your Google Sheet.

**Want to change a service?**
Open the **Services** tab and edit the row — name, category, price, or
whether it shows `Fixed`, `From`, or is left blank for "Price on enquiry."

**Want to hide a service?**
Change its **active** column to **No**. It disappears from the website
within about a minute (the next time someone loads the page).

**Want to reorder services?**
Change the numbers in the **display_order** column.

**Want to add an option to the booking form?**
Add a row in the **Additional Services** tab and set **active** to **Yes**.

**Want to see who has requested an appointment?**
Open the **Bookings** tab. Every request appears as one new row with their
name, mobile number, chosen service, add-ons and preferred date.

**Want to update your phone number, WhatsApp number, address, Instagram
link, or the text on the booking button?**
Edit the matching row in the **Settings** tab. The website picks up the
change automatically.

**Want automatic WhatsApp notifications instead of tapping "send" yourself?**
Change **WHATSAPP_MODE** in Settings from `CLICK_TO_CHAT` to `AUTO_NOTIFY`.
This needs a one-time technical setup first — ask your developer (see
`docs/whatsapp-template.txt`).

**Want to speak to a customer?**
Use the phone number in their row, or reply to the WhatsApp message you
received when they submitted the form.

**Nothing else is required.** The website reads directly from this Sheet —
there is no separate dashboard, login, or app to manage.

## Tracking a request (Bookings tab)

Update the **status** column as you work through requests: `NEW` →
`CONTACTED` → `CONFIRMED` (or `CANCELLED`). This is for your own tracking
only — the website doesn't read this column.

## One important note

This website currently refers to your salon as **Shahnaz Beauty Parlour**,
with **Shahnai Unisex Salon** kept as an older name customers might still
search for. Before you put this name on a sign, a domain, or your Google
Business listing, please read the short note your developer left in
`docs/fact-validation-table.md` — a similarly-named salon already exists
elsewhere in Patna, and it's worth five minutes to make sure the name is
clear for you to use.
