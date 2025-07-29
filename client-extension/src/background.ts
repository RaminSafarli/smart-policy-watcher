const BACKEND_BASE_URL = "http://localhost:8000";
const CHECK_INTERVAL_MINUTES = 1

chrome.runtime.onInstalled.addListener(() => {
    chrome.alarms.create("checkPolicies", {periodInMinutes: CHECK_INTERVAL_MINUTES})
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (alarm.name !== "checkPolicies") return;
    
    const {selectedPlatforms} = await chrome.storage.local.get("selectedPlatforms");

    const {policies = {}} = await chrome.storage.local.get("policies");

    if (!selectedPlatforms || selectedPlatforms.length === 0) return;

    for (const platform of selectedPlatforms) {
        const url = getPolicyUrl(platform);

        try {
            const newHtml = await fetchHtmlFromBackend(url);
            const prevHtml = policies[platform]?.currentHtml ?? null;

            const result = prevHtml
                ? await analyzeChange(prevHtml, newHtml)
                : { is_meaningful: true, summary: "Initial snapshot stored." };


        } catch (err) {
            console.error(`Failed to check ${platform} policies:`, err);
        }
    }

});

// Utility functions (ADD TO DIFFERENT FILE)
function getPolicyUrl(platform: string): string{
    const urls: Record<string, string> = {
        Telegram: "https://telegram.org/privacy"
        // other platforms and their URLs should be added here
    }
    return urls[platform];
}

async function fetchHtmlFromBackend(url: string): Promise<string> {
    // IMPORTANT
    const res = await fetch(`${BACKEND_BASE_URL}/fetch_wayback_html?URL=${encodeURIComponent(url)}`);
    const data = await res.json();
    if (!data.html) throw new Error("Backend did not return HTML");
    return data.html;
}

async function analyzeChange(oldHtml: string, newHtml: string): Promise<{is_meaningful: boolean; summary: string}>{
    const res = await fetch(`${BACKEND_BASE_URL}/analyze_change`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({old_html: oldHtml, new_html: newHtml})
    })

    if (!res.ok) {
        throw new Error("Backend analyze_change failed");
    }
    return await res.json();
}
