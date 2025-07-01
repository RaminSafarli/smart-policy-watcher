console.log("Popup script loaded");

function popupState() {
  console.log("Popup State function worked")
  return {
    isFirstTime: true,
    updateFound: false,
    lastChecked: "",
    selectedPlatforms: [],

    async init() {
      chrome.storage.local.get(
        ["isFirstTime", "updateFound", "lastChecked", "selectedPlatforms"],
        (data) => {
          this.isFirstTime = data.isFirstTime ?? true;
          this.updateFound = data.updateFound ?? false;
          this.lastChecked = data.lastChecked ?? "Never";
          this.selectedPlatforms = data.selectedPlatforms ?? [];
        }
      );
    },

    saveSetup() {
      this.isFirstTime = false;
      this.lastChecked = new Date().toLocaleString();

      chrome.storage.local.set({
        isFirstTime: false,
        updateFound: true, // simulate update for now
        lastChecked: this.lastChecked,
        selectedPlatforms: this.selectedPlatforms,
      });
    },

    viewFull() {
      chrome.tabs.create({ url: "https://example.com/full-summary" });
    },
  };
}
