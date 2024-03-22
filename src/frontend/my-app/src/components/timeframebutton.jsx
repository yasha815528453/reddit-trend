import React from 'react';

const TimeFrameButton = ({ label, setTimeFrame }) => (
  <button onClick={() => setTimeFrame(label)}>
    {label.toUpperCase()}
  </button>
);

export default TimeFrameButton;
