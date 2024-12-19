// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import 'font-awesome/css/font-awesome.min.css';
import './App.css';

function App() {

  const [receiverPosition, setReceiverPosition] = useState({ row: 0, column: 1.5 });

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
        <h1>Graph Grid</h1>
      </header>
      <div className="coordinates-box">
        <p>Receiver Position: Row {receiverPosition.row}, Column {receiverPosition.column}</p>
      </div>
      <div className="graph-grid">
        {[...Array(64)].map((_, index) => (
          <div key={index} className="grid-cell"></div>
        ))}
        <div
          className="red-square"
          style={{
            top: `calc(${receiverPosition.row} * 100px)`,
            left: `calc(${receiverPosition.column} * 100px)`
          }}
        ></div>
      </div>
    </div>
  );
}

export default App;
