import { useEffect, useState } from "react";
import { allPlatforms } from '../constants/platforms';

interface SettingsProps {
    onGoBack: () => void;
}


const Settings: React.FC<SettingsProps> = ({ onGoBack }) => {
  const [selected, setSelected] = useState<string[]>([]);

  useEffect(() => {
    chrome.storage.local.get("selectedPlatforms", (data) => {
      setSelected(data.selectedPlatforms || []);
    });
  }, []);

  const togglePlatform = (platform: string) => {
    const updated = selected.includes(platform) ? selected.filter(p=> p !== platform) : [...selected, platform];

    setSelected(updated);
    chrome.storage.local.set({ selectedPlatforms: updated });
  };

  return (
    <div style={{ padding: "1rem"}}>
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

      <button onClick={onGoBack}>Back</button>
    </div>
  );
}

export default Settings;