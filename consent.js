// Cookie-consent gate for Google Analytics. GA4 sets tracking cookies, so
// under GDPR/ePrivacy nothing from Google may load until the visitor agrees.
// The banner shows once; the choice is remembered so it never shows again in
// this browser, and declining actually prevents the analytics script from
// ever being requested rather than just hiding what it collects.
(function () {
  "use strict";

  var GA_MEASUREMENT_ID = "G-0SGW2S5FXF";
  var STORAGE_KEY = "consent-analytics";

  function loadAnalytics() {
    if (!GA_MEASUREMENT_ID || GA_MEASUREMENT_ID.indexOf("XXXX") !== -1) return;

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_MEASUREMENT_ID;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", GA_MEASUREMENT_ID);
  }

  function getStoredChoice() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (err) {
      return null; // private browsing / storage blocked - treat as undecided, ask again
    }
  }

  function storeChoice(value) {
    try {
      window.localStorage.setItem(STORAGE_KEY, value);
    } catch (err) {
      // Storage unavailable - the choice for THIS load still applies below,
      // it just won't be remembered next visit.
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var choice = getStoredChoice();

    if (choice === "accepted") {
      loadAnalytics();
      return;
    }
    if (choice === "declined") {
      return;
    }

    var banner = document.getElementById("consent-banner");
    var acceptBtn = document.getElementById("consent-accept");
    var declineBtn = document.getElementById("consent-decline");
    if (!banner || !acceptBtn || !declineBtn) return;

    banner.hidden = false;

    acceptBtn.addEventListener("click", function () {
      storeChoice("accepted");
      banner.hidden = true;
      loadAnalytics();
    });

    declineBtn.addEventListener("click", function () {
      storeChoice("declined");
      banner.hidden = true;
    });
  });
})();
