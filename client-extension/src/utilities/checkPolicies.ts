import getPlatformUrl from "./getPlatformUrl";

const BACKEND_BASE_URL = "http://localhost:8000";

export default async function checkPolicies() {
  const { selectedPlatforms = [], policies = {} } =
    await chrome.storage.local.get(["selectedPlatforms", "policies"]);

  for (const platform of selectedPlatforms) {
    try {
      const fetchUrl = getPlatformUrl(platform);
      const stored = policies[platform] || {};
      const oldSentences = stored.currentSentences || null;

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

      const newSentences = await htmlRes.json();

      console.log(typeof newSentences);

      if (!newSentences || newSentences === oldSentences) {
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
        body: JSON.stringify({
          old_sentences: oldSentences,
          new_sentences: newSentences,
        }),
      });
      const result = await analysisRes.json();

      const updated = {
        currentSentences: newSentences,
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
