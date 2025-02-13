// CoordinatesBox.js
import React from 'react';

const CoordinatesBox = ({ receiverPosition, frozenPosition }) => {
  return (
    <div className="coordinates-box">
      <p>
        {frozenPosition
          ? `Frozen Position: Row ${frozenPosition.row}, Column ${frozenPosition.column}`
          : `Receiver Position: Row ${receiverPosition.row}, Column ${receiverPosition.column}`}
      </p>
    </div>
  );
};

export default CoordinatesBox;
