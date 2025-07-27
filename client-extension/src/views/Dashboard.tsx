interface DashboardProps {
    onGoSettings: () => void;
}

const Dashbooard: React.FC<DashboardProps> = ({ onGoSettings }) => {
    const platforms = JSON.parse(localStorage.getItem("selectedPlatforms") || "[]");
    return (
    <div>
      <h2>Policy Updates</h2>
      {platforms.map((platform: string) => (
        <div key={platform}>
          <strong>{platform}:</strong> No changes detected (placeholder)
        </div>
      ))}
      <button onClick={onGoSettings}>Settings</button>
    </div>
  );
}

export default Dashbooard;
