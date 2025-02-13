// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import 'font-awesome/css/font-awesome.min.css';
import './App.css';

//iimported functions
import GraphGrid from './components/GraphGrid';
import FreezeButton from './components/FreezeButton';
import CoordinatesBox from './components/CoordinatesBox';
import { connectToNano33 } from './components/bluetooth'; 
import ConnectionStatus from "./components/ConectionStatus";

function App() {

  const [receiverPosition, setReceiverPosition] = useState({ row: 0, column: 1.5 });

  const [frozenPosition, setFrozenPosition] = useState(null);

  const toggleFreezePosition = () => {
    if (frozenPosition) {
      setFrozenPosition(null); // Unfreeze the position
    } else {
      setFrozenPosition(receiverPosition); // Freeze the current position
    }
  };

  // Fetch data from the backend
  useEffect(() => {
    const fetchPosition = () => {
      fetch('http://localhost:5000/receiver-position')
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => setReceiverPosition(data))
        .catch((error) => console.error('Error fetching receiver position:', error));
    };
  
    // Fetch every 2 seconds
    const interval = setInterval(fetchPosition, 2000);
  
    // Cleanup interval on component unmount
    return () => clearInterval(interval);
  }, []);
 


  return (
    <div className="App">
      <header className="App-header">
        <h1>Grid</h1>
      </header>
      <CoordinatesBox receiverPosition={receiverPosition} frozenPosition={frozenPosition} />
      <div className="graph-container">
        <GraphGrid receiverPosition={frozenPosition || receiverPosition} />
        <div className="button-container">
          <ConnectionStatus />
          <FreezeButton onFreeze={toggleFreezePosition} />
        </div>
        
      </div>
      <button onClick={connectToNano33} className="connect-btn">
                Connect to Nano 33 BLE Sense
      </button>
    </div>
  );
}

export default App;
