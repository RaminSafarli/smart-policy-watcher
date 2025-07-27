interface SettingsProps {
    onGoBack: () => void;
}

const Settings: React.FC<SettingsProps> = ({ onGoBack }) => {
    return (
    <div>
      <h2>Settings</h2>
      <label>
        <input type="checkbox" />
        Enable AI Summaries (Coming Soon)
      </label>
      <button onClick={onGoBack}>Back</button>
    </div>
  );
}

export default Settings;