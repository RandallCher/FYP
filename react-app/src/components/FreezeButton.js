import React from 'react';

const FreezeButton = ({ onFreeze }) => {
  return (
    <button className="action-button" onClick={onFreeze}>
      Freeze Position
    </button>
  );
};

export default FreezeButton;
