import {useState} from 'react';

interface Props {
    onContinue: () => void;
}

const platforms = ["Telegram","Facebook", "Twitter", "Instagram", "LinkedIn"];

const Welcome: React.FC<Props> = ({onContinue}) => {
    const [selected, setSelected] = useState<string[]>([]);

    const togglePlatform = (p: string) => {
        setSelected(prev =>
            prev.includes(p) ? prev.filter(x => x !== p) : [...prev, p]
        )
    };

    const handleContinue = () => {
        localStorage.setItem("selectedPlatforms", JSON.stringify(selected));
        onContinue();
    }

  return (
    <div>
        <h2>Welcome to Smart Policy Watcher</h2>
        <p>Select platforms to monitor:
        {platforms.map((p)=>(
            <div key={p}>
          <label>
            <input type="checkbox" checked={selected.includes(p)} onChange={() => togglePlatform(p)} />
            {p}
          </label>
        </div>
        ))}
        <button disabled={selected.length===0} onClick={handleContinue}>Continue</button>
        </p>
    </div>
  )
}
export default Welcome;
