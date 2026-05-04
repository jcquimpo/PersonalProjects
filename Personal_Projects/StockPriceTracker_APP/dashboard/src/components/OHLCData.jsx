import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './OHLCData.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SYMBOL_NAMES = {
  "AAPL": "Apple Inc.",
  "MSFT": "Microsoft Corporation",
  "NVDA": "NVIDIA Corporation",
  "TSLA": "Tesla Inc.",
  "AMZN": "Amazon Inc.",
  "GOOGL": "Alphabet Inc.",
  "META": "Meta Platforms",
  "BRK.B": "Berkshire Hathaway",
  "JNJ": "Johnson & Johnson",
  "V": "Visa Inc.",
};

function OHLCData({ ohlcData, title = "OHLC Data" }) {
  const [selectedSymbol, setSelectedSymbol] = useState(null);

  const getCompanyName = (symbol) => {
    return SYMBOL_NAMES[symbol] || symbol;
  };

  const formatCurrency = (value) => {
    return `$${parseFloat(value).toFixed(2)}`;
  };

  if (!ohlcData || Object.keys(ohlcData).length === 0) {
    return (
      <section className="section ohlc-section">
        <h2>{title}</h2>
        <p className="no-data">No OHLC data available</p>
      </section>
    );
  }

  const symbols = Object.keys(ohlcData);
  const activeSymbol = selectedSymbol || symbols[0];
  const data = ohlcData[activeSymbol];

  if (!data || !data.dates) {
    return (
      <section className="section ohlc-section">
        <h2>{title}</h2>
        <p className="no-data">No data available for selected symbol</p>
      </section>
    );
  }

  // Prepare chart data
  const chartData = {
    labels: data.dates.map(date => new Date(date).toLocaleDateString()),
    datasets: [
      {
        label: 'Open',
        data: data.opens,
        borderColor: '#60a5fa',
        backgroundColor: 'rgba(96, 165, 250, 0.1)',
        tension: 0.3,
        fill: false,
      },
      {
        label: 'High',
        data: data.highs,
        borderColor: '#22c55e',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.3,
        fill: false,
      },
      {
        label: 'Low',
        data: data.lows,
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        tension: 0.3,
        fill: false,
      },
      {
        label: 'Close',
        data: data.closes,
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        tension: 0.3,
        fill: false,
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: '#cbd5e1',
          padding: 15,
        },
      },
      title: {
        display: true,
        text: `${activeSymbol} - ${getCompanyName(activeSymbol)}`,
        color: '#60a5fa',
      },
    },
    scales: {
      y: {
        ticks: {
          color: '#94a3b8',
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
        },
      },
      x: {
        ticks: {
          color: '#94a3b8',
        },
        grid: {
          color: 'rgba(148, 163, 184, 0.1)',
        },
      },
    },
  };

  return (
    <section className="section ohlc-section">
      <h2>{title}</h2>

      {/* Symbol selector */}
      <div className="symbol-selector">
        {symbols.map(symbol => (
          <button
            key={symbol}
            className={`symbol-btn ${activeSymbol === symbol ? 'active' : ''}`}
            onClick={() => setSelectedSymbol(symbol)}
          >
            {symbol}
          </button>
        ))}
      </div>

      {/* Chart */}
      <div className="chart-container">
        <Line data={chartData} options={chartOptions} />
      </div>

      {/* Table */}
      <div className="ohlc-table-container">
        <h3>Price Data for {activeSymbol}</h3>
        <table className="ohlc-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
            </tr>
          </thead>
          <tbody>
            {data.dates.map((date, index) => (
              <tr key={index}>
                <td>{new Date(date).toLocaleDateString()}</td>
                <td>{formatCurrency(data.opens[index])}</td>
                <td className="high">{formatCurrency(data.highs[index])}</td>
                <td className="low">{formatCurrency(data.lows[index])}</td>
                <td className="close">{formatCurrency(data.closes[index])}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default OHLCData;
