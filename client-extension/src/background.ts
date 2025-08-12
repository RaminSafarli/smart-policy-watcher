import checkPolicies from "./utilities/checkPolicies";

const ALARM_NAME = "checkPoliciesAlarm";
let isChecking = false;

async function getSettings() {
  const { checkIntervalMinutes, autoCheckEnabled } =
    await chrome.storage.local.get([
      "checkIntervalMinutes",
      "autoCheckEnabled",
    ]);
  return {
    checkIntervalMinutes: Number.isFinite(checkIntervalMinutes)
      ? checkIntervalMinutes
      : 1,
    autoCheckEnabled:
      typeof autoCheckEnabled === "boolean" ? autoCheckEnabled : true,
  };
}

async function scheduleAlarm() {
  const { checkIntervalMinutes, autoCheckEnabled } = await getSettings();

  await chrome.alarms.clear(ALARM_NAME);

  if (!autoCheckEnabled) {
    console.log("[SPW] Auto-check disabled; no alarm scheduled.");
    return;
  }

  const period = Math.max(1, Math.floor(checkIntervalMinutes));
  chrome.alarms.create(ALARM_NAME, { periodInMinutes: period });
  console.log(`[SPW] Alarm scheduled every ${period} minute(s).`);
}

async function runCheck() {
  if (isChecking) {
    console.log("[SPW] Policy check skipped (already running).");
    return;
  }
  isChecking = true;
  console.log("[SPW] Starting policy check...");
  try {
    await checkPolicies();
    console.log("[SPW] ✅ Policy check completed");
  } catch (err) {
    console.error("[SPW] ❌ Error during policy check:", err);
  } finally {
    isChecking = false;
    console.log("[SPW] 🔚 Policy check finished");
  }
}

chrome.runtime.onInstalled.addListener(() => {
  console.log("[SPW] Extension installed");
  scheduleAlarm();
});
chrome.runtime.onStartup.addListener(() => {
  console.log("[SPW] Browser startup");
  scheduleAlarm();
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name !== ALARM_NAME) return;
  console.log("[SPW] 🔔 Alarm triggered");
  runCheck();
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "local") return;
  if (changes.checkIntervalMinutes || changes.autoCheckEnabled) {
    console.log("[SPW] Settings changed → rescheduling alarm");
    scheduleAlarm();
  }
});

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg?.type === "CHECK_POLICIES_NOW") {
    (async () => {
      await runCheck();
      sendResponse({ ok: true });
    })();
    return true;
  }
});
