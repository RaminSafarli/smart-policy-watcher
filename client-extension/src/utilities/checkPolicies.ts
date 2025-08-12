import getPlatformUrl from "./getPlatformUrl";

const BACKEND_BASE_URL = import.meta.env.VITE_API_BASE as string;

type Summary = { short_summary: string; detailed_summary: string };
type PlatformState = {
  currentSentences?: string[];
  htmlSha256?: string | null;
  lastSummary?: Summary | null;
  lastUpdatedAt: number;
};

function isFirstRun(state?: PlatformState): boolean {
  return !state?.currentSentences || state.currentSentences.length === 0;
}

function arraysEqual(a?: string[] | null, b?: string[] | null): boolean {
  if (!a || !b) return false;
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

export default async function checkPolicies() {
  const { selectedPlatforms = [], policies = {} } =
    await chrome.storage.local.get(["selectedPlatforms", "policies"]);

  const runTime = Date.now();
  let workingPolicies: Record<string, PlatformState> = { ...policies };

  for (const platform of selectedPlatforms) {
    try {
      const { testUrls = {} } = await chrome.storage.local.get("testUrls");
      const fetchUrl =
        (testUrls as Record<string, string>)[platform] ??
        getPlatformUrl(platform);

      const stored: PlatformState = workingPolicies[platform] || {};
      const oldSentences = stored.currentSentences ?? [];

      const fetchRes = await fetch(`${BACKEND_BASE_URL}/fetch_and_preprocess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: fetchUrl }),
      });
      if (!fetchRes.ok)
        throw new Error(`fetch_and_preprocess failed: ${fetchRes.status}`);

      const fetched = (await fetchRes.json()) as {
        sentences: string[];
        html_sha256?: string;
        final_url?: string;
        fetched_at?: string;
        content_type?: string;
        truncated?: boolean;
      };
      const newSentences: string[] = fetched.sentences || [];

      if (isFirstRun(stored)) {
        workingPolicies[platform] = {
          ...stored,
          currentSentences: newSentences,
          htmlSha256: fetched.html_sha256 ?? null,
          lastSummary: null,
          lastUpdatedAt: stored.lastUpdatedAt ?? null,
        };
        continue;
      }

      const unchangedByHash =
        stored.htmlSha256 &&
        fetched.html_sha256 &&
        stored.htmlSha256 === fetched.html_sha256;
      const unchangedByContent = arraysEqual(newSentences, oldSentences);

      if (unchangedByHash || unchangedByContent) {
        workingPolicies[platform] = {
          ...stored,
          htmlSha256: fetched.html_sha256 ?? stored.htmlSha256 ?? null,
        };
        continue;
      }

      const analyzeRes = await fetch(`${BACKEND_BASE_URL}/analyze_change`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          old_sentences: oldSentences,
          new_sentences: newSentences,
        }),
      });
      if (!analyzeRes.ok)
        throw new Error(`analyze_change failed: ${analyzeRes.status}`);

      const result = (await analyzeRes.json()) as {
        is_meaningful: boolean;
        summary: Summary;
      };

      if (result.is_meaningful) {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: `Privacy Update: ${platform}`,
          message: "Privacy policy has been updated.",
        });

        workingPolicies[platform] = {
          ...stored,
          currentSentences: newSentences,
          htmlSha256: fetched.html_sha256 ?? stored.htmlSha256 ?? null,
          lastSummary: result.summary ?? null,
          lastUpdatedAt: runTime,
        };
      } else {
        workingPolicies[platform] = {
          ...stored,
          currentSentences: newSentences,
          htmlSha256: fetched.html_sha256 ?? stored.htmlSha256 ?? null,
          lastSummary: result.summary ?? null,
        };
      }
    } catch (error) {
      console.error(`Error checking ${platform}`, error);
    }
  }

  await chrome.storage.local.set({
    lastCheckedAt: runTime,
    policies: workingPolicies,
  });
}
