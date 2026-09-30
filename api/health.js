"use strict";
module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  const e = process.env;
  res.status(200).json({
    ok: true,
    time: new Date().toISOString(),
    configured: {
      appsScriptUrl: /^https:\/\/script\.google\.com\//.test(e.APPS_SCRIPT_URL || ""),
      sharedSecret: Boolean(e.BOOKING_SHARED_SECRET),
      whatsappProvider: ["meta", "twilio"].includes(String(e.WHATSAPP_PROVIDER || "").toLowerCase())
    }
  });
};
