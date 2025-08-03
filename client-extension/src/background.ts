import { log } from "console";
import { platformUrls } from "./constants/platformsUrls";
const BACKEND_BASE_URL = "http://localhost:8000";
const CHECK_INTERVAL_MINUTES = 1;
// let isChecking = false;

chrome.runtime.onInstalled.addListener(() => {
  console.log("Smart Policy Watcher Extension Installed");
  chrome.alarms.create("checkPolicies", {
    periodInMinutes: CHECK_INTERVAL_MINUTES,
  });
});

// chrome.alarms.onAlarm.addListener(async (alarm) => {
//     console.log("🔔 Alarm triggered");
//     if (alarm.name !== "checkPolicies") return;
//     if (isChecking) {
//         console.log("🔁 Policy check skipped (still running)");
//         return;
//     }

//     isChecking = true;
//     console.log("✅ Policy check started:", new Date().toISOString());

//     const {selectedPlatforms} = await chrome.storage.local.get("selectedPlatforms");
//     const {policies = {}} = await chrome.storage.local.get("policies");

//     if (!selectedPlatforms || selectedPlatforms.length === 0) return;

//     for (const platform of selectedPlatforms) {
//         console.log(`Checking ${platform} policies...`);
//         const url = getPolicyUrl(platform);

//         try {
//             const newHtml = await fetchHtmlFromBackend(url);
//             const prevHtml = policies[platform]?.currentHtml ?? null;

//             const result = prevHtml
//                 ? await analyzeChange(prevHtml, newHtml)
//                 : { is_meaningful: true, summary: "Initial snapshot stored." };

//             if (result.is_meaningful) {
//                 const updated = {
//                     previousHtml: prevHtml,
//                     currentHtml: newHtml,
//                     lastChecked: new Date().toISOString(),
//                     summaries: [
//                         ...(policies[platform]?.summaries || []),
//                         {date: new Date().toISOString(), summary: result.summary}
//                     ]
//                 }
//                 await chrome.storage.local.set({
//                     policies: {
//                         ...policies,
//                         [platform]: updated
//                     }
//                 })

//                 chrome.notifications.create({
//                     type: "basic",
//                     iconUrl: "icon.png",
//                     title: `${platform} Privacy Policy Changed`,
//                     message: result.summary
//                 })

//                  chrome.action.setBadgeText({ text: "1" });
//             };
//         } catch (err) {
//             console.error(`Failed to check ${platform} policies:`, err);
//         } finally{
//             isChecking = false;
//             console.log("✅ Policy check finished");
//         }
//     }

// });

async function checkPolicies() {
  const { selectedPlatforms = [], policies = {} } =
    await chrome.storage.local.get(["selectedPlatforms", "policies"]);

  for (const platform of selectedPlatforms) {
    try {
      const fetchUrl = getPlatformUrl(platform);
      const stored = policies[platform] || {};
      const oldHtml = stored.currentHtml || null;

      const htmlRes = await fetch(`${BACKEND_BASE_URL}/fetch_html`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url: fetchUrl }),
      });

      if (!htmlRes.ok) {
        console.warn(`Failed to fetch live HTML for ${platform}`);
        continue;
      }

      const newHtml = await htmlRes.text();

      if (!newHtml || newHtml === oldHtml) {
        console.log(`No change detected for ${platform}`);
        continue;
      }

      // ANALYSIS
      const analysisRes = await fetch(`${BACKEND_BASE_URL}/analyze_change`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // ATTENTION ON PARAMETER NAMES
        body: JSON.stringify({ prevHtml: oldHtml, newHtml }),
      });
      const result = await analysisRes.json();

      const updated = {
        currentHtml: newHtml,
        summary: result.summary || null,
        lastChecked: new Date().toISOString(),
      };

      await chrome.storage.local.set({
        policies: {
          ...policies,
          [platform]: updated,
        },
      });

      if (result.summary) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: `Privacy Update: ${platform}`,
          message: "Privacy policy has been updated.",
        });
      }
    } catch (error) {
      console.error(`Error checking ${platform}`, error);
    }
  }
}

// Utility functions (ADD TO DIFFERENT FILE)
function getPlatformUrl(platform: string): string {
  // const urls: Record<string, string> =
  return platformUrls[platform];
}

// async function fetchHtmlFromBackend(url: string): Promise<string> {
//   // IMPORTANT
//   const res = await fetch(
//     `${BACKEND_BASE_URL}/fetch_wayback_html?url=${encodeURIComponent(url)}`
//   );
//   const data = await res.json();
//   if (!data.html) throw new Error("Backend did not return HTML");
//   return data.html;
// }

// async function analyzeChange(
//   oldHtml: string,
//   newHtml: string
// ): Promise<{ is_meaningful: boolean; summary: string }> {
//   const res = await fetch(`${BACKEND_BASE_URL}/analyze_change`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ old_html: oldHtml, new_html: newHtml }),
//   });

//   if (!res.ok) {
//     throw new Error("Backend analyze_change failed");
//   }
//   return await res.json();
// }

// async function getSnapshotUrl(targetUrl: string): Promise<string | null> {
//   const api = "https://archive.org/wayback/available";
//   const params = new URLSearchParams({ url: targetUrl });
//   console.log(params);

//   console.log(`${api}?${params.toString()}`);

//   const res = await fetch(`${api}?${params.toString()}`);
//   const data = await res.json();

//   console.log(data);

//   const snapshot = data?.archived_snapshots?.closest;
//   if (snapshot?.available && snapshot?.url) {
//     // Optional: fix Telegram-encoded snapshots
//     return decodeURIComponent(snapshot.url.replace(/%E2%9C%85.*?@/, ""));
//   }

//   return null;
// }
