// chrome.runtime.onInstalled.addListener(() => {
//     chrome.alarms.create("checkPolicies", {periodInMinutes: 1})
// });

// chrome.alarms.onAlarm.addListener(async (alarm) => {
//     if (alarm.name !== "checkPolicies") return;
    
//     const {selectedPlatforms} = await chrome.storage.local.get("selectedPlatforms");

//     const {policies = {}} = await chrome.storage.local.get("policies");

//     if (!selectedPlatforms || selectedPlatforms.length === 0) return;

//     for (const platform of selectedPlatforms) {

//     }

// });