import React from 'react';

const GraphGrid = ({ receiverPosition }) => (

  
  <div className="graph-grid">
    {[...Array(64)].map((_, index) => (
      <div key={index} className="grid-cell"></div>
    ))}
    <div
      className="red-square"
      style={{
        top: `calc(${receiverPosition.row} * 100px)`,
        left: `calc(${receiverPosition.column} * 100px)`,
      }}
    ></div>
  </div>
);

export default GraphGrid;
