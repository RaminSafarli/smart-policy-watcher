import { useState } from 'react'
import Welcome from './views/Welcome'
import Dashbooard from './views/Dashboard';
import Settings from './views/Settings';
import './App.css'

function App() {
   const [view, setView] = useState<'welcome' | 'dashboard' | 'settings'>('welcome');

  const renderView = () => {
    switch (view) {
      case 'dashboard':
        return <Dashbooard onGoSettings={() => setView('settings')} />;
      case 'settings':
        return <Settings onGoBack={() => setView('dashboard')} />;
      default:
        return <Welcome onContinue={() => setView('dashboard')} />;
    }
  }

  return <div>{renderView()}</div>
}

export default App
