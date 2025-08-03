import {useState, useEffect} from 'react';
import { allPlatforms } from '../constants/platforms';

interface Props {
    onContinue: () => void;
}

const Welcome: React.FC<Props> = ({onContinue}) => {
    const [selected, setSelected] = useState<string[]>([]);

    useEffect(() => {
        const loadSelectedPlatforms = async () => {
          chrome.storage.local.get("selectedPlatforms",result => {
            if(Array.isArray(result.selectedPlatforms)) {
                setSelected(result.selectedPlatforms);
            }
          });
        }

        loadSelectedPlatforms();
    }, []);

    const togglePlatform = (p: string) => {
        setSelected(prev =>
            prev.includes(p) ? prev.filter(x => x !== p) : [...prev, p]
        )
    };

    const handleContinue = () => {
        chrome.storage.local.set({selectedPlatforms: selected});
        onContinue();
    }

  return (
    <div>
        <h2>Welcome to Smart Policy Watcher</h2>
        <p>Select platforms to monitor:
        {allPlatforms.map((p)=>(
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
