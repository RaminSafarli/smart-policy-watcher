import { useEffect, useState } from "react";
import { allPlatforms } from "../constants/platforms";

interface SettingsProps {
  onGoBack: () => void;
}

const Settings: React.FC<SettingsProps> = ({ onGoBack }) => {
  const [selected, setSelected] = useState<string[]>([]);
  const [checkIntervalMinutes, setCheckIntervalMinutes] = useState<number>(1);
  const [autoCheckEnabled, setAutoCheckEnabled] = useState<boolean>(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    chrome.storage.local.get(
      ["selectedPlatforms", "checkIntervalMinutes", "autoCheckEnabled"],
      (data) => {
        setSelected(data.selectedPlatforms || []);
        setCheckIntervalMinutes(
          Number.isFinite(data.checkIntervalMinutes)
            ? data.checkIntervalMinutes
            : 1
        );
        setAutoCheckEnabled(
          typeof data.autoCheckEnabled === "boolean"
            ? data.autoCheckEnabled
            : true
        );
      }
    );
  }, []);

  const togglePlatform = (platform: string) => {
    const updated = selected.includes(platform)
      ? selected.filter((p) => p !== platform)
      : [...selected, platform];
    setSelected(updated);
    chrome.storage.local.set({ selectedPlatforms: updated });
  };

  const saveSettings = () => {
    setSaving(true);
    const minutes = Math.max(1, Math.floor(checkIntervalMinutes || 1)); // enforce min 1
    chrome.storage.local.set(
      {
        selectedPlatforms: selected,
        checkIntervalMinutes: minutes,
        autoCheckEnabled,
      },
      () => {
        setSaving(false);
        console.log("[SPW] Settings saved");
      }
    );
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>🔧 Tracked Platforms</h2>
      <p>Enable or disable platforms you want to monitor.</p>

      <ul>
        {allPlatforms.map((platform) => (
          <li key={platform} className="mb-2">
            <label style={{ display: "flex", alignItems: "center" }}>
              <input
                type="checkbox"
                checked={selected.includes(platform)}
                onChange={() => togglePlatform(platform)}
              />
              <span>{platform}</span>
            </label>
          </li>
        ))}
      </ul>

      <hr style={{ margin: "1rem 0" }} />

      <h3>⏱️ Policy Check Settings</h3>

      <label style={{ display: "block", marginBottom: "0.5rem" }}>
        <input
          type="checkbox"
          checked={autoCheckEnabled}
          onChange={(e) => setAutoCheckEnabled(e.target.checked)}
        />{" "}
        Enable automatic checks
      </label>

      <label
        style={{
          display: "block",
          marginBottom: "0.5rem",
          opacity: autoCheckEnabled ? 1 : 0.6,
        }}
      >
        Interval (minutes):{" "}
        <input
          type="number"
          min={1}
          step={1}
          value={checkIntervalMinutes}
          onChange={(e) =>
            setCheckIntervalMinutes(parseInt(e.target.value || "1", 10))
          }
          disabled={!autoCheckEnabled}
          style={{ width: 80 }}
        />
      </label>

      <button onClick={saveSettings} disabled={saving}>
        {saving ? "Saving..." : "Save Settings"}
      </button>

      <div style={{ marginTop: "1rem" }}>
        <button onClick={onGoBack}>Back</button>
      </div>
    </div>
  );
};

export default Settings;
