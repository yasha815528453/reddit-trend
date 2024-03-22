import React from 'react';
import './Table.css';

const Table = ({ data, sortData }) => (
  <div className="table-container">
    <table>
      <thead>
        <tr>
          <th onClick={() => sortData('KEYWORD')}>Keyword</th>
          <th onClick={() => sortData('TODAY_COUNT')}>Today's Count</th>
          <th onClick={() => sortData('SUBREDDIT')}>Subreddit</th>
          <th onClick={() => sortData('RATIO_24H')}>24h Ratio</th>
          <th onClick={() => sortData('RATIO_1W')}>1 Week Ratio</th>
          <th onClick={() => sortData('RATIO_1M')}>1 Month Ratio</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={index}>
            <td>{item.KEYWORD}</td>
            <td>{item.TODAY_COUNT}</td>
            <td>{item.SUBREDDIT}</td>
            <td>{item.RATIO_24H ? item.RATIO_24H.toFixed(2) : 'N/A'}</td>
            <td>{item.RATIO_1W ? item.RATIO_1W.toFixed(2) : 'N/A'}</td>
            <td>{item.RATIO_1M ? item.RATIO_1M.toFixed(2) : 'N/A'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default Table;
