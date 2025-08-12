import { useState, useEffect } from "react";
import Welcome from "./views/Welcome";
import Dashboard from "./views/Dashboard";
import Settings from "./views/Settings";
import "./App.css";

function App() {
  const [view, setView] = useState<"welcome" | "dashboard" | "settings">(
    "welcome"
  );
  const [booting, setBooting] = useState(true);

  useEffect(() => {
    const hasChrome = typeof chrome !== "undefined" && chrome.storage?.local;
    if (!hasChrome) {
      setView("dashboard");
      setBooting(false);
      return;
    }

    chrome.storage.local.get("hasSeenWelcome", (data) => {
      const seen = Boolean(data?.hasSeenWelcome);
      setView(seen ? "dashboard" : "welcome");
      setBooting(false);
    });
  }, []);

  if (booting) return <div>Loading...</div>;

  const renderView = () => {
    switch (view) {
      case "dashboard":
        return <Dashboard onGoSettings={() => setView("settings")} />;
      case "settings":
        return <Settings onGoBack={() => setView("dashboard")} />;
      case "welcome":
      default:
        return (
          <Welcome
            onContinue={() => {
              chrome.storage.local.set({ hasSeenWelcome: true });
              setView("dashboard");
            }}
          />
        );
    }
  };

  return <div>{renderView()}</div>;
}

export default App;
