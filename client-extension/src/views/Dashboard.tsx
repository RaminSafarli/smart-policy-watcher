import { useEffect, useState } from "react";

interface DashboardProps {
  onGoSettings: () => void;
}

interface PolicyEntry {
  summary?: string | null;
  lastChecked?: string | null;
}

const Dashbooard: React.FC<DashboardProps> = ({ onGoSettings }) => {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [policies, setPolicies] = useState<Record<string, PolicyEntry>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    chrome.storage.local.get(["selectedPlatforms", "policies"], (data) => {
      setSelectedPlatforms(data.selectedPlatforms || []);
      setPolicies(data.policies || {});
      setLoading(false);
    });
  });

  if (loading) {
    return <p>Loading dashboard...</p>;
  }

  if (!selectedPlatforms.length) {
    return (
      <div>
        <h2>No Platforms Selected</h2>
        <p>Please select at least one platform in settings.</p>
        <button onClick={onGoSettings}>Go to Settings</button>
      </div>
    );
  }

  return (
    <div>
      <h2>Policy Updates</h2>

      {selectedPlatforms.map((platform) => {
        const policy = policies[platform] || {};
        const summary = policy.summary;
        const lastChecked = policy.lastChecked
          ? new Date(policy.lastChecked).toLocaleString()
          : null;

        return (
          <div key={platform}>
            <h3>{platform}</h3>
            {lastChecked ? (
              <p>Last checked: {lastChecked}</p>
            ) : (
              <p>Not checked yet</p>
            )}

            {summary ? <p>{summary}</p> : <p>No meaningful changes found.</p>}
          </div>
        );
      })}

      <button onClick={onGoSettings}>Settings</button>
    </div>
  );
};

export default Dashbooard;
