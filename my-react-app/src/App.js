// import logo from './logo.svg';
import React, { useState, useEffect } from 'react';
import 'font-awesome/css/font-awesome.min.css';
import './App.css';

function App() {

  const [redSquarePosition, setRedSquarePosition] = useState({ row: 0, column: 0 });

  // Fetch data from the backend
  useEffect(() => {
    fetch('http://localhost:5000/red-square') // Replace with your backend endpoint
      .then((response) => response.json())
      .then((data) => setRedSquarePosition(data))
      .catch((error) => console.error('Error fetching red square position:', error));
  }, []);



  return (
    <div className="App">
      <header className="App-header">
        <h1>Graph Grid</h1>
      </header>
      <div className="coordinates-box">
        <p>Current Position: Row {redSquarePosition.row}, Column {redSquarePosition.column}</p>
      </div>
      <div className="graph-grid">
        {[...Array(64)].map((_, index) => (
          <div key={index} className="grid-cell"></div>
        ))}
        <div
          className="red-square"
          style={{
            top: `calc(${redSquarePosition.row} * 100px)`,
            left: `calc(${redSquarePosition.column} * 100px)`
          }}
        ></div>
      </div>
    </div>
  );
}

export default App;
