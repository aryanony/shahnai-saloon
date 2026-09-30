"use strict";
/* AUTO_NOTIFY delivery. Only runs after the Sheet row already exists, so a failure here never loses a booking.
 *
 * WHATSAPP_PROVIDER=meta   -> WhatsApp Business Platform (Cloud API)
 *   WHATSAPP_META_TOKEN, WHATSAPP_META_PHONE_NUMBER_ID, WHATSAPP_TEMPLATE_NAME, [WHATSAPP_TEMPLATE_LANG=en], [WHATSAPP_API_VERSION]
 * WHATSAPP_PROVIDER=twilio -> Twilio WhatsApp
 *   TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, TWILIO_CONTENT_SID
 *
 * Business-initiated messages need an approved template on either provider. The template text to submit is in
 * docs/whatsapp-template.txt (8 body variables, matching ShahnazMessage.templateParams).
 */
const Message = require("../../src/js/message.js");

const TIMEOUT_MS = 8000;

async function post(url, options) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, Object.assign({ signal: ctrl.signal }, options));
    if (!res.ok) throw new Error("provider_http_" + res.status);
    return true;
  } finally {
    clearTimeout(timer);
  }
}

async function viaMeta(toE164, booking) {
  const token = process.env.WHATSAPP_META_TOKEN;
  const phoneId = process.env.WHATSAPP_META_PHONE_NUMBER_ID;
  const template = process.env.WHATSAPP_TEMPLATE_NAME;
  if (!token || !phoneId || !template) throw new Error("meta_not_configured");
  const version = process.env.WHATSAPP_API_VERSION || "v21.0";
  return post(`https://graph.facebook.com/${version}/${phoneId}/messages`, {
    method: "POST",
    headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
    body: JSON.stringify({
      messaging_product: "whatsapp",
      to: toE164.replace(/^\+/, ""),
      type: "template",
      template: {
        name: template,
        language: { code: process.env.WHATSAPP_TEMPLATE_LANG || "en" },
        components: [{ type: "body", parameters: Message.templateParams(booking).map((text) => ({ type: "text", text })) }]
      }
    })
  });
}

async function viaTwilio(toE164, booking) {
  const sid = process.env.TWILIO_ACCOUNT_SID;
  const token = process.env.TWILIO_AUTH_TOKEN;
  const from = process.env.TWILIO_WHATSAPP_FROM;
  const contentSid = process.env.TWILIO_CONTENT_SID;
  if (!sid || !token || !from || !contentSid) throw new Error("twilio_not_configured");
  const vars = {};
  Message.templateParams(booking).forEach((v, i) => { vars[String(i + 1)] = v; });
  const body = new URLSearchParams({ To: "whatsapp:" + toE164, From: from, ContentSid: contentSid, ContentVariables: JSON.stringify(vars) });
  return post(`https://api.twilio.com/2010-04-01/Accounts/${sid}/Messages.json`, {
    method: "POST",
    headers: { Authorization: "Basic " + Buffer.from(sid + ":" + token).toString("base64"), "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString()
  });
}

/** @returns {Promise<"sent"|"failed">} never throws */
async function notifyOwner(toE164, booking) {
  try {
    const provider = (process.env.WHATSAPP_PROVIDER || "").toLowerCase();
    if (provider === "meta") await viaMeta(toE164, booking);
    else if (provider === "twilio") await viaTwilio(toE164, booking);
    else throw new Error("no_provider_configured");
    return "sent";
  } catch (err) {
    console.error("whatsapp: notification failed -", err.message); // no customer data in logs
    return "failed";
  }
}

module.exports = { notifyOwner };
