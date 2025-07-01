chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    console.log("Extension installed for the first time.");

    chrome.storage.local
      .set({ hasRunBefore: true })
      .then(() => {
        console.log("Value is set");
      })
      .catch((error) => {
        console.error("Error setting value:", error);
      });
  } else if (details.reason === "update") {
    console.log("Extension updated from version", details.previousVersion);
  }
});

chrome.runtime.onStartup.addListener(() => {
  console.log("Extension started up.");
});

chrome.storage.local
  .get(["hasRunBefore"])
  .then((result) => {
    console.log("Value is " + result.hasRunBefore);
  })
  .catch((error) => {
    console.error("Error getting value:", error);
  });
