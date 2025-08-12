import { useEffect, useState } from "react";

interface DashboardProps {
  onGoSettings: () => void;
}

interface Summary {
  short_summary: string;
  detailed_summary: string;
}
interface PolicyEntry {
  lastSummary?: Summary | null;
  lastUpdatedAt?: number | null;
  currentSentences?: string[];
  htmlSha256?: string | null;
}

const Dashboard: React.FC<DashboardProps> = ({ onGoSettings }) => {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [policies, setPolicies] = useState<Record<string, PolicyEntry>>({});
  const [globalLastCheckedAt, setGlobalLastCheckedAt] = useState<number | null>(
    null
  );
  const [autoCheckEnabled, setAutoCheckEnabled] = useState<boolean>(true);
  const [loading, setLoading] = useState(true);
  const [detailPlatform, setDetailPlatform] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<"list" | "details">("list");
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    chrome.storage.local.get(
      ["selectedPlatforms", "policies", "lastCheckedAt", "autoCheckEnabled"],
      (data) => {
        setSelectedPlatforms(data.selectedPlatforms || []);
        setPolicies(data.policies || {});
        setGlobalLastCheckedAt(data.lastCheckedAt || null);
        setAutoCheckEnabled(
          typeof data.autoCheckEnabled === "boolean"
            ? data.autoCheckEnabled
            : true
        );
        setLoading(false);
      }
    );
  }, []);

  useEffect(() => {
    function onChanged(changes: any, areaName: string) {
      if (areaName !== "local") return;
      if (
        changes.policies ||
        changes.selectedPlatforms ||
        changes.lastCheckedAt ||
        changes.autoCheckEnabled
      ) {
        chrome.storage.local.get(
          [
            "selectedPlatforms",
            "policies",
            "lastCheckedAt",
            "autoCheckEnabled",
          ],
          (data) => {
            setSelectedPlatforms(data.selectedPlatforms || []);
            setPolicies(data.policies || {});
            setGlobalLastCheckedAt(data.lastCheckedAt || null);
            setAutoCheckEnabled(
              typeof data.autoCheckEnabled === "boolean"
                ? data.autoCheckEnabled
                : true
            );
          }
        );
      }
    }
    chrome.storage.onChanged.addListener(onChanged);
    return () => chrome.storage.onChanged.removeListener(onChanged);
  }, []);

  async function handleCheckNow() {
    try {
      setIsChecking(true);
      const res = await chrome.runtime.sendMessage({
        type: "CHECK_POLICIES_NOW",
      });
      if (!res?.ok) {
        console.error("Manual check failed:", res?.error);
      }
    } catch (e) {
      console.error("Manual check exception:", e);
    } finally {
      setIsChecking(false);
    }
  }

  if (loading) return <p>Loading dashboard...</p>;

  if (!selectedPlatforms.length) {
    return (
      <div>
        <h2>No Platforms Selected</h2>
        <p>Please select at least one platform in settings.</p>
        <button onClick={onGoSettings}>Go to Settings</button>
      </div>
    );
  }

  if (currentView === "details" && detailPlatform) {
    const policy = policies[detailPlatform] || {};
    const s = policy.lastSummary;
    const lastUpdatedAt = policy.lastUpdatedAt
      ? new Date(policy.lastUpdatedAt).toLocaleString()
      : null;

    return (
      <div>
        <button onClick={() => setCurrentView("list")}>← Back</button>
        <h2>{detailPlatform} — Detailed Summary</h2>
        <p style={{ margin: "6px 0" }}>Last updated: {lastUpdatedAt || "—"}</p>
        {s ? (
          <>
            <p style={{ margin: "6px 0" }}>
              <strong>{s.short_summary}</strong>
            </p>
            <div style={{ whiteSpace: "pre-wrap" }}>{s.detailed_summary}</div>
          </>
        ) : (
          <p>No details available.</p>
        )}
        <div style={{ marginTop: 12 }}>
          <button onClick={onGoSettings}>Settings</button>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2>Policy Updates</h2>
      <p>
        Auto-check: {autoCheckEnabled ? "Enabled" : "Disabled"} &nbsp;•&nbsp;{" "}
        Last check run:{" "}
        {globalLastCheckedAt
          ? new Date(globalLastCheckedAt).toLocaleString()
          : "—"}
      </p>
      <div style={{ marginBottom: 12 }}>
        <button onClick={handleCheckNow} disabled={isChecking}>
          {isChecking ? "Checking..." : "Check now"}
        </button>
        &nbsp;
        <button onClick={onGoSettings}>Settings</button>
      </div>

      {selectedPlatforms.map((platform) => {
        const policy = policies[platform] || {};
        const lastUpdatedAt = policy.lastUpdatedAt
          ? new Date(policy.lastUpdatedAt).toLocaleString()
          : "—";
        const lastSummary = policy.lastSummary;

        const status = !policy.currentSentences?.length
          ? "Not checked yet"
          : lastSummary
          ? "Updated"
          : "No changes";

        return (
          <div
            key={platform}
            style={{
              border: "1px solid #ddd",
              borderRadius: 8,
              padding: 12,
              marginBottom: 12,
            }}
          >
            <h3 style={{ margin: "0 0 6px" }}>{platform}</h3>
            <p style={{ margin: "0 0 6px" }}>Status: {status}</p>
            <p style={{ margin: "0 0 6px" }}>Last updated: {lastUpdatedAt}</p>

            {lastSummary ? (
              <>
                <p style={{ margin: "6px 0" }}>
                  <strong>{lastSummary.short_summary}</strong>
                </p>
                <button
                  onClick={() => {
                    setDetailPlatform(platform);
                    setCurrentView("details");
                  }}
                >
                  View details
                </button>
              </>
            ) : (
              <p style={{ margin: "6px 0" }}>No meaningful changes found.</p>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default Dashboard;
