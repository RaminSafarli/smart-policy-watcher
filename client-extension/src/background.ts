import checkPolicies from "./utilities/checkPolicies";

const CHECK_INTERVAL_MINUTES = 1;
let isChecking = false;

chrome.runtime.onInstalled.addListener(() => {
  console.log("Smart Policy Watcher Extension Installed");
  chrome.alarms.create("checkPoliciesAlarm", {
    periodInMinutes: CHECK_INTERVAL_MINUTES,
  });
});

chrome.alarms.onAlarm.addListener((alarm) => {
  console.log("🔔 Alarm triggered");
  if (alarm.name !== "checkPoliciesAlarm") return;
  if (isChecking) {
    console.log("🔁 Policy check skipped (still running)");
    return;
  }

  isChecking = true;
  console.log("Starting policy check...");
  checkPolicies()
    .then(() => {
      console.log("✅ Policy check completed");
    })
    .catch((error) => {
      console.error("❌ Error during policy check:", error);
    })
    .finally(() => {
      isChecking = false;
      console.log("🔚 Policy check finished");
    });
});
