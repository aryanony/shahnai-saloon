"use strict";
const { getCatalog } = require("./_lib/catalog");

module.exports = async (req, res) => {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ ok: false, message: "Method not allowed." });
  }
  const data = await getCatalog();
  // Only cache real Sheet data at the edge; never cache a fallback response.
  res.setHeader("Cache-Control", data.source === "sheet" ? "public, s-maxage=45, stale-while-revalidate=120" : "no-store");
  return res.status(200).json({
    business: data.business,
    services: data.services,
    additionalServices: data.additionalServices,
    source: data.source
  });
};
