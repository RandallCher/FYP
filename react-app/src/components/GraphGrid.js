import React from "react";
import "../App.css"; // Ensure the CSS is applied

const GraphGrid = ({ receiverPosition }) => {
    const gridSize = 8;
    const cellSize = 100; // Each cell is 100x100 px (800px / 8)

    // Convert row & column into absolute pixel positions
    const redSquareStyle = {
        transform: `translate(${receiverPosition.column * cellSize}px, ${receiverPosition.row * cellSize}px)`,
    };

    return (
        <div className="graph-grid">
            {/* Create 8x8 grid */}
            {Array.from({ length: gridSize * gridSize }, (_, index) => (
                <div key={index} className="grid-cell"></div>
            ))}
            {/* Red Square representing receiver */}
            <div className="red-square" style={redSquareStyle}></div>
        </div>
    );
};

export default GraphGrid;
