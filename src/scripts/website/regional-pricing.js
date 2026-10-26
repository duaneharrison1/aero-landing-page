/* Aero website, Pricing page: regional plan prices.
   Regional prices are intentional (CLAUDE.md): this is the SAME logic as src/components/PricingTableNew.astro, which the
   site used before Oct 2026 (Firestore config/pricing for tiers and prices, ipinfo for the visitor's country, the same
   fallbacks). Never change the currency or the pricing logic here; only where the prices are shown.
   Every element with data-price="basic|solo|pro" gets that plan's monthly price for the visitor's region.
   The markup's own numbers (US prices from docs/brand/PRICING-FACTS.md) stay if anything fails. */
(function () {
  'use strict';
  var els = document.querySelectorAll('[data-price]');
  if (!els.length) return;

  // Fallback regional pricing data (used if Firestore fetch fails)
  var FALLBACK_PRICING = {
    US: {
      basic: { monthly: '$3', yearly: '$2.33', yearlyTotal: '$28' },
      solo: { monthly: '$6', yearly: '$4.75', yearlyTotal: '$57' },
      pro: { monthly: '$19', yearly: '$16.58', yearlyTotal: '$199' }
    },
    JP: {
      basic: { monthly: '$2.50', yearly: '$2', yearlyTotal: '$24' },
      solo: { monthly: '$5', yearly: '$4', yearlyTotal: '$48' },
      pro: { monthly: '$16', yearly: '$14', yearlyTotal: '$168' }
    },
    TW: {
      basic: { monthly: '$2', yearly: '$1.58', yearlyTotal: '$19' },
      solo: { monthly: '$4', yearly: '$3.17', yearlyTotal: '$38' },
      pro: { monthly: '$13', yearly: '$10.83', yearlyTotal: '$130' }
    },
    PH: {
      basic: { monthly: '$1.50', yearly: '$1.17', yearlyTotal: '$14' },
      solo: { monthly: '$3', yearly: '$2.33', yearlyTotal: '$28' },
      pro: { monthly: '$9.50', yearly: '$7.58', yearlyTotal: '$91' }
    },
    TH: {
      basic: { monthly: '$1', yearly: '$0.75', yearlyTotal: '$9' },
      solo: { monthly: '$2', yearly: '$1.58', yearlyTotal: '$19' },
      pro: { monthly: '$6', yearly: '$4.75', yearlyTotal: '$57' }
    }
  };

  // Fallback country to tier mapping (used if Firestore fetch fails)
  var FALLBACK_TIERS = {
    JP: ['IE', 'GB', 'FR', 'JP', 'KR', 'IL', 'IT'],
    TW: ['TW', 'ES', 'PT', 'PL'],
    PH: ['PH', 'MY', 'CN', 'AR', 'BR'],
    TH: ['TH', 'VN', 'ID', 'IN', 'NG']
  };

  // Get pricing tier from country using tiers data
  function getPricingTier(country, tiers) {
    var c = (country || 'US').toUpperCase();
    for (var tierName in tiers) {
      if (tiers[tierName].indexOf(c) !== -1) return tierName;
    }
    return 'US';
  }

  async function run() {
    var projectId = 'figmawebapp';
    var tiers = FALLBACK_TIERS, pricing = FALLBACK_PRICING, tier = 'US';

    // Fetch pricing data from Firestore (do this first so we can use tiers for region detection)
    try {
      var pricingUrl = 'https://firestore.googleapis.com/v1/projects/' + projectId + '/databases/(default)/documents/config/pricing';
      var pricingDoc = await (await fetch(pricingUrl)).json();
      if (pricingDoc.fields) {
        var tiersField = pricingDoc.fields.tiers && pricingDoc.fields.tiers.mapValue && pricingDoc.fields.tiers.mapValue.fields;
        if (tiersField) {
          tiers = {};
          Object.keys(tiersField).forEach(function (tierName) {
            var countries = (tiersField[tierName].arrayValue && tiersField[tierName].arrayValue.values) || [];
            tiers[tierName] = countries.map(function (c) { return c.stringValue; });
          });
        }
        var pricesField = pricingDoc.fields.prices && pricingDoc.fields.prices.mapValue && pricingDoc.fields.prices.mapValue.fields;
        if (pricesField) {
          pricing = {};
          Object.keys(pricesField).forEach(function (tierName) {
            var tierPrices = (pricesField[tierName].mapValue && pricesField[tierName].mapValue.fields) || {};
            pricing[tierName] = {};
            Object.keys(tierPrices).forEach(function (planKey) {
              var f = (tierPrices[planKey].mapValue && tierPrices[planKey].mapValue.fields) || {};
              pricing[tierName][planKey] = {
                monthly: (f.monthly && f.monthly.stringValue) || '$0',
                yearly: (f.yearly && f.yearly.stringValue) || '$0',
                yearlyTotal: (f.yearlyTotal && f.yearlyTotal.stringValue) || '$0'
              };
            });
          });
        }
      }
    } catch (e) { /* keep using fallback pricing and tiers */ }

    // Detect region using the fetched (or fallback) tiers
    try {
      var data = await (await fetch('https://ipinfo.io/json?token=b259d22dc84b2e')).json();
      tier = getPricingTier(data.country, tiers);
    } catch (e) { tier = 'US'; }

    var prices = pricing[tier] || pricing.US;
    if (!prices) return;
    els.forEach(function (el) {
      var p = prices[el.getAttribute('data-price')];
      if (p && p.monthly) el.textContent = p.monthly;
    });
  }
  run();
})();
