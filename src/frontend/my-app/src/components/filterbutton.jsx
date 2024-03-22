import React from 'react';

const FilterButton = ({ label, setFilter }) => (
  <button onClick={() => setFilter(label.toLowerCase())}>
    {label}
  </button>
);

export default FilterButton;
