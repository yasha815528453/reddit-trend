import React, { useState, useEffect } from 'react';
import Table from './components/table';
import './App.css'; // If you are using a separate CSS file

function App() {
  const [data, setData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch your data from the backend
    const fetchData = async () => {
      try {
        // The endpoint to retrieve data from your database
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/tabledata`);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const fetchedData = await response.json();
        console.log('Fetched data:', fetchedData);
        setData(fetchedData);
      } catch (error) {
        console.error("Error fetching data:", error);
        setError(error.message);
      }
    };

    fetchData();
  }, []);

  const sortData = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    } else {
      direction = 'ascending';
    }

    setSortConfig({ key, direction });

    setData(currentData => {
      const sortedData = [...currentData].sort((a, b) => {
        if (a[key] < b[key]) {
          return direction === 'ascending' ? -1 : 1;
        }
        if (a[key] > b[key]) {
          return direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });

      return sortedData;
    });
  };

  return (
    <div className="app-container">
      {/* Display error if there is one */}
      {error && <div>Error: {error}</div>}

      {/* Table with sorting */}
      <Table data={data} sortData={sortData} />
    </div>
  );
}

export default App;
